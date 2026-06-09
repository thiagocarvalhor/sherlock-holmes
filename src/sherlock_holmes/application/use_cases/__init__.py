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
from sherlock_holmes.application.use_cases.compare_manual_record import compare_manual_record
from sherlock_holmes.application.use_cases.enrich_cnpj import enrich_cnpj
from sherlock_holmes.application.use_cases.investigate_manual_row import (
    DEFAULT_WINDOW_DAYS,
    FetchFn,
    InvestigationResult,
    build_search_window,
    investigate_row,
    load_manual_rows,
)
from sherlock_holmes.application.use_cases.list_contract_documents import list_contract_documents
from sherlock_holmes.application.use_cases.prepare_review import prepare_review
from sherlock_holmes.application.use_cases.search_pncp_contracts import search_pncp_contracts

__all__ = [
    "DEFAULT_WINDOW_DAYS",
    "FetchFn",
    "InvestigationResult",
    "build_audit_report",
    "build_batch_audit_report",
    "build_search_window",
    "compare_manual_record",
    "enrich_cnpj",
    "investigate_row",
    "load_cnpj_enrichments",
    "load_comparison_results",
    "load_document_references",
    "list_contract_documents",
    "load_manual_rows",
    "prepare_review",
    "render_audit_report_markdown",
    "render_batch_audit_report_markdown",
    "search_pncp_contracts",
    "summarize_comparisons",
    "write_audit_report_json",
    "write_audit_report_markdown",
    "write_batch_audit_report_json",
    "write_batch_audit_report_markdown",
]
