from __future__ import annotations

import csv
import json
import os
import time
from pathlib import Path
from typing import Any

from sherlock_holmes.adapters.outbound.ocr.extractors import OcrExtractor
from sherlock_holmes.preprocessing.presets import apply_preset

TOOLS = ("tesseract", "paddleocr", "doctr")


def configure_local_caches(root_dir: Path) -> None:
    cache_root = root_dir / ".cache"
    os.environ["HOME"] = str(root_dir)
    os.environ["USERPROFILE"] = str(root_dir)
    os.environ.setdefault("XDG_CACHE_HOME", str(cache_root))
    os.environ.setdefault("PADDLE_PDX_CACHE_HOME", str(cache_root / "paddlex"))
    os.environ.setdefault("PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT", "False")
    os.environ.setdefault("DOCTR_CACHE_DIR", str(cache_root / "doctr"))
    os.environ.setdefault("TORCH_HOME", str(cache_root / "torch"))
    os.environ.setdefault("HF_HOME", str(cache_root / "huggingface"))
    os.environ.setdefault("DOCTR_MULTIPROCESSING_DISABLE", "TRUE")


def load_manifest(path: Path, limit: int | None) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    return rows[:limit] if limit is not None else rows


def run_ocr_manifest(
    *,
    root_dir: Path,
    tool: str,
    preset: str,
    manifest: Path,
    output_root: Path,
    interim_root: Path,
    run_id: str,
    limit: int | None = None,
    doctr_pretrained: bool = True,
) -> Path:
    configure_local_caches(root_dir)
    rows = load_manifest(manifest, limit)
    extractor = OcrExtractor(tool, doctr_pretrained=doctr_pretrained)
    summary_rows: list[dict[str, Any]] = []

    for row in rows:
        input_path = root_dir / row["relative_path"]
        category = row["category"]
        interim_dir = interim_root / run_id / preset / category
        output_path = output_root / run_id / tool / preset / category / f"{input_path.stem}.json"

        started_at = time.perf_counter()
        text = ""
        raw: Any = None
        confidence_avg = None
        error = None
        processed_path = input_path
        preprocessing_notes: dict[str, Any] = {}

        try:
            processed_path, preprocessing_notes = apply_preset(input_path, preset, interim_dir)
            output = extractor.extract(processed_path)
            text = output.text
            raw = output.raw
            confidence_avg = output.confidence_avg
            status = "success"
        except Exception as exc:  # noqa: BLE001 - batch output must capture tool failures.
            status = "error"
            error = f"{type(exc).__name__}: {exc}"

        elapsed_seconds = time.perf_counter() - started_at
        payload = build_result_payload(
            root_dir=root_dir,
            tool=tool,
            preset=preset,
            row=row,
            status=status,
            elapsed_seconds=elapsed_seconds,
            text=text,
            raw=raw,
            confidence_avg=confidence_avg,
            processed_path=processed_path,
            preprocessing_notes=preprocessing_notes,
            error=error,
        )
        write_json(output_path, payload)

        summary_rows.append(
            {
                "tool": tool,
                "preset": preset,
                "category": category,
                "input_path": row["relative_path"],
                "status": status,
                "elapsed_seconds": payload["elapsed_seconds"],
                "text_length": payload["text_length"],
                "word_count": payload["word_count"],
                "confidence_avg": confidence_avg,
                "output_path": output_path.relative_to(root_dir).as_posix(),
                "error": error,
            }
        )

        print(
            f"{tool}/{preset} {category}/{input_path.name}: "
            f"{status} text_length={len(text)} elapsed={elapsed_seconds:.2f}s"
        )

    summary_path = output_root / run_id / tool / preset / "summary.csv"
    write_summary(summary_path, summary_rows)
    return summary_path


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def write_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "tool",
        "preset",
        "category",
        "input_path",
        "status",
        "elapsed_seconds",
        "text_length",
        "word_count",
        "confidence_avg",
        "output_path",
        "error",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_result_payload(
    *,
    root_dir: Path,
    tool: str,
    preset: str,
    row: dict[str, str],
    status: str,
    elapsed_seconds: float,
    text: str,
    raw: Any,
    confidence_avg: float | None,
    processed_path: Path,
    preprocessing_notes: dict[str, Any],
    error: str | None,
) -> dict[str, Any]:
    return {
        "tool": tool,
        "preset": preset,
        "category": row["category"],
        "input_path": row["relative_path"],
        "processed_input_path": processed_path.relative_to(root_dir).as_posix(),
        "status": status,
        "elapsed_seconds": round(elapsed_seconds, 6),
        "text": text,
        "text_length": len(text),
        "word_count": len(text.split()),
        "confidence_avg": confidence_avg,
        "raw_output": raw,
        "preprocessing": preprocessing_notes,
        "error": error,
    }
