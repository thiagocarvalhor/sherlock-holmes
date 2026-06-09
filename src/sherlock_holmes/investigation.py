"""Compatibility wrapper for the manual-row investigation use case."""

from sherlock_holmes.application.use_cases.investigate_manual_row import (
    DEFAULT_WINDOW_DAYS,
    FetchFn,
    InvestigationResult,
    build_search_window,
    investigate_row,
    load_manual_rows,
)

__all__ = [
    "DEFAULT_WINDOW_DAYS",
    "FetchFn",
    "InvestigationResult",
    "build_search_window",
    "investigate_row",
    "load_manual_rows",
]
