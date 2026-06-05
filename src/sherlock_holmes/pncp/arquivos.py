"""Document reference helpers for PNCP file metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
