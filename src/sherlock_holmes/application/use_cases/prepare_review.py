"""Prepare operational review recommendations for comparison results."""

from __future__ import annotations

from typing import Any

from sherlock_holmes.domain.entities import RecordComparison
from sherlock_holmes.domain.services import ReviewAssessment, assess_review_needs


def prepare_review(
    comparison: RecordComparison,
    documents: list[dict[str, Any]],
) -> ReviewAssessment:
    """Prepare document-review and OCR recommendations for one comparison."""

    return assess_review_needs(comparison, documents)


__all__ = ["prepare_review"]
