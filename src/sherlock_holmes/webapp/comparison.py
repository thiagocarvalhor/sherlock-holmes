"""Comparison display helpers for the Streamlit app."""

from __future__ import annotations

import pandas as pd

from sherlock_holmes.pncp.client import contract_detail_url
from sherlock_holmes.pncp.ids import parse_numero_controle_pncp
from sherlock_holmes.validation import RecordComparison

# Manual-row keys shown in the "registro manual" header.
MANUAL_FIELDS = [
    ("cnpj", "CNPJ"),
    ("municipio", "Município"),
    ("uf", "UF"),
    ("numero_contrato", "Número"),
    ("valor_contrato", "Valor"),
    ("vigencia_inicio", "Vigência início"),
    ("vigencia_fim", "Vigência fim"),
]


def candidate_detail_url(numero_controle: str) -> str | None:
    """Build a PNCP detail URL from a numeroControlePNCP, or None if invalid."""
    try:
        resource = parse_numero_controle_pncp(numero_controle)
    except ValueError:
        return None
    return contract_detail_url(resource.orgao_cnpj, resource.ano, resource.sequencial)


def candidates_dataframe(comparisons: list[RecordComparison]) -> pd.DataFrame:
    """Build a ranked candidates table from RecordComparison objects."""
    rows = []
    for c in comparisons:
        rows.append({
            "numero_controle_pncp": c.numero_controle_pncp,
            "score": c.overall_score,
            "status": c.status,
            "objeto": _field(c, "objeto_contrato"),
            "valor": _field(c, "valor_contrato"),
            "vigencia_inicio": _field(c, "vigencia_inicio"),
        })
    return pd.DataFrame(rows)


def match_count(comparison: RecordComparison) -> tuple[int, int]:
    """Return (fields in 'match', total fields) for a comparison."""
    total = len(comparison.fields)
    matched = sum(1 for f in comparison.fields if f.status == "match")
    return matched, total


def _field(comparison: RecordComparison, field_name: str) -> str:
    for f in comparison.fields:
        if f.field_name == field_name:
            return "" if f.official_value is None else str(f.official_value)
    return ""
