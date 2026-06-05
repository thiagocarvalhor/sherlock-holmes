"""File type inspection and direct text extraction."""

from __future__ import annotations

import zipfile
from dataclasses import dataclass
import json
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


@dataclass(frozen=True)
class ZipMember:
    """Metadata for a member inside a ZIP archive."""

    filename: str
    size_bytes: int
    compressed_size_bytes: int
    is_dir: bool


@dataclass(frozen=True)
class ExtractedZipMember:
    """A ZIP member extracted to a controlled local path."""

    filename: str
    local_path: str
    size_bytes: int


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


def list_zip_members(path: Path) -> list[ZipMember]:
    """List members of a ZIP archive without extracting them."""

    with zipfile.ZipFile(path) as archive:
        return [
            ZipMember(
                filename=info.filename,
                size_bytes=info.file_size,
                compressed_size_bytes=info.compress_size,
                is_dir=info.is_dir(),
            )
            for info in archive.infolist()
        ]


def extract_zip_members(
    path: Path,
    *,
    output_dir: Path,
    allowed_extensions: set[str] | None = None,
) -> list[ExtractedZipMember]:
    """Extract ZIP members to output_dir, rejecting unsafe member paths."""

    path = Path(path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    extracted: list[ExtractedZipMember] = []
    allowed = {ext.lower() for ext in allowed_extensions} if allowed_extensions else None

    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue

            member_path = Path(info.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValueError(f"Unsafe ZIP member path: {info.filename}")

            if allowed is not None and member_path.suffix.lower() not in allowed:
                continue

            target_path = output_dir / member_path.name
            with archive.open(info) as source, target_path.open("wb") as target:
                target.write(source.read())

            extracted.append(
                ExtractedZipMember(
                    filename=info.filename,
                    local_path=target_path.as_posix(),
                    size_bytes=info.file_size,
                )
            )

    return extracted


def write_text_extraction_result(
    extraction: DirectTextExtraction,
    *,
    output_path: Path,
) -> Path:
    """Persist a direct text extraction result as JSON."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "path": extraction.path,
        "file_type": extraction.file_type,
        "status": extraction.status,
        "text": extraction.text,
        "text_length": extraction.text_length,
        "page_count": extraction.page_count,
        "notes": extraction.notes,
    }
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
    return output_path


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
