"""Compatibility wrapper for OCR fallback decision helpers."""

from sherlock_holmes.adapters.outbound.filesystem.documents.ocr_fallback import (
    OcrFallbackDecision,
    decide_ocr_fallback,
)

__all__ = [
    "OcrFallbackDecision",
    "decide_ocr_fallback",
]
