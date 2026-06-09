"""Compatibility wrapper for filesystem document text-quality helpers."""

from sherlock_holmes.adapters.outbound.filesystem.documents.text_quality import (
    TextQuality,
    assess_text_quality,
    normalize_extracted_text,
)

__all__ = [
    "TextQuality",
    "assess_text_quality",
    "normalize_extracted_text",
]
