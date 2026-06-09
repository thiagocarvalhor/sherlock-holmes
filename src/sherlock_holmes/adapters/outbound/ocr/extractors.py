from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class OcrOutput:
    text: str
    raw: Any
    confidence_avg: float | None = None


class OcrExtractor:
    def __init__(self, tool: str, *, doctr_pretrained: bool = True) -> None:
        self.tool = tool
        self.doctr_pretrained = doctr_pretrained
        self._model: Any = None

    def extract(self, image_path: Path) -> OcrOutput:
        if self.tool == "tesseract":
            return self._extract_tesseract(image_path)
        if self.tool == "paddleocr":
            return self._extract_paddleocr(image_path)
        if self.tool == "doctr":
            return self._extract_doctr(image_path)
        raise ValueError(f"Unknown OCR tool: {self.tool}")

    def _extract_tesseract(self, image_path: Path) -> OcrOutput:
        tesseract_cmd = _resolve_tesseract_cmd()
        if tesseract_cmd is None:
            raise RuntimeError("tesseract executable was not found in PATH or common install paths")

        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        text = pytesseract.image_to_string(str(image_path))
        return OcrOutput(
            text=text,
            raw={"engine": "tesseract", "version": str(pytesseract.get_tesseract_version())},
        )

    def _extract_paddleocr(self, image_path: Path) -> OcrOutput:
        if self._model is None:
            # Keep this import local. PaddleOCR/PaddlePaddle and Torch should not
            # be imported together by benchmark orchestration on Windows.
            from paddleocr import PaddleOCR

            self._model = PaddleOCR(
                lang="en",
                ocr_version="PP-OCRv4",
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )

        results = self._model.predict(str(image_path))
        raw = [_to_jsonable(result) for result in results]
        text_parts = _collect_values(raw, {"rec_text", "rec_texts", "text"})
        score_values = _collect_numeric_values(raw, {"rec_score", "rec_scores", "score"})
        confidence = sum(score_values) / len(score_values) if score_values else None
        return OcrOutput(text="\n".join(text_parts), raw=raw, confidence_avg=confidence)

    def _extract_doctr(self, image_path: Path) -> OcrOutput:
        if self._model is None:
            from doctr.models import ocr_predictor

            self._model = ocr_predictor(
                pretrained=self.doctr_pretrained,
                pretrained_backbone=self.doctr_pretrained,
            )

        from doctr.io import DocumentFile

        document = DocumentFile.from_images(str(image_path))
        result = self._model(document)
        return OcrOutput(text=result.render(), raw=result.export())


def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "json"):
        return value.json
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    return value


def _collect_values(value: Any, target_keys: set[str]) -> list[str]:
    values: list[str] = []

    if isinstance(value, dict):
        for key, item in value.items():
            if key in target_keys:
                values.extend(_string_values(item))
            else:
                values.extend(_collect_values(item, target_keys))
    elif isinstance(value, list):
        for item in value:
            values.extend(_collect_values(item, target_keys))

    return values


def _collect_numeric_values(value: Any, target_keys: set[str]) -> list[float]:
    values: list[float] = []

    if isinstance(value, dict):
        for key, item in value.items():
            if key in target_keys:
                values.extend(_numeric_values(item))
            else:
                values.extend(_collect_numeric_values(item, target_keys))
    elif isinstance(value, list):
        for item in value:
            values.extend(_collect_numeric_values(item, target_keys))

    return values


def _string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(_string_values(item))
        return values
    return []


def _resolve_tesseract_cmd() -> str | None:
    candidates = [
        shutil.which("tesseract"),
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]

    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)

    return None


def _numeric_values(value: Any) -> list[float]:
    if isinstance(value, (int, float)):
        return [float(value)]
    if isinstance(value, list):
        values: list[float] = []
        for item in value:
            values.extend(_numeric_values(item))
        return values
    return []
