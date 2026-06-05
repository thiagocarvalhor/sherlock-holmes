"""Comparison data helpers for Streamlit pages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sherlock_holmes.pncp.client import contract_detail_url  # noqa: E402

DEFAULT_COMPARISON_JSON = (
    ROOT_DIR / "data/processed/comparison/row67/record_comparison.json"
)


def load_comparison(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_numero_controle_pncp(numero: str) -> tuple[str, int, int] | None:
    """Extract (cnpj, ano, sequencial) from '39485438000142-2-000019/2025'."""
    match = re.fullmatch(r"(\d{14})-\d+-(\d+)/(\d{4})", numero.strip())
    if not match:
        return None
    cnpj, sequencial, ano = match.group(1), int(match.group(2)), int(match.group(3))
    return cnpj, ano, sequencial


def candidate_detail_url(numero_controle: str) -> str | None:
    parsed = parse_numero_controle_pncp(numero_controle)
    if not parsed:
        return None
    cnpj, ano, sequencial = parsed
    return contract_detail_url(cnpj, ano, sequencial)


def build_candidates_df(records: list[dict]) -> pd.DataFrame:
    rows = []
    for r in records:
        rows.append({
            "numero_controle_pncp": r["numero_controle_pncp"],
            "score": r["overall_score"],
            "status": r["status"],
            "objeto": _field_value(r, "objeto_contrato", "official_value"),
            "valor": _field_value(r, "valor_contrato", "official_value"),
            "vigencia_inicio": _field_value(r, "vigencia_inicio", "official_value"),
        })
    return pd.DataFrame(rows)


def build_fields_df(record: dict) -> pd.DataFrame:
    rows = [
        {
            "campo": f["field_name"],
            "manual": f["manual_value"],
            "oficial": f["official_value"],
            "status": f["status"],
            "score": f["similarity_score"],
        }
        for f in record["fields"]
    ]
    return pd.DataFrame(rows)


def manual_info(records: list[dict]) -> dict[str, Any]:
    if not records:
        return {}
    return {f["field_name"]: f.get("manual_value") for f in records[0]["fields"]}


def _field_value(record: dict, field_name: str, side: str) -> str:
    for f in record["fields"]:
        if f["field_name"] == field_name:
            v = f.get(side)
            return str(v) if v is not None else ""
    return ""
