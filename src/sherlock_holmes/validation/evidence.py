"""Evidence records for auditable validation flows."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sherlock_holmes.documents import DirectTextExtraction
from sherlock_holmes.pncp.arquivos import PncpDocumentReference

SOURCE_TYPES = {
    "official_api",
    "official_document",
    "manual_spreadsheet",
    "ocr_extracted",
    "llm_extracted",
    "human_reviewed",
    "unresolved",
}

CONFIDENCE_LEVELS = {"high", "medium", "low", "reviewed", "unknown"}


@dataclass(frozen=True)
class EvidenceRecord:
    """One auditable source behind a value, file, or extracted text."""

    evidence_id: str
    source_type: str
    confidence_level: str
    method: str
    collected_at: str
    source_url: str = ""
    local_path: str = ""
    field_name: str = ""
    value: Any = None
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def evidence_from_official_api(
    *,
    evidence_id: str,
    source_url: str,
    method: str,
    value: Any = None,
    field_name: str = "",
    metadata: dict[str, Any] | None = None,
    notes: str = "",
) -> EvidenceRecord:
    """Create high-confidence evidence from an official structured API."""

    return _record(
        evidence_id=evidence_id,
        source_type="official_api",
        confidence_level="high",
        method=method,
        source_url=source_url,
        field_name=field_name,
        value=value,
        metadata=metadata or {},
        notes=notes,
    )


def evidence_from_document_reference(
    reference: PncpDocumentReference,
    *,
    evidence_id: str,
    notes: str = "",
) -> EvidenceRecord:
    """Create medium-confidence evidence from an official document reference."""

    return _record(
        evidence_id=evidence_id,
        source_type="official_document",
        confidence_level="medium",
        method="pncp_document_reference",
        source_url=reference.url or reference.uri,
        value=reference.title,
        metadata={
            "resource_type": reference.resource_type,
            "resource_id": reference.resource_id,
            "document_type": reference.document_type,
            "sequence": reference.sequence,
            "published_at": reference.published_at,
        },
        notes=notes,
    )


def evidence_from_extracted_text(
    extraction: DirectTextExtraction,
    *,
    evidence_id: str,
    confidence_level: str = "medium",
    notes: str = "",
) -> EvidenceRecord:
    """Create evidence from direct text extraction output."""

    return _record(
        evidence_id=evidence_id,
        source_type="official_document",
        confidence_level=confidence_level,
        method="direct_text_extraction",
        local_path=extraction.path,
        value=extraction.text,
        metadata={
            "file_type": extraction.file_type,
            "status": extraction.status,
            "text_length": extraction.text_length,
            "page_count": extraction.page_count,
            "notes": extraction.notes,
        },
        notes=notes,
    )


def evidence_from_manual_spreadsheet(
    *,
    evidence_id: str,
    field_name: str,
    value: Any,
    source_row: str,
    source_path: str = "",
    notes: str = "",
) -> EvidenceRecord:
    """Create evidence from a manual spreadsheet row."""

    return _record(
        evidence_id=evidence_id,
        source_type="manual_spreadsheet",
        confidence_level="unknown",
        method="manual_spreadsheet",
        local_path=source_path,
        field_name=field_name,
        value=value,
        metadata={"source_row": source_row},
        notes=notes,
    )


def write_evidence_records(records: list[EvidenceRecord], *, output_path: Path) -> Path:
    """Persist evidence records as JSON."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump([asdict(record) for record in records], file, ensure_ascii=False, indent=2)
    return output_path


def _record(
    *,
    evidence_id: str,
    source_type: str,
    confidence_level: str,
    method: str,
    source_url: str = "",
    local_path: str = "",
    field_name: str = "",
    value: Any = None,
    metadata: dict[str, Any] | None = None,
    notes: str = "",
) -> EvidenceRecord:
    if source_type not in SOURCE_TYPES:
        raise ValueError(f"Unknown source_type: {source_type}")
    if confidence_level not in CONFIDENCE_LEVELS:
        raise ValueError(f"Unknown confidence_level: {confidence_level}")

    return EvidenceRecord(
        evidence_id=evidence_id,
        source_type=source_type,
        confidence_level=confidence_level,
        method=method,
        collected_at=datetime.now(timezone.utc).isoformat(),
        source_url=source_url,
        local_path=local_path,
        field_name=field_name,
        value=value,
        notes=notes,
        metadata=metadata or {},
    )
