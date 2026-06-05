"""Document inspection and direct text extraction helpers."""

from sherlock_holmes.documents.inspection import (
    DocumentInspection,
    DirectTextExtraction,
    ExtractedZipMember,
    ZipMember,
    detect_document_type,
    extract_zip_members,
    extract_text_direct,
    list_zip_members,
    write_text_extraction_result,
)
from sherlock_holmes.documents.ocr_fallback import (
    OcrFallbackDecision,
    decide_ocr_fallback,
)
from sherlock_holmes.documents.text_quality import (
    TextQuality,
    assess_text_quality,
    normalize_extracted_text,
)


__all__ = [
    "DirectTextExtraction",
    "DocumentInspection",
    "ExtractedZipMember",
    "OcrFallbackDecision",
    "ZipMember",
    "TextQuality",
    "detect_document_type",
    "decide_ocr_fallback",
    "assess_text_quality",
    "extract_zip_members",
    "extract_text_direct",
    "list_zip_members",
    "normalize_extracted_text",
    "write_text_extraction_result",
]
