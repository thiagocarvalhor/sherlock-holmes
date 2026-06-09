"""Sherlock Holmes - investigacao de contratos publicos (PNCP)."""

from __future__ import annotations

import streamlit as st

from sherlock_holmes.adapters.inbound.streamlit import inject_css, render_app


def main() -> None:
    st.set_page_config(page_title="Sherlock Holmes - PNCP", layout="wide")
    inject_css()
    st.title("Sherlock Holmes")
    st.caption("PNCP primeiro. Documentos depois. OCR quando necessario. Evidencia sempre.")
    render_app()


if __name__ == "__main__":
    main()
