"""Shared UI helpers for the Streamlit app: theme, badges and cards."""

from __future__ import annotations

import streamlit as st

# Background / text colors for status pills.
STATUS_COLORS: dict[str, str] = {
    "match": "#d4edda",
    "partial_match": "#fff3cd",
    "divergent": "#f8d7da",
    "missing_in_manual": "#e2e3e5",
    "missing_in_official": "#e2e3e5",
    "unresolved": "#e2e3e5",
    "inconclusive": "#e2e3e5",
}

STATUS_TEXT_COLORS: dict[str, str] = {
    "match": "#155724",
    "partial_match": "#856404",
    "divergent": "#721c24",
    "missing_in_manual": "#383d41",
    "missing_in_official": "#383d41",
    "unresolved": "#383d41",
    "inconclusive": "#383d41",
}

STATUS_LABELS: dict[str, str] = {
    "match": "✅ match",
    "partial_match": "⚠️ parcial",
    "divergent": "❌ divergente",
    "missing_in_manual": "— sem manual",
    "missing_in_official": "— sem oficial",
    "unresolved": "— indefinido",
    "inconclusive": "— inconclusivo",
}


def color_status(val: str) -> str:
    """Pandas Styler helper: background color for a status cell."""
    bg = STATUS_COLORS.get(val, "#ffffff")
    return f"background-color: {bg}"


def inject_css() -> None:
    """Inject the app stylesheet once per session."""
    st.markdown(
        """
        <style>
        .sh-badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 0.80rem;
            font-weight: 600;
            line-height: 1.4;
            white-space: nowrap;
        }
        .sh-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding: 6px 0;
            border-bottom: 1px solid rgba(128,128,128,0.15);
        }
        .sh-row:last-child { border-bottom: none; }
        .sh-field { font-weight: 600; min-width: 130px; }
        .sh-vals { flex: 1; font-size: 0.86rem; opacity: 0.9; }
        .sh-vals .manual { color: #6c757d; }
        .sh-muted { color: #6c757d; font-size: 0.85rem; }
        .stTabs [data-baseweb="tab"] { font-size: 1.0rem; font-weight: 600; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def status_badge(status: str) -> str:
    """Return an HTML pill for a comparison status."""
    bg = STATUS_COLORS.get(status, "#e2e3e5")
    fg = STATUS_TEXT_COLORS.get(status, "#383d41")
    label = STATUS_LABELS.get(status, status)
    return f'<span class="sh-badge" style="background:{bg};color:{fg};">{label}</span>'


def field_row_html(field_name: str, manual_value, official_value, status: str) -> str:
    """Render one field-by-field comparison row as HTML."""
    manual = "—" if manual_value in (None, "") else str(manual_value)
    official = "—" if official_value in (None, "") else str(official_value)
    return (
        '<div class="sh-row">'
        f'<span class="sh-field">{field_name}</span>'
        f'<span class="sh-vals"><span class="manual">{manual}</span> &nbsp;→&nbsp; {official}</span>'
        f"{status_badge(status)}"
        "</div>"
    )
