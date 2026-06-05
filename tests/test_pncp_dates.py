"""Tests for PNCP date helpers."""

from __future__ import annotations

from datetime import date

import pytest

from sherlock_holmes.pncp.dates import (
    PncpDateRange,
    default_date_range,
    format_pncp_date,
    parse_pncp_date,
    validate_pncp_date_range,
)


def test_format_pncp_date_from_date():
    assert format_pncp_date(date(2025, 11, 4)) == "20251104"


def test_parse_pncp_date_roundtrip():
    assert parse_pncp_date("20251104") == date(2025, 11, 4)


def test_parse_pncp_date_invalid():
    with pytest.raises(ValueError):
        parse_pncp_date("2025-11-04")


def test_validate_range_ok():
    result = validate_pncp_date_range("20250920", "20251219")
    assert result == PncpDateRange(data_inicial="20250920", data_final="20251219")


def test_validate_range_inverted():
    with pytest.raises(ValueError):
        validate_pncp_date_range("20251219", "20250920")


def test_validate_range_exceeds_limit():
    with pytest.raises(ValueError):
        validate_pncp_date_range("20240101", "20251231", max_days=365)


def test_default_date_range_window():
    result = default_date_range(days_back=30, today=date(2025, 11, 4))
    assert result.data_final == "20251104"
    assert result.data_inicial == "20251005"


def test_default_date_range_negative():
    with pytest.raises(ValueError):
        default_date_range(days_back=-1)
