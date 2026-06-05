"""Helpers for PNCP public API exploration."""

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
    "PncpResourceId",
    "compact_digits",
    "default_date_range",
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
    "resolve_pncp_contract_id",
    "search_contratos",
    "search_contratos_url",
    "search_licitacoes",
    "search_licitacoes_url",
    "validate_pncp_date_range",
]
