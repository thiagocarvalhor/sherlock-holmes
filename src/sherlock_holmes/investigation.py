"""Compatibility wrapper for the manual-row investigation use case."""

from __future__ import annotations

from typing import Any

from sherlock_holmes.adapters.outbound.pncp import PncpContractSearchGateway
from sherlock_holmes.application.use_cases.investigate_manual_row import (
    DEFAULT_WINDOW_DAYS,
    FetchFn,
    InvestigationResult,
    build_search_window,
    load_manual_rows,
)
from sherlock_holmes.application.use_cases.investigate_manual_row import (
    investigate_row as _investigate_row,
)


def investigate_row(
    manual_row: dict[str, Any],
    *,
    fetch_fn: FetchFn | None = None,
    window_days: int = DEFAULT_WINDOW_DAYS,
    page_size: int = 500,
    max_pages: int = 20,
    timeout: int = 30,
) -> InvestigationResult:
    """Investigate one manual row, using the live PNCP adapter by default."""

    return _investigate_row(
        manual_row,
        fetch_fn=fetch_fn or PncpContractSearchGateway(),
        window_days=window_days,
        page_size=page_size,
        max_pages=max_pages,
        timeout=timeout,
    )


__all__ = [
    "DEFAULT_WINDOW_DAYS",
    "FetchFn",
    "InvestigationResult",
    "build_search_window",
    "investigate_row",
    "load_manual_rows",
]
