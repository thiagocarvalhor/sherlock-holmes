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


__all__ = [
    "PNCP_MAX_DATE_RANGE_DAYS",
    "PncpResourceId",
    "compact_digits",
    "default_date_range",
    "format_pncp_date",
    "get_contrato",
    "get_contrato_url",
    "list_contrato_arquivos",
    "list_contrato_arquivos_url",
    "normalize_cnpj",
    "parse_numero_controle_pncp",
    "parse_pncp_date",
    "resolve_pncp_contract_id",
    "search_contratos",
    "search_contratos_url",
    "validate_pncp_date_range",
]
