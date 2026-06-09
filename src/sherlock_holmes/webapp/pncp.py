"""Compatibility wrapper for inbound Streamlit PNCP helpers."""

from sherlock_holmes.adapters.inbound.streamlit.pncp import (
    KEYWORD_SUGGESTIONS,
    PRESET_ORGAOS,
    TABLE_COLUMNS,
    cached_contract_files,
    cached_contract_search,
    contract_detail_url,
    contract_file_download_url,
    filter_records_by_terms,
    normalize_topic_key,
    record_label,
    records_to_dataframe,
    suggested_terms,
)

__all__ = [
    "KEYWORD_SUGGESTIONS",
    "PRESET_ORGAOS",
    "TABLE_COLUMNS",
    "cached_contract_files",
    "cached_contract_search",
    "contract_detail_url",
    "contract_file_download_url",
    "filter_records_by_terms",
    "normalize_topic_key",
    "record_label",
    "records_to_dataframe",
    "suggested_terms",
]
