"""Document reference helpers for PNCP file metadata."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

USER_AGENT = "sherlock-holmes-pncp-documents/0.1"


@dataclass(frozen=True)
class PncpDocumentReference:
    """Auditable reference to a PNCP document or attachment."""

    source: str
    resource_type: str
    resource_id: str
    title: str
    document_type: str
    sequence: int | None
    url: str
    uri: str
    published_at: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class PncpDownloadedDocument:
    """Metadata for a locally downloaded PNCP document."""

    source: str
    resource_type: str
    resource_id: str
    url: str
    local_path: str
    content_type: str
    bytes_written: int
    downloaded_at: str
    reference: PncpDocumentReference


def document_reference_from_pncp_file(
    file_record: dict[str, Any],
    *,
    resource_type: str,
    resource_id: str,
    source: str = "pncp",
) -> PncpDocumentReference:
    """Build a standardized document reference from PNCP file metadata."""

    sequence = _optional_int(file_record.get("sequencialDocumento"))
    return PncpDocumentReference(
        source=source,
        resource_type=resource_type,
        resource_id=resource_id,
        title=str(file_record.get("titulo") or file_record.get("nome") or ""),
        document_type=str(file_record.get("tipoDocumentoNome") or file_record.get("tipo") or ""),
        sequence=sequence,
        url=str(file_record.get("url") or ""),
        uri=str(file_record.get("uri") or ""),
        published_at=str(file_record.get("dataPublicacaoPncp") or ""),
        raw=file_record,
    )


def safe_document_filename(
    title: str,
    *,
    sequence: int | None = None,
    default_extension: str = "",
) -> str:
    """Return a filesystem-safe filename for a PNCP document."""

    clean_title = "".join(
        char if char.isalnum() or char in {"-", "_", "."} else "_"
        for char in str(title or "").strip()
    ).strip("._")
    compact_title = "_".join(part for part in clean_title.split("_") if part)
    name = compact_title or "documento"

    if sequence is not None:
        name = f"{sequence:03d}_{name}"

    extension = default_extension if default_extension.startswith(".") else f".{default_extension}"
    if extension != "." and extension and not name.lower().endswith(extension.lower()):
        name = f"{name}{extension}"
    return name


def download_document_reference(
    reference: PncpDocumentReference,
    *,
    output_dir: Path,
    timeout: int = 60,
    filename: str | None = None,
) -> PncpDownloadedDocument:
    """Download one PNCP document reference to a local directory."""

    source_url = reference.url or reference.uri
    if not source_url:
        raise ValueError("Document reference has no URL or URI to download.")

    output_dir.mkdir(parents=True, exist_ok=True)
    request = Request(source_url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - public PNCP URL.
        content = response.read()
        content_type = response.headers.get("Content-Type", "")

    output_name = filename or safe_document_filename(
        reference.title or reference.document_type,
        sequence=reference.sequence,
        default_extension=_extension_from_response(content_type, content),
    )
    output_path = output_dir / output_name
    output_path.write_bytes(content)

    return PncpDownloadedDocument(
        source=reference.source,
        resource_type=reference.resource_type,
        resource_id=reference.resource_id,
        url=source_url,
        local_path=output_path.as_posix(),
        content_type=content_type,
        bytes_written=len(content),
        downloaded_at=datetime.now(timezone.utc).isoformat(),
        reference=reference,
    )


def document_references_from_pncp_files(
    files: list[dict[str, Any]],
    *,
    resource_type: str,
    resource_id: str,
    source: str = "pncp",
) -> list[PncpDocumentReference]:
    """Build document references from a list of PNCP file records."""

    return [
        document_reference_from_pncp_file(
            file_record,
            resource_type=resource_type,
            resource_id=resource_id,
            source=source,
        )
        for file_record in files
        if isinstance(file_record, dict)
    ]


def contract_file_references(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
    timeout: int = 30,
) -> list[PncpDocumentReference]:
    """Fetch contract file metadata and return standardized references."""

    from sherlock_holmes.pncp.contratos import list_contrato_arquivos
    from sherlock_holmes.pncp.ids import resolve_pncp_contract_id

    resolved = resolve_pncp_contract_id(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    result = list_contrato_arquivos(
        orgao_cnpj=resolved.orgao_cnpj,
        ano=resolved.ano,
        sequencial=resolved.sequencial,
        timeout=timeout,
    )
    files = result.payload if isinstance(result.payload, list) else []
    return document_references_from_pncp_files(
        files,
        resource_type="contract",
        resource_id=_resource_id(resolved.orgao_cnpj, resolved.ano, resolved.sequencial),
    )


def procurement_file_references(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
    timeout: int = 30,
) -> list[PncpDocumentReference]:
    """Fetch procurement file metadata and return standardized references."""

    from sherlock_holmes.pncp.ids import resolve_pncp_contract_id
    from sherlock_holmes.pncp.licitacoes import list_licitacao_arquivos

    resolved = resolve_pncp_contract_id(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    result = list_licitacao_arquivos(
        orgao_cnpj=resolved.orgao_cnpj,
        ano=resolved.ano,
        sequencial=resolved.sequencial,
        timeout=timeout,
    )
    files = result.payload if isinstance(result.payload, list) else []
    return document_references_from_pncp_files(
        files,
        resource_type="procurement",
        resource_id=_resource_id(resolved.orgao_cnpj, resolved.ano, resolved.sequencial),
    )


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _resource_id(orgao_cnpj: str, ano: int, sequencial: int) -> str:
    return f"{orgao_cnpj}/{ano}/{sequencial}"


def _extension_from_content_type(content_type: str) -> str:
    lowered = content_type.lower()
    if "pdf" in lowered:
        return ".pdf"
    if "zip" in lowered:
        return ".zip"
    if "json" in lowered:
        return ".json"
    if "html" in lowered:
        return ".html"
    if "text" in lowered:
        return ".txt"
    return ""


def _extension_from_response(content_type: str, content: bytes) -> str:
    extension = _extension_from_content_type(content_type)
    if extension:
        return extension
    if content.startswith(b"%PDF"):
        return ".pdf"
    if content.startswith(b"PK\x03\x04"):
        return ".zip"
    return ""
