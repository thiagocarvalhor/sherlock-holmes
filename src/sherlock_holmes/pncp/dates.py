"""Date helpers for PNCP API parameters."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

PNCP_MAX_DATE_RANGE_DAYS = 365


@dataclass(frozen=True)
class PncpDateRange:
    """PNCP date range formatted for query parameters."""

    data_inicial: str
    data_final: str


def format_pncp_date(value: date | datetime | str) -> str:
    """Format a date-like value as YYYYMMDD for PNCP APIs."""

    if isinstance(value, datetime):
        return value.strftime("%Y%m%d")
    if isinstance(value, date):
        return value.strftime("%Y%m%d")

    parsed = parse_pncp_date(value)
    return parsed.strftime("%Y%m%d")


def parse_pncp_date(value: str) -> date:
    """Parse a YYYYMMDD string into a date."""

    text = str(value or "").strip()
    try:
        return datetime.strptime(text, "%Y%m%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid PNCP date: {value!r} (expected YYYYMMDD)") from exc


def validate_pncp_date_range(
    data_inicial: date | datetime | str,
    data_final: date | datetime | str,
    *,
    max_days: int = PNCP_MAX_DATE_RANGE_DAYS,
) -> PncpDateRange:
    """Validate and format a PNCP date range."""

    start_text = format_pncp_date(data_inicial)
    end_text = format_pncp_date(data_final)
    start = parse_pncp_date(start_text)
    end = parse_pncp_date(end_text)

    days = (end - start).days
    if days < 0:
        raise ValueError(f"Invalid PNCP date range: {start_text} is after {end_text}")
    if days > max_days:
        raise ValueError(
            f"Invalid PNCP date range: {days} days exceeds the {max_days}-day limit"
        )

    return PncpDateRange(data_inicial=start_text, data_final=end_text)


def default_date_range(days_back: int = 30, *, today: date | None = None) -> PncpDateRange:
    """Return a default PNCP date range ending today."""

    if days_back < 0:
        raise ValueError("days_back must be non-negative")

    end = today or date.today()
    start = end - timedelta(days=days_back)
    return validate_pncp_date_range(start, end)
