"""Streamlit page: comparacao de registro manual versus candidatos PNCP."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

DEFAULT_COMPARISON_JSON = (
    ROOT_DIR / "data/processed/comparison/row67/record_comparison.json"
)

STATUS_COLORS = {
    "match": "#d4edda",
    "partial_match": "#fff3cd",
    "divergent": "#f8d7da",
    "missing_in_manual": "#e2e3e5",
    "missing_in_official": "#e2e3e5",
    "unresolved": "#e2e3e5",
    "inconclusive": "#e2e3e5",
}

STATUS_LABELS = {
    "match": "✅ match",
    "partial_match": "⚠️ partial_match",
    "divergent": "❌ divergent",
    "missing_in_manual": "— missing_manual",
    "missing_in_official": "— missing_oficial",
    "unresolved": "— unresolved",
    "inconclusive": "— inconclusive",
}


def color_status(val: str) -> str:
    bg = STATUS_COLORS.get(val, "#ffffff")
    return f"background-color: {bg}"


def load_comparison(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_candidates_df(records: list[dict]) -> pd.DataFrame:
    rows = []
    for r in records:
        rows.append(
            {
                "numero_controle_pncp": r["numero_controle_pncp"],
                "score": r["overall_score"],
                "status": r["status"],
                "objeto": _field_value(r, "objeto_contrato", "official_value"),
                "valor": _field_value(r, "valor_contrato", "official_value"),
                "vigencia_inicio": _field_value(r, "vigencia_inicio", "official_value"),
            }
        )
    return pd.DataFrame(rows)


def build_fields_df(record: dict) -> pd.DataFrame:
    rows = []
    for f in record["fields"]:
        rows.append(
            {
                "campo": f["field_name"],
                "manual": f["manual_value"],
                "oficial": f["official_value"],
                "status": f["status"],
                "score": f["similarity_score"],
            }
        )
    return pd.DataFrame(rows)


def _field_value(record: dict, field_name: str, side: str) -> str:
    for f in record["fields"]:
        if f["field_name"] == field_name:
            v = f.get(side)
            return str(v) if v is not None else ""
    return ""


def _manual_info(records: list[dict]) -> dict:
    if not records:
        return {}
    fields = records[0]["fields"]
    return {f["field_name"]: f.get("manual_value") for f in fields}


st.set_page_config(page_title="Comparação Manual vs PNCP", layout="wide")
st.title("Comparação Manual vs PNCP")

with st.sidebar:
    st.header("Arquivo de comparação")
    custom_path = st.text_input(
        "Caminho do JSON",
        value=str(DEFAULT_COMPARISON_JSON),
    )
    json_path = Path(custom_path)

if not json_path.exists():
    st.error(f"Arquivo não encontrado: `{json_path}`")
    st.stop()

records = load_comparison(json_path)
manual = _manual_info(records)

with st.expander("Registro manual", expanded=True):
    col1, col2, col3 = st.columns(3)
    col1.metric("CNPJ", manual.get("cnpj", "—"))
    col2.metric("Município / UF", f"{manual.get('municipio', '—')} / {manual.get('uf', '—')}")
    col3.metric("Valor contrato", manual.get("valor_contrato", "—"))

    col4, col5, col6 = st.columns(3)
    col4.metric("Número contrato", manual.get("numero_contrato", "—"))
    col5.metric("Vigência início", manual.get("vigencia_inicio", "—"))
    col6.metric("Vigência fim", manual.get("vigencia_fim", "—"))

    st.caption(f"Objeto: {manual.get('objeto_contrato', '—')}")

st.divider()
st.subheader(f"Candidatos PNCP — {len(records)} avaliados")

candidates_df = build_candidates_df(records)

styled = candidates_df.style.map(color_status, subset=["status"]).format(
    {"score": "{:.4f}"}
)
st.dataframe(styled, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Detalhe campo a campo")

numero_controles = [r["numero_controle_pncp"] for r in records]
selected = st.selectbox(
    "Selecione o candidato",
    options=numero_controles,
    index=0,
    format_func=lambda v: f"{v}  (score={next(r['overall_score'] for r in records if r['numero_controle_pncp'] == v):.4f})",
)

selected_record = next(r for r in records if r["numero_controle_pncp"] == selected)

col_score, col_status = st.columns(2)
col_score.metric("Score geral", f"{selected_record['overall_score']:.4f}")
col_status.metric("Status", STATUS_LABELS.get(selected_record["status"], selected_record["status"]))

fields_df = build_fields_df(selected_record)

styled_fields = fields_df.style.map(color_status, subset=["status"]).format(
    {"score": "{:.2f}"}
)
st.dataframe(styled_fields, use_container_width=True, hide_index=True)
