"""Compatibility wrapper for domain comparison models."""

from sherlock_holmes.domain.entities.comparison import (
    COMPARISON_STATUSES,
    RECORD_COMPARISON_STATUSES,
    FieldComparison,
    RecordComparison,
    compare_field_values,
    compare_records,
)

__all__ = [
    "COMPARISON_STATUSES",
    "RECORD_COMPARISON_STATUSES",
    "FieldComparison",
    "RecordComparison",
    "compare_field_values",
    "compare_records",
]
