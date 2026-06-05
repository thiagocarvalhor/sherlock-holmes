"""Shared UI helpers for Streamlit pages."""

from __future__ import annotations

STATUS_COLORS: dict[str, str] = {
    "match": "#d4edda",
    "partial_match": "#fff3cd",
    "divergent": "#f8d7da",
    "missing_in_manual": "#e2e3e5",
    "missing_in_official": "#e2e3e5",
    "unresolved": "#e2e3e5",
    "inconclusive": "#e2e3e5",
}

STATUS_LABELS: dict[str, str] = {
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
