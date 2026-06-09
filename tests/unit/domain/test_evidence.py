"""Tests for evidence records."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError

import pytest

from sherlock_holmes.validation import (
    EvidenceRecord,
    evidence_from_manual_spreadsheet,
    evidence_from_official_api,
    write_evidence_records,
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


def test_write_evidence_roundtrip(tmp_path):
    records = [
        evidence_from_official_api(
            evidence_id="e1",
            source_url="https://pncp.gov.br/api",
            method="m",
        ),
        evidence_from_manual_spreadsheet(
            evidence_id="m1",
            field_name="cnpj",
            value="39485438000142",
            source_row="67",
        ),
    ]
    out = tmp_path / "evidence.json"
    written = write_evidence_records(records, output_path=out)

    assert written == out
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["evidence_id"] == "e1"
    assert data[1]["source_type"] == "manual_spreadsheet"


def test_evidence_record_is_frozen():
    record = evidence_from_official_api(evidence_id="e1", source_url="u", method="m")
    assert isinstance(record, EvidenceRecord)
    with pytest.raises(FrozenInstanceError):
        record.evidence_id = "e2"  # type: ignore[misc]
