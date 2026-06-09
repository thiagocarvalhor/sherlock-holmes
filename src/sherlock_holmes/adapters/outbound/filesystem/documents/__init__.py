"""Filesystem document inspection and direct extraction adapters."""

from sherlock_holmes.adapters.outbound.filesystem.documents.inspection import (
    DirectTextExtraction,
    DocumentInspection,
    ExtractedZipMember,
    ZipMember,
    detect_document_type,
    extract_text_direct,
    extract_zip_members,
    list_zip_members,
    write_text_extraction_result,
)
from sherlock_holmes.adapters.outbound.filesystem.documents.ocr_fallback import (
    OcrFallbackDecision,
    decide_ocr_fallback,
)
from sherlock_holmes.adapters.outbound.filesystem.documents.text_quality import (
    TextQuality,
    assess_text_quality,
    normalize_extracted_text,
)

__all__ = [
    "DirectTextExtraction",
    "DocumentInspection",
    "ExtractedZipMember",
    "OcrFallbackDecision",
    "TextQuality",
    "ZipMember",
    "assess_text_quality",
    "decide_ocr_fallback",
    "detect_document_type",
    "extract_text_direct",
    "extract_zip_members",
    "list_zip_members",
    "normalize_extracted_text",
    "write_text_extraction_result",
]
