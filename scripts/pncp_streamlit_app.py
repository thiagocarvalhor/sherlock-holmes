"""Sherlock Holmes — investigação de contratos públicos (PNCP)."""

from __future__ import annotations

import streamlit as st

from sherlock_holmes.webapp.ui import inject_css
from sherlock_holmes.webapp.views import render_busca_tab, render_comparacao_tab


def main() -> None:
    st.set_page_config(page_title="Sherlock Holmes — PNCP", layout="wide")
    inject_css()
    st.title("Sherlock Holmes")
    st.caption("PNCP primeiro · Documentos depois · OCR quando necessário · Evidência sempre")

    tab_comparacao, tab_busca = st.tabs(["⚖️ Comparação", "🔍 Busca PNCP"])
    with tab_comparacao:
        render_comparacao_tab()
    with tab_busca:
        render_busca_tab()


if __name__ == "__main__":
    main()
