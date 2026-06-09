"""Review workflow decisions for comparison results."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sherlock_holmes.domain.entities import RecordComparison

REVIEW_FIELD_STATUSES = {
    "partial_match",
    "divergent",
    "missing_in_official",
    "missing_in_manual",
}


@dataclass(frozen=True)
class ReviewAssessment:
    """Operational review and OCR recommendation for one comparison."""

    document_review_required: bool
    document_review_status: str
    document_review_label: str
    ocr_status: str
    ocr_label: str
    review_fields_count: int
    review_fields: list[str]
    documents_count: int

    def to_dict(self) -> dict[str, Any]:
        """Return the stable dictionary shape used by reports and the webapp."""

        return asdict(self)


def assess_review_needs(
    comparison: RecordComparison,
    documents: list[dict[str, Any]],
) -> ReviewAssessment:
    """Assess whether a comparison needs document review and possible OCR."""

    review_fields = [field for field in comparison.fields if field.status in REVIEW_FIELD_STATUSES]
    has_documents = bool(documents)

    if not review_fields:
        document_review_status = "nao_necessaria"
        document_review_label = "Nao necessaria"
        ocr_status = "nao_necessario"
        ocr_label = "Nao necessario"
    elif has_documents:
        document_review_status = "revisar_documento"
        document_review_label = "Revisar documento"
        ocr_status = "pode_precisar"
        ocr_label = "Pode precisar"
    else:
        document_review_status = "sem_documento"
        document_review_label = "Sem documento"
        ocr_status = "nao_avaliado"
        ocr_label = "Nao avaliado"

    return ReviewAssessment(
        document_review_required=bool(review_fields),
        document_review_status=document_review_status,
        document_review_label=document_review_label,
        ocr_status=ocr_status,
        ocr_label=ocr_label,
        review_fields_count=len(review_fields),
        review_fields=[field.field_name for field in review_fields],
        documents_count=len(documents),
    )


__all__ = [
    "REVIEW_FIELD_STATUSES",
    "ReviewAssessment",
    "assess_review_needs",
]
