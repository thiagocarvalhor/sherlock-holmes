"""Compatibility wrapper for inbound Streamlit comparison helpers."""

from sherlock_holmes.adapters.inbound.streamlit.comparison import (
    MANUAL_FIELDS,
    candidate_detail_url,
    candidates_dataframe,
    match_count,
)

__all__ = [
    "MANUAL_FIELDS",
    "candidate_detail_url",
    "candidates_dataframe",
    "match_count",
]
