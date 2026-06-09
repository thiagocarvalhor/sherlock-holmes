"""Compatibility wrapper for PNCP date helpers."""

from sherlock_holmes.adapters.outbound.pncp.dates import (
    PNCP_MAX_DATE_RANGE_DAYS,
    PncpDateRange,
    default_date_range,
    format_pncp_date,
    parse_pncp_date,
    validate_pncp_date_range,
)

__all__ = [
    "PNCP_MAX_DATE_RANGE_DAYS",
    "PncpDateRange",
    "default_date_range",
    "format_pncp_date",
    "parse_pncp_date",
    "validate_pncp_date_range",
]
