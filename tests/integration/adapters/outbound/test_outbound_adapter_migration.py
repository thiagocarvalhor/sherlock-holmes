"""Compatibility checks for outbound adapter migrations."""

from __future__ import annotations

from sherlock_holmes.adapters.outbound.brasilapi import client as brasilapi_adapter
from sherlock_holmes.adapters.outbound.filesystem.documents import inspection as documents_adapter
from sherlock_holmes.adapters.outbound.ocr import extractors as ocr_adapter
from sherlock_holmes.adapters.outbound.pncp import client as pncp_adapter
from sherlock_holmes.documents import inspection as documents_legacy
from sherlock_holmes.enrichment import brasilapi as brasilapi_legacy
from sherlock_holmes.ocr import extractors as ocr_legacy
from sherlock_holmes.pncp import client as pncp_legacy


def test_legacy_pncp_client_points_to_outbound_adapter():
    assert pncp_legacy.PncpRequestResult is pncp_adapter.PncpRequestResult
    assert pncp_legacy.fetch_contracts_by_publication is pncp_adapter.fetch_contracts_by_publication
    assert pncp_legacy.fetch_contract_files is pncp_adapter.fetch_contract_files


def test_legacy_brasilapi_client_points_to_outbound_adapter():
    assert brasilapi_legacy.BrasilApiCnpjRecord is brasilapi_adapter.BrasilApiCnpjRecord
    assert brasilapi_legacy.fetch_cnpj is brasilapi_adapter.fetch_cnpj


def test_legacy_documents_package_points_to_filesystem_adapter():
    assert documents_legacy.DocumentInspection is documents_adapter.DocumentInspection
    assert documents_legacy.extract_text_direct is documents_adapter.extract_text_direct


def test_legacy_ocr_package_points_to_outbound_adapter():
    assert ocr_legacy.OcrExtractor is ocr_adapter.OcrExtractor
    assert ocr_legacy.OcrOutput is ocr_adapter.OcrOutput
