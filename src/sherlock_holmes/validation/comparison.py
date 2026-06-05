"""Field-by-field and record-level comparison helpers."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
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

RECORD_COMPARISON_STATUSES = {
    "match",
    "partial_match",
    "divergent",
    "inconclusive",
}

_CRITICAL_FIELDS = {"valor_contrato", "numero_contrato"}

_FIELD_MAPPING: list[tuple[str, str, str, str]] = [
    # (manual_key, pncp_path, nested_key, value_type)
    ("cnpj",            "orgaoEntidade",  "cnpj",          "cnpj"),
    ("municipio",       "unidadeOrgao",   "municipioNome", "text"),
    ("uf",              "unidadeOrgao",   "ufSigla",       "text"),
    ("objeto_contrato", "",               "objetoContrato","text"),
    ("numero_contrato", "",               "numeroContratoEmpenho", "text"),
    ("valor_contrato",  "",               "valorGlobal",   "number"),
    ("vigencia_inicio", "",               "dataVigenciaInicio", "date"),
    ("vigencia_fim",    "",               "dataVigenciaFim",    "date"),
]


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


def _nested_get(record: dict[str, Any], parent_key: str, child_key: str) -> Any:
    if parent_key:
        parent = record.get(parent_key) or {}
        return parent.get(child_key) if isinstance(parent, dict) else None
    return record.get(child_key)


@dataclass
class RecordComparison:
    """Comparison between one manual record and one PNCP contract record."""

    source_row: str
    numero_controle_pncp: str
    fields: list[FieldComparison] = field(default_factory=list)
    overall_score: float = 0.0
    status: str = "inconclusive"
    notes: str = ""


def compare_records(
    *,
    source_row: str,
    manual_record: dict[str, Any],
    pncp_record: dict[str, Any],
    manual_evidence: EvidenceRecord,
    official_evidence: EvidenceRecord,
) -> RecordComparison:
    """Compare all mapped fields between a manual record and a PNCP contract."""

    numero_controle_pncp = pncp_record.get("numeroControlePNCP", "")
    comparisons: list[FieldComparison] = []

    for manual_key, parent_key, pncp_key, value_type in _FIELD_MAPPING:
        manual_value = manual_record.get(manual_key)
        official_value = _nested_get(pncp_record, parent_key, pncp_key)
        comparisons.append(
            compare_field_values(
                field_name=manual_key,
                manual_value=manual_value,
                official_value=official_value,
                manual_evidence=manual_evidence,
                official_evidence=official_evidence,
                value_type=value_type,
            )
        )

    comparable = [
        c for c in comparisons
        if c.status not in {"unresolved", "missing_in_manual", "missing_in_official"}
    ]

    if not comparable:
        return RecordComparison(
            source_row=source_row,
            numero_controle_pncp=numero_controle_pncp,
            fields=comparisons,
            overall_score=0.0,
            status="inconclusive",
            notes="No comparable fields found.",
        )

    overall_score = sum(c.similarity_score for c in comparable) / len(comparable)

    critical_divergent = any(
        c.field_name in _CRITICAL_FIELDS and c.status == "divergent"
        for c in comparable
    )

    if critical_divergent:
        status = "divergent"
    elif overall_score >= 0.9:
        status = "match"
    elif overall_score >= 0.4:
        status = "partial_match"
    else:
        status = "divergent"

    return RecordComparison(
        source_row=source_row,
        numero_controle_pncp=numero_controle_pncp,
        fields=comparisons,
        overall_score=round(overall_score, 4),
        status=status,
    )
