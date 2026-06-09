"""Filesystem adapter for audit report outputs."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

MarkdownRenderer = Callable[[dict[str, Any]], str]


class FileSystemReportWriter:
    """Persist audit reports as JSON or Markdown files."""

    def __init__(self, markdown_renderer: MarkdownRenderer | None = None) -> None:
        self._markdown_renderer = markdown_renderer

    def write_json(self, report: dict[str, Any], *, output_path: str | Path) -> Path:
        """Persist a report as JSON."""

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def write_markdown(self, report: dict[str, Any], *, output_path: str | Path) -> Path:
        """Persist a report as Markdown."""

        if self._markdown_renderer is None:
            raise ValueError("FileSystemReportWriter requires a markdown renderer.")

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self._markdown_renderer(report), encoding="utf-8")
        return path


__all__ = ["FileSystemReportWriter", "MarkdownRenderer"]
