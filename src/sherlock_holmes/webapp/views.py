"""Compatibility wrapper for inbound Streamlit views."""

from typing import Any

from sherlock_holmes.adapters.inbound.streamlit import views as _views
from sherlock_holmes.adapters.inbound.streamlit.views import (
    REVIEW_STATUS_LABELS,
    REVIEW_STATUS_OPTIONS,
    ContractCandidate,
    cached_cnpj_enrichment,
    cached_investigate_row,
    render_app,
    render_busca_tab,
    render_comparacao_tab,
    render_comparison_section,
    render_document_search_section,
)


def __getattr__(name: str) -> Any:
    """Return legacy private helpers from the inbound Streamlit implementation."""

    return getattr(_views, name)


__all__ = [
    "ContractCandidate",
    "REVIEW_STATUS_LABELS",
    "REVIEW_STATUS_OPTIONS",
    "cached_cnpj_enrichment",
    "cached_investigate_row",
    "render_app",
    "render_busca_tab",
    "render_comparacao_tab",
    "render_comparison_section",
    "render_document_search_section",
]
