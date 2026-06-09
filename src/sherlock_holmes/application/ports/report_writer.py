"""Port for writing audit reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ReportWriter(Protocol):
    """Persist audit reports in one or more formats."""

    def write_json(self, report: dict[str, Any], *, output_path: str | Path) -> Path:
        """Persist a report as JSON."""

    def write_markdown(self, report: dict[str, Any], *, output_path: str | Path) -> Path:
        """Persist a report as Markdown."""
