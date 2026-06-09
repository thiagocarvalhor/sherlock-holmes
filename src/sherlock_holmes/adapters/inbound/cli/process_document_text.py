"""Process a local document with direct text extraction before OCR."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from sherlock_holmes.adapters.outbound.filesystem.documents import (
    detect_document_type,
    extract_text_direct,
    extract_zip_members,
    list_zip_members,
    write_text_extraction_result,
)

ROOT_DIR = Path(__file__).resolve().parents[5]


DEFAULT_INTERIM_ROOT = ROOT_DIR / "data" / "interim" / "pncp" / "documents"
DEFAULT_OUTPUT_ROOT = ROOT_DIR / "data" / "processed" / "pncp" / "documents"
DEFAULT_ZIP_EXTENSIONS = (".pdf", ".txt", ".csv", ".md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process a local document with direct text extraction."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--interim-root", type=Path, default=DEFAULT_INTERIM_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--max-pages", type=int, default=None)
    parser.add_argument("--zip-extension", action="append", default=[])
    return parser.parse_args()


def resolve_project_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT_DIR / path


def safe_stem(path: Path) -> str:
    stem = re.sub(r"[^0-9A-Za-z._-]+", "_", path.stem).strip("._")
    return stem or "document"


def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
    return path


def process_one(path: Path, *, output_dir: Path, max_pages: int | None) -> Path:
    extraction = extract_text_direct(path, max_pages=max_pages)
    output_path = output_dir / "text" / f"{safe_stem(path)}.json"
    return write_text_extraction_result(extraction, output_path=output_path)


def run() -> None:
    args = parse_args()
    input_path = resolve_project_path(args.input)
    if not input_path.is_file():
        raise FileNotFoundError(input_path)

    run_id = args.run_id or datetime.now().strftime("document-processing-%Y%m%d-%H%M%S")
    interim_dir = resolve_project_path(args.interim_root) / run_id
    output_dir = resolve_project_path(args.output_root) / run_id
    allowed_extensions = set(args.zip_extension or DEFAULT_ZIP_EXTENSIONS)

    inspection = detect_document_type(input_path)
    inspection_path = write_json(output_dir / "inspection.json", asdict(inspection))

    text_outputs: list[str] = []
    extracted_members: list[dict] = []
    zip_members: list[dict] = []

    if inspection.file_type == "zip":
        members = list_zip_members(input_path)
        zip_members = [asdict(member) for member in members]
        write_json(output_dir / "zip_members.json", {"members": zip_members})

        extracted = extract_zip_members(
            input_path,
            output_dir=interim_dir,
            allowed_extensions=allowed_extensions,
        )
        extracted_members = [asdict(member) for member in extracted]
        write_json(output_dir / "extracted_members.json", {"members": extracted_members})

        for member in extracted:
            text_outputs.append(
                process_one(Path(member.local_path), output_dir=output_dir, max_pages=args.max_pages)
                .relative_to(ROOT_DIR)
                .as_posix()
            )
    else:
        text_outputs.append(
            process_one(input_path, output_dir=output_dir, max_pages=args.max_pages)
            .relative_to(ROOT_DIR)
            .as_posix()
        )

    summary = {
        "run_id": run_id,
        "input_path": input_path.relative_to(ROOT_DIR).as_posix(),
        "inspection_path": inspection_path.relative_to(ROOT_DIR).as_posix(),
        "file_type": inspection.file_type,
        "zip_members_count": len(zip_members),
        "extracted_members_count": len(extracted_members),
        "text_outputs": text_outputs,
    }
    summary_path = write_json(output_dir / "summary.json", summary)

    print(f"run_id={run_id}")
    print(f"file_type={inspection.file_type}")
    print(f"summary={summary_path.relative_to(ROOT_DIR).as_posix()}")
    print(f"text_outputs={len(text_outputs)}")


if __name__ == "__main__":
    run()
