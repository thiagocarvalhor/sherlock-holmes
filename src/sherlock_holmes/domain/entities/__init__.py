"""Domain entities with identity and lifecycle."""

from sherlock_holmes.domain.entities.comparison import (
    COMPARISON_STATUSES,
    RECORD_COMPARISON_STATUSES,
    FieldComparison,
    RecordComparison,
    compare_field_values,
    compare_records,
)
from sherlock_holmes.domain.entities.evidence import (
    CONFIDENCE_LEVELS,
    SOURCE_TYPES,
    EvidenceRecord,
    evidence_from_document_reference,
    evidence_from_extracted_text,
    evidence_from_manual_spreadsheet,
    evidence_from_official_api,
)

__all__ = [
    "CONFIDENCE_LEVELS",
    "COMPARISON_STATUSES",
    "RECORD_COMPARISON_STATUSES",
    "SOURCE_TYPES",
    "EvidenceRecord",
    "FieldComparison",
    "RecordComparison",
    "compare_field_values",
    "compare_records",
    "evidence_from_document_reference",
    "evidence_from_extracted_text",
    "evidence_from_manual_spreadsheet",
    "evidence_from_official_api",
]
