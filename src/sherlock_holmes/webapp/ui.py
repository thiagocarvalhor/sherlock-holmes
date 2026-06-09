"""Compatibility wrapper for inbound Streamlit UI helpers."""

from sherlock_holmes.adapters.inbound.streamlit.ui import (
    color_status,
    field_row_html,
    inject_css,
    status_badge,
)

__all__ = [
    "color_status",
    "field_row_html",
    "inject_css",
    "status_badge",
]
