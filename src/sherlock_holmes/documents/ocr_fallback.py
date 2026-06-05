"""Decision helpers for OCR fallback."""

from __future__ import annotations

from dataclasses import dataclass

from sherlock_holmes.documents.inspection import DirectTextExtraction
from sherlock_holmes.documents.text_quality import TextQuality, assess_text_quality


@dataclass(frozen=True)
class OcrFallbackDecision:
    """Operational decision about whether OCR should be considered."""

    status: str
    should_run_ocr: bool
    reason: str
    extraction_status: str
    text_quality: str


def decide_ocr_fallback(
    extraction: DirectTextExtraction,
    *,
    quality: TextQuality | None = None,
) -> OcrFallbackDecision:
    """Decide whether OCR should be considered for an extraction result."""

    quality = quality or assess_text_quality(extraction.text)

    if extraction.status == "success" and quality.quality == "good":
        return OcrFallbackDecision(
            status="direct_text_ok",
            should_run_ocr=False,
            reason="Direct text extraction produced usable text.",
            extraction_status=extraction.status,
            text_quality=quality.quality,
        )

    if extraction.status == "success" and quality.quality == "partial":
        return OcrFallbackDecision(
            status="manual_review",
            should_run_ocr=False,
            reason="Direct text is usable but should be reviewed before OCR.",
            extraction_status=extraction.status,
            text_quality=quality.quality,
        )

    if extraction.status == "no_text" or quality.quality in {"empty", "poor"}:
        return OcrFallbackDecision(
            status="consider_ocr",
            should_run_ocr=True,
            reason="Direct extraction did not produce enough usable text.",
            extraction_status=extraction.status,
            text_quality=quality.quality,
        )

    if extraction.status in {"unsupported_container", "unsupported"}:
        return OcrFallbackDecision(
            status="manual_review",
            should_run_ocr=False,
            reason="File type needs routing or extraction before OCR decision.",
            extraction_status=extraction.status,
            text_quality=quality.quality,
        )

    return OcrFallbackDecision(
        status="manual_review",
        should_run_ocr=False,
        reason="Fallback decision is inconclusive.",
        extraction_status=extraction.status,
        text_quality=quality.quality,
    )
