"""Helpers for PNCP public API exploration."""

from sherlock_holmes.pncp.arquivos import (
    PncpDocumentReference,
    contract_file_references,
    document_reference_from_pncp_file,
    document_references_from_pncp_files,
    procurement_file_references,
)
from sherlock_holmes.pncp.contratos import (
    get_contrato,
    get_contrato_url,
    list_contrato_arquivos,
    list_contrato_arquivos_url,
    search_contratos,
    search_contratos_url,
)
from sherlock_holmes.pncp.dates import (
    PNCP_MAX_DATE_RANGE_DAYS,
    default_date_range,
    format_pncp_date,
    parse_pncp_date,
    validate_pncp_date_range,
)
from sherlock_holmes.pncp.ids import (
    PncpResourceId,
    compact_digits,
    normalize_cnpj,
    parse_numero_controle_pncp,
    resolve_pncp_contract_id,
)
from sherlock_holmes.pncp.licitacoes import (
    get_licitacao,
    get_licitacao_url,
    list_licitacao_arquivos,
    list_licitacao_arquivos_url,
    list_licitacao_itens,
    list_licitacao_itens_url,
    search_licitacoes,
    search_licitacoes_url,
)


__all__ = [
    "PNCP_MAX_DATE_RANGE_DAYS",
    "PncpDocumentReference",
    "PncpResourceId",
    "compact_digits",
    "contract_file_references",
    "default_date_range",
    "document_reference_from_pncp_file",
    "document_references_from_pncp_files",
    "format_pncp_date",
    "get_contrato",
    "get_contrato_url",
    "get_licitacao",
    "get_licitacao_url",
    "list_contrato_arquivos",
    "list_contrato_arquivos_url",
    "list_licitacao_arquivos",
    "list_licitacao_arquivos_url",
    "list_licitacao_itens",
    "list_licitacao_itens_url",
    "normalize_cnpj",
    "parse_numero_controle_pncp",
    "parse_pncp_date",
    "procurement_file_references",
    "resolve_pncp_contract_id",
    "search_contratos",
    "search_contratos_url",
    "search_licitacoes",
    "search_licitacoes_url",
    "validate_pncp_date_range",
]
