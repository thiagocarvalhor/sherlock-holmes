"""Compatibility wrapper for PNCP domain identifiers."""

from sherlock_holmes.domain.value_objects import (
    NUMERO_CONTROLE_PNCP_RE,
    PncpResourceId,
    compact_digits,
    normalize_cnpj,
    parse_numero_controle_pncp,
    resolve_pncp_contract_id,
)

__all__ = [
    "NUMERO_CONTROLE_PNCP_RE",
    "PncpResourceId",
    "compact_digits",
    "normalize_cnpj",
    "parse_numero_controle_pncp",
    "resolve_pncp_contract_id",
]
