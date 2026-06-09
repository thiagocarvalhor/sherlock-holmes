"""Compatibility checks for inbound adapter migrations."""

from __future__ import annotations

from sherlock_holmes.adapters.inbound.streamlit import views as streamlit_views
from sherlock_holmes.webapp import views as legacy_views


def test_legacy_webapp_views_point_to_streamlit_adapter():
    assert legacy_views.render_app is streamlit_views.render_app
    assert legacy_views.render_document_search_section is streamlit_views.render_document_search_section
    assert legacy_views._rank_contract_candidates is streamlit_views._rank_contract_candidates


def test_script_wrappers_point_to_inbound_cli_adapters():
    from scripts import generate_audit_report, process_document_text, run_pncp_api_smoke

    from sherlock_holmes.adapters.inbound.cli import (
        generate_audit_report as audit_adapter,
    )
    from sherlock_holmes.adapters.inbound.cli import (
        process_document_text as document_adapter,
    )
    from sherlock_holmes.adapters.inbound.cli import (
        run_pncp_api_smoke as pncp_smoke_adapter,
    )

    assert generate_audit_report.main is audit_adapter.main
    assert process_document_text.run is document_adapter.run
    assert run_pncp_api_smoke.run is pncp_smoke_adapter.run
