"""File type inspection and direct text extraction."""

from __future__ import annotations

import zipfile
from dataclasses import dataclass
from pathlib import Path


PDF_SIGNATURE = b"%PDF"
ZIP_SIGNATURE = b"PK\x03\x04"
UTF_BOMS = (b"\xef\xbb\xbf", b"\xff\xfe", b"\xfe\xff")


@dataclass(frozen=True)
class DocumentInspection:
    """Basic file type information."""

    path: str
    file_type: str
    extension: str
    size_bytes: int
    detection_method: str


@dataclass(frozen=True)
class DirectTextExtraction:
    """Result of a direct text extraction attempt."""

    path: str
    file_type: str
    status: str
    text: str
    text_length: int
    page_count: int | None = None
    notes: str = ""


def detect_document_type(path: Path) -> DocumentInspection:
    """Detect a document type using file signature first and extension second."""

    path = Path(path)
    signature = path.read_bytes()[:8]
    extension = path.suffix.lower()

    if signature.startswith(PDF_SIGNATURE):
        file_type = "pdf"
        method = "signature"
    elif signature.startswith(ZIP_SIGNATURE):
        file_type = "zip"
        method = "signature"
    elif _looks_like_text(path, signature):
        file_type = "text"
        method = "content"
    elif extension in {".pdf", ".zip", ".txt", ".csv", ".md"}:
        file_type = extension.lstrip(".")
        method = "extension"
    else:
        file_type = "binary"
        method = "fallback"

    return DocumentInspection(
        path=path.as_posix(),
        file_type=file_type,
        extension=extension,
        size_bytes=path.stat().st_size,
        detection_method=method,
    )


def extract_text_direct(path: Path, *, max_pages: int | None = None) -> DirectTextExtraction:
    """Extract text directly when the file type supports it."""

    inspection = detect_document_type(path)
    path = Path(path)

    if inspection.file_type == "pdf":
        return _extract_pdf_text(path, inspection, max_pages=max_pages)

    if inspection.file_type in {"text", "txt", "csv", "md"}:
        text = _read_text(path)
        return DirectTextExtraction(
            path=inspection.path,
            file_type=inspection.file_type,
            status="success",
            text=text,
            text_length=len(text),
            notes="Text read directly from file.",
        )

    if inspection.file_type == "zip":
        text = _zip_inventory_text(path)
        return DirectTextExtraction(
            path=inspection.path,
            file_type="zip",
            status="unsupported_container",
            text=text,
            text_length=len(text),
            notes="ZIP inventory generated. Extract nested files before text extraction.",
        )

    return DirectTextExtraction(
        path=inspection.path,
        file_type=inspection.file_type,
        status="unsupported",
        text="",
        text_length=0,
        notes="Direct text extraction is not supported for this file type.",
    )


def _extract_pdf_text(
    path: Path,
    inspection: DocumentInspection,
    *,
    max_pages: int | None,
) -> DirectTextExtraction:
    import pypdfium2 as pdfium

    document = pdfium.PdfDocument(str(path))
    page_count = len(document)
    limit = min(page_count, max_pages) if max_pages is not None else page_count
    parts: list[str] = []

    for index in range(limit):
        page = document[index]
        textpage = page.get_textpage()
        parts.append(textpage.get_text_range())
        textpage.close()
        page.close()

    text = "\n".join(part.strip() for part in parts if part.strip())
    status = "success" if text.strip() else "no_text"
    return DirectTextExtraction(
        path=inspection.path,
        file_type="pdf",
        status=status,
        text=text,
        text_length=len(text),
        page_count=page_count,
        notes="Text extracted with pypdfium2." if text else "No text layer found.",
    )


def _zip_inventory_text(path: Path) -> str:
    rows = ["ZIP entries:"]
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            rows.append(f"- {info.filename} ({info.file_size} bytes)")
    return "\n".join(rows)


def _looks_like_text(path: Path, signature: bytes) -> bool:
    if signature.startswith(UTF_BOMS):
        return True
    sample = path.read_bytes()[:2048]
    if not sample:
        return True
    if b"\x00" in sample:
        return False
    try:
        sample.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")
