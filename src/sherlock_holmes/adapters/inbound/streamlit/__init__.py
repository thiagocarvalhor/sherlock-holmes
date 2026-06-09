"""Inbound Streamlit adapter package."""

from sherlock_holmes.adapters.inbound.streamlit.ui import inject_css
from sherlock_holmes.adapters.inbound.streamlit.views import (
    render_app,
    render_busca_tab,
    render_comparacao_tab,
)

__all__ = [
    "inject_css",
    "render_app",
    "render_busca_tab",
    "render_comparacao_tab",
]
