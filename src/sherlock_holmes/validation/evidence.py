"""Compatibility wrapper for domain evidence models."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from sherlock_holmes.domain.entities.evidence import (
    CONFIDENCE_LEVELS,
    SOURCE_TYPES,
    EvidenceRecord,
    evidence_from_document_reference,
    evidence_from_extracted_text,
    evidence_from_manual_spreadsheet,
    evidence_from_official_api,
)


def write_evidence_records(records: list[EvidenceRecord], *, output_path: Path) -> Path:
    """Persist evidence records as JSON."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump([asdict(record) for record in records], file, ensure_ascii=False, indent=2)
    return output_path


__all__ = [
    "CONFIDENCE_LEVELS",
    "SOURCE_TYPES",
    "EvidenceRecord",
    "evidence_from_document_reference",
    "evidence_from_extracted_text",
    "evidence_from_manual_spreadsheet",
    "evidence_from_official_api",
    "write_evidence_records",
]
