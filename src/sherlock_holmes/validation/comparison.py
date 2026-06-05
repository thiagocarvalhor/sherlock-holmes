"""Field-by-field comparison helpers."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from sherlock_holmes.validation.evidence import EvidenceRecord


COMPARISON_STATUSES = {
    "match",
    "partial_match",
    "divergent",
    "missing_in_manual",
    "missing_in_official",
    "unresolved",
}


@dataclass(frozen=True)
class FieldComparison:
    """Comparison between one manual value and one official value."""

    field_name: str
    manual_value: Any
    official_value: Any
    status: str
    similarity_score: float
    manual_evidence_id: str
    official_evidence_id: str
    notes: str = ""


def compare_field_values(
    *,
    field_name: str,
    manual_value: Any,
    official_value: Any,
    manual_evidence: EvidenceRecord,
    official_evidence: EvidenceRecord,
    value_type: str = "text",
) -> FieldComparison:
    """Compare one field and return a coarse status."""

    if _is_missing(manual_value) and _is_missing(official_value):
        status = "unresolved"
        score = 0.0
        notes = "Both values are missing."
    elif _is_missing(manual_value):
        status = "missing_in_manual"
        score = 0.0
        notes = "Manual value is missing."
    elif _is_missing(official_value):
        status = "missing_in_official"
        score = 0.0
        notes = "Official value is missing."
    else:
        score = _similarity(manual_value, official_value, value_type=value_type)
        if score == 1.0:
            status = "match"
            notes = "Values match after normalization."
        elif score >= 0.75:
            status = "partial_match"
            notes = "Values are similar after normalization."
        else:
            status = "divergent"
            notes = "Values differ after normalization."

    return FieldComparison(
        field_name=field_name,
        manual_value=manual_value,
        official_value=official_value,
        status=status,
        similarity_score=score,
        manual_evidence_id=manual_evidence.evidence_id,
        official_evidence_id=official_evidence.evidence_id,
        notes=notes,
    )


def _is_missing(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def _similarity(left: Any, right: Any, *, value_type: str) -> float:
    if value_type == "cnpj":
        return 1.0 if _digits(left) == _digits(right) else 0.0
    if value_type == "number":
        left_number = _number(left)
        right_number = _number(right)
        if left_number is None or right_number is None:
            return 0.0
        return 1.0 if abs(left_number - right_number) < 0.01 else 0.0
    if value_type == "date":
        return 1.0 if str(left).strip() == str(right).strip() else 0.0

    left_text = _normalized_text(left)
    right_text = _normalized_text(right)
    if left_text == right_text:
        return 1.0
    if left_text and right_text and (left_text in right_text or right_text in left_text):
        return 0.8
    return 0.0


def _digits(value: Any) -> str:
    return "".join(char for char in str(value or "") if char.isdigit())


def _number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value or "").strip()
    if not text:
        return None
    normalized = text.replace(".", "").replace(",", ".") if "," in text else text
    try:
        return float(normalized)
    except ValueError:
        return None


def _normalized_text(value: Any) -> str:
    normalized = unicodedata.normalize("NFKD", str(value or ""))
    without_accents = "".join(char for char in normalized if not unicodedata.combining(char))
    return " ".join(re.sub(r"\s+", " ", without_accents.casefold()).split())
