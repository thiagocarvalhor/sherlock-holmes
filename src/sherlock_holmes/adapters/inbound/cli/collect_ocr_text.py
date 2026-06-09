from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[5]
DEFAULT_OUTPUT_DIR = ROOT_DIR / "data" / "processed" / "ocr-text"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect OCR JSON page outputs into one text file.")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--page-separators", action="store_true")
    return parser.parse_args()


def resolve_project_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT_DIR / path


def page_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"(\d+)", path.stem)
    if match:
        return int(match.group(1)), path.name
    return 10**9, path.name


def load_page_text(path: Path) -> str:
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    text = data.get("text")
    if not isinstance(text, str):
        raise ValueError(f"Missing string field 'text' in {path}")
    return text.strip()


def collect_text(input_dir: Path, *, title: str | None, page_separators: bool) -> str:
    json_paths = sorted(input_dir.glob("*.json"), key=page_sort_key)
    if not json_paths:
        raise FileNotFoundError(f"No JSON files found in {input_dir}")

    parts: list[str] = []
    if title:
        parts.extend([title.strip(), ""])

    for page_index, path in enumerate(json_paths, start=1):
        if page_separators:
            parts.append(f"===== PAGE {page_index:03d} | {path.name} =====")
        parts.append(load_page_text(path))
        parts.append("")

    return "\n".join(parts).strip() + "\n"


def main() -> None:
    args = parse_args()
    input_dir = resolve_project_path(args.input_dir)
    output = (
        resolve_project_path(args.output)
        if args.output
        else DEFAULT_OUTPUT_DIR / f"{input_dir.parent.parent.parent.name}-{input_dir.name}.txt"
    )

    text = collect_text(input_dir, title=args.title, page_separators=args.page_separators)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")

    print(f"Input: {input_dir.relative_to(ROOT_DIR).as_posix()}")
    print(f"Output: {output.relative_to(ROOT_DIR).as_posix()}")
    print(f"Characters: {len(text)}")


if __name__ == "__main__":
    main()
