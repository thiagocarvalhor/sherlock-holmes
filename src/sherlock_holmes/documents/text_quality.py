"""Text normalization and coarse quality signals."""

from __future__ import annotations

import re
from dataclasses import dataclass


CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
SPACE_RE = re.compile(r"[ \t]+")
LINEBREAK_RE = re.compile(r"\n{3,}")
MOJIBAKE_MARKERS = ("Ã", "Â", "�")


@dataclass(frozen=True)
class TextQuality:
    """Coarse quality metrics for extracted text."""

    quality: str
    text_length: int
    word_count: int
    line_count: int
    mojibake_marker_count: int
    should_consider_ocr: bool
    notes: str


def normalize_extracted_text(text: str) -> str:
    """Apply light normalization without changing document semantics."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = CONTROL_CHARS_RE.sub("", normalized)
    normalized = "\n".join(SPACE_RE.sub(" ", line).strip() for line in normalized.split("\n"))
    normalized = LINEBREAK_RE.sub("\n\n", normalized)
    return normalized.strip()


def assess_text_quality(text: str) -> TextQuality:
    """Return simple quality signals for direct extraction output."""

    normalized = normalize_extracted_text(text)
    words = normalized.split()
    line_count = len(normalized.splitlines()) if normalized else 0
    mojibake_count = sum(normalized.count(marker) for marker in MOJIBAKE_MARKERS)

    if not normalized:
        quality = "empty"
        should_consider_ocr = True
        notes = "No text extracted."
    elif len(normalized) < 100 or len(words) < 20:
        quality = "poor"
        should_consider_ocr = True
        notes = "Extracted text is very short."
    elif mojibake_count > max(10, len(words) // 20):
        quality = "partial"
        should_consider_ocr = False
        notes = "Text is usable but contains many encoding artifacts."
    else:
        quality = "good"
        should_consider_ocr = False
        notes = "Text appears usable for direct review."

    return TextQuality(
        quality=quality,
        text_length=len(normalized),
        word_count=len(words),
        line_count=line_count,
        mojibake_marker_count=mojibake_count,
        should_consider_ocr=should_consider_ocr,
        notes=notes,
    )
