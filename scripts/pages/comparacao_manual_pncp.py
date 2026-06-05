"""Streamlit page: comparacao de registro manual versus candidatos PNCP."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from sherlock_holmes.webapp.comparison import (
    DEFAULT_COMPARISON_JSON,
    build_candidates_df,
    build_fields_df,
    candidate_detail_url,
    load_comparison,
    manual_info,
)
from sherlock_holmes.webapp.ui import STATUS_LABELS, color_status

st.set_page_config(page_title="Comparação Manual vs PNCP", layout="wide")
st.title("Comparação Manual vs PNCP")

with st.sidebar:
    st.header("Arquivo de comparação")
    custom_path = st.text_input("Caminho do JSON", value=str(DEFAULT_COMPARISON_JSON))
    json_path = Path(custom_path)

    st.divider()
    st.page_link("pncp_streamlit_app.py", label="Explorador PNCP")

if not json_path.exists():
    st.error(f"Arquivo não encontrado: `{json_path}`")
    st.stop()

records = load_comparison(json_path)
info = manual_info(records)

with st.expander("Registro manual", expanded=True):
    col1, col2, col3 = st.columns(3)
    col1.metric("CNPJ", info.get("cnpj", "—"))
    col2.metric("Município / UF", f"{info.get('municipio', '—')} / {info.get('uf', '—')}")
    col3.metric("Valor contrato", info.get("valor_contrato", "—"))

    col4, col5, col6 = st.columns(3)
    col4.metric("Número contrato", info.get("numero_contrato", "—"))
    col5.metric("Vigência início", info.get("vigencia_inicio", "—"))
    col6.metric("Vigência fim", info.get("vigencia_fim", "—"))

    st.caption(f"Objeto: {info.get('objeto_contrato', '—')}")

st.divider()
st.subheader(f"Candidatos PNCP — {len(records)} avaliados")

candidates_df = build_candidates_df(records)
styled = candidates_df.style.map(color_status, subset=["status"]).format({"score": "{:.4f}"})
st.dataframe(styled, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Detalhe campo a campo")

numero_controles = [r["numero_controle_pncp"] for r in records]
selected = st.selectbox(
    "Selecione o candidato",
    options=numero_controles,
    index=0,
    format_func=lambda v: (
        f"{v}  (score={next(r['overall_score'] for r in records if r['numero_controle_pncp'] == v):.4f})"
    ),
)

selected_record = next(r for r in records if r["numero_controle_pncp"] == selected)

col_score, col_status, col_link = st.columns(3)
col_score.metric("Score geral", f"{selected_record['overall_score']:.4f}")
col_status.metric("Status", STATUS_LABELS.get(selected_record["status"], selected_record["status"]))

detail_url = candidate_detail_url(selected)
if detail_url:
    with col_link:
        st.link_button("Abrir no PNCP", detail_url)

fields_df = build_fields_df(selected_record)
styled_fields = fields_df.style.map(color_status, subset=["status"]).format({"score": "{:.2f}"})
st.dataframe(styled_fields, use_container_width=True, hide_index=True)
