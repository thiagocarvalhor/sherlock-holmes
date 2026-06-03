"""Convert PDF pages to OCR-ready images and generate an OCR manifest."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import pypdfium2 as pdfium


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PDF = (
    ROOT_DIR
    / "data"
    / "raw"
    / "dataset"
    / "26-SSO-04 - Contrato de Concessao - Agrupamento Sudeste.pdf"
)
DEFAULT_OUTPUT_ROOT = ROOT_DIR / "data" / "interim" / "ocr" / "pdf-pages"
DEFAULT_MANIFEST_DIR = ROOT_DIR / "documentation" / "plans"

FIELDNAMES = [
    "category",
    "sample_index",
    "relative_path",
    "filename",
    "extension",
    "size_bytes",
    "selection_rank",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render PDF pages as images and write a manifest for scripts/run_ocr_smoke.py."
    )
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--slug", default=None, help="Stable identifier used in output paths.")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--category", default="Contract")
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--format", choices=("jpg", "png"), default="jpg")
    parser.add_argument("--quality", type=int, default=90)
    parser.add_argument("--first-page", type=int, default=1)
    parser.add_argument("--last-page", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def resolve_project_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT_DIR / path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "pdf-document"


def build_paths(args: argparse.Namespace) -> tuple[Path, str, Path, Path]:
    pdf_path = resolve_project_path(args.pdf)
    slug = args.slug or slugify(pdf_path.stem)
    output_dir = resolve_project_path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_ROOT / slug
    manifest_path = (
        resolve_project_path(args.manifest)
        if args.manifest
        else DEFAULT_MANIFEST_DIR / f"ocr-{slug}-pages.csv"
    )
    return pdf_path, slug, output_dir, manifest_path


def validate_args(pdf_path: Path, args: argparse.Namespace) -> None:
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if args.dpi <= 0:
        raise ValueError("--dpi must be greater than zero")
    if args.quality < 1 or args.quality > 100:
        raise ValueError("--quality must be between 1 and 100")
    if args.first_page < 1:
        raise ValueError("--first-page must be greater than zero")
    if args.last_page is not None and args.last_page < args.first_page:
        raise ValueError("--last-page must be greater than or equal to --first-page")


def render_pdf_pages(
    *,
    pdf_path: Path,
    output_dir: Path,
    image_format: str,
    dpi: int,
    quality: int,
    first_page: int,
    last_page: int | None,
    overwrite: bool,
    category: str,
) -> list[dict[str, str | int]]:
    document = pdfium.PdfDocument(str(pdf_path))
    page_count = len(document)
    requested_last_page = last_page or page_count

    if first_page > page_count:
        raise ValueError(f"--first-page {first_page} is greater than PDF page count {page_count}")
    if requested_last_page > page_count:
        raise ValueError(f"--last-page {requested_last_page} is greater than PDF page count {page_count}")

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str | int]] = []
    scale = dpi / 72
    extension = f".{image_format}"

    for sample_index, page_number in enumerate(range(first_page, requested_last_page + 1), start=1):
        output_path = output_dir / f"page-{page_number:03d}{extension}"

        if overwrite or not output_path.exists():
            page = document[page_number - 1]
            image = page.render(scale=scale).to_pil()
            if image.mode != "RGB":
                image = image.convert("RGB")

            if image_format == "jpg":
                image.save(output_path, "JPEG", quality=quality, optimize=True)
            else:
                image.save(output_path, "PNG", optimize=True)

        rows.append(
            {
                "category": category,
                "sample_index": sample_index,
                "relative_path": output_path.relative_to(ROOT_DIR).as_posix(),
                "filename": output_path.name,
                "extension": output_path.suffix.lower(),
                "size_bytes": output_path.stat().st_size,
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
    args = parse_args()
    pdf_path, slug, output_dir, manifest_path = build_paths(args)
    validate_args(pdf_path, args)

    rows = render_pdf_pages(
        pdf_path=pdf_path,
        output_dir=output_dir,
        image_format=args.format,
        dpi=args.dpi,
        quality=args.quality,
        first_page=args.first_page,
        last_page=args.last_page,
        overwrite=args.overwrite,
        category=args.category,
    )
    write_manifest(manifest_path, rows)

    print(f"PDF: {pdf_path.relative_to(ROOT_DIR).as_posix()}")
    print(f"Slug: {slug}")
    print(f"Pages rendered: {len(rows)}")
    print(f"Images: {output_dir.relative_to(ROOT_DIR).as_posix()}")
    print(f"Manifest: {manifest_path.relative_to(ROOT_DIR).as_posix()}")


if __name__ == "__main__":
    main()
