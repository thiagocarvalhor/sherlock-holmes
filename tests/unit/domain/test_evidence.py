"""Tests for evidence records."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from sherlock_holmes.domain.entities import (
    EvidenceRecord,
    evidence_from_manual_spreadsheet,
    evidence_from_official_api,
)


def test_official_api_is_high_confidence():
    record = evidence_from_official_api(
        evidence_id="e1",
        source_url="https://pncp.gov.br/api",
        method="pncp_contratos_search",
        value={"x": 1},
    )
    assert record.source_type == "official_api"
    assert record.confidence_level == "high"
    assert record.collected_at  # ISO timestamp set


def test_manual_spreadsheet_is_unknown_confidence():
    record = evidence_from_manual_spreadsheet(
        evidence_id="m1",
        field_name="cnpj",
        value="39485438000142",
        source_row="67",
    )
    assert record.source_type == "manual_spreadsheet"
    assert record.confidence_level == "unknown"
    assert record.metadata["source_row"] == "67"


def test_evidence_record_is_frozen():
    record = evidence_from_official_api(evidence_id="e1", source_url="u", method="m")
    assert isinstance(record, EvidenceRecord)
    with pytest.raises(FrozenInstanceError):
        record.evidence_id = "e2"  # type: ignore[misc]
