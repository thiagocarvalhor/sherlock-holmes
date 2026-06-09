"""Use cases that orchestrate domain rules and external ports."""

from sherlock_holmes.application.use_cases.build_audit_report import (
    build_audit_report,
    build_batch_audit_report,
    load_cnpj_enrichments,
    load_comparison_results,
    load_document_references,
    render_audit_report_markdown,
    render_batch_audit_report_markdown,
    summarize_comparisons,
    write_audit_report_json,
    write_audit_report_markdown,
    write_batch_audit_report_json,
    write_batch_audit_report_markdown,
)
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
    "build_audit_report",
    "build_batch_audit_report",
    "build_search_window",
    "investigate_row",
    "load_cnpj_enrichments",
    "load_comparison_results",
    "load_document_references",
    "load_manual_rows",
    "render_audit_report_markdown",
    "render_batch_audit_report_markdown",
    "summarize_comparisons",
    "write_audit_report_json",
    "write_audit_report_markdown",
    "write_batch_audit_report_json",
    "write_batch_audit_report_markdown",
]
