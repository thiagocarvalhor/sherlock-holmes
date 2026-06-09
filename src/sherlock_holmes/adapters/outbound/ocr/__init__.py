"""Outbound OCR adapter package."""

from sherlock_holmes.adapters.outbound.ocr.extractors import OcrExtractor, OcrOutput
from sherlock_holmes.adapters.outbound.ocr.manifest_runner import (
    TOOLS,
    build_result_payload,
    configure_local_caches,
    load_manifest,
    run_ocr_manifest,
    write_json,
    write_summary,
)

__all__ = [
    "TOOLS",
    "OcrExtractor",
    "OcrOutput",
    "build_result_payload",
    "configure_local_caches",
    "load_manifest",
    "run_ocr_manifest",
    "write_json",
    "write_summary",
]
