"""Reporting helpers for audit outputs."""

from sherlock_holmes.reporting.audit import (
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

__all__ = [
    "build_audit_report",
    "build_batch_audit_report",
    "load_cnpj_enrichments",
    "load_comparison_results",
    "load_document_references",
    "render_audit_report_markdown",
    "render_batch_audit_report_markdown",
    "summarize_comparisons",
    "write_audit_report_json",
    "write_audit_report_markdown",
    "write_batch_audit_report_json",
    "write_batch_audit_report_markdown",
]
