"""Generate reproducible OCR sample manifests for the initial benchmark."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT_DIR / "data" / "raw" / "dataset"
OUTPUT_DIR = ROOT_DIR / "documentation" / "plans"

CATEGORIES = [
    "ADVE",
    "Email",
    "Form",
    "Letter",
    "Memo",
    "News",
    "Note",
    "Report",
    "Resume",
    "Scientific",
]

ELIGIBLE_EXTENSIONS = {".jpg"}
SMOKE_PER_CATEGORY = 3
BENCHMARK_PER_CATEGORY = 20
SELECTION_SEED = "sherlock-holmes-ocr-v1"

FIELDNAMES = [
    "category",
    "sample_index",
    "relative_path",
    "filename",
    "extension",
    "size_bytes",
    "selection_rank",
]


def selection_key(path: Path) -> str:
    relative_path = path.relative_to(ROOT_DIR).as_posix()
    payload = f"{SELECTION_SEED}:{relative_path}".encode()
    return hashlib.sha256(payload).hexdigest()


def list_category_images(category: str) -> list[Path]:
    category_dir = DATASET_DIR / category
    if not category_dir.is_dir():
        raise FileNotFoundError(f"Missing dataset category: {category_dir}")

    return sorted(
        (
            path
            for path in category_dir.iterdir()
            if path.is_file() and path.suffix.lower() in ELIGIBLE_EXTENSIONS
        ),
        key=selection_key,
    )


def build_rows(per_category: int) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []

    for category in CATEGORIES:
        images = list_category_images(category)
        if len(images) < per_category:
            raise ValueError(
                f"Category {category} has {len(images)} eligible images; "
                f"{per_category} required."
            )

        for sample_index, image_path in enumerate(images[:per_category], start=1):
            rows.append(
                {
                    "category": category,
                    "sample_index": sample_index,
                    "relative_path": image_path.relative_to(ROOT_DIR).as_posix(),
                    "filename": image_path.name,
                    "extension": image_path.suffix.lower(),
                    "size_bytes": image_path.stat().st_size,
                    "selection_rank": sample_index,
                }
            )

    return rows


def write_manifest(path: Path, rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    smoke_rows = build_rows(SMOKE_PER_CATEGORY)
    benchmark_rows = build_rows(BENCHMARK_PER_CATEGORY)

    write_manifest(OUTPUT_DIR / "ocr-smoke-sample-v1.csv", smoke_rows)
    write_manifest(OUTPUT_DIR / "ocr-benchmark-sample-v1.csv", benchmark_rows)

    print(f"Smoke sample rows: {len(smoke_rows)}")
    print(f"Benchmark sample rows: {len(benchmark_rows)}")
    print(f"Seed: {SELECTION_SEED}")


if __name__ == "__main__":
    main()
