from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from sherlock_holmes.ocr.manifest_runner import TOOLS, run_ocr_manifest
from sherlock_holmes.preprocessing.presets import PRESETS

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT_DIR / "data" / "processed" / "ocr"
DEFAULT_INTERIM_ROOT = ROOT_DIR / "data" / "interim" / "ocr"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run OCR for images listed in a manifest.")
    parser.add_argument("--tool", required=True, choices=TOOLS)
    parser.add_argument("--preset", default="none", choices=PRESETS)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--interim-root", type=Path, default=DEFAULT_INTERIM_ROOT)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--no-doctr-pretrained",
        action="store_true",
        help="Instantiate docTR without pretrained weights for setup debugging.",
    )
    return parser.parse_args()


def resolve_project_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT_DIR / path


def main() -> None:
    args = parse_args()
    run_id = args.run_id or datetime.now().strftime("ocr-manifest-%Y%m%d-%H%M%S")
    summary_path = run_ocr_manifest(
        root_dir=ROOT_DIR,
        tool=args.tool,
        preset=args.preset,
        manifest=resolve_project_path(args.manifest),
        output_root=resolve_project_path(args.output_root),
        interim_root=resolve_project_path(args.interim_root),
        run_id=run_id,
        limit=args.limit,
        doctr_pretrained=not args.no_doctr_pretrained,
    )
    print(f"Summary: {summary_path.relative_to(ROOT_DIR).as_posix()}")


if __name__ == "__main__":
    main()
