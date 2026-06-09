"""Immutable domain values such as identifiers and normalized fields."""

from sherlock_holmes.domain.value_objects.cnpj import compact_digits, normalize_cnpj
from sherlock_holmes.domain.value_objects.pncp_id import (
    NUMERO_CONTROLE_PNCP_RE,
    PncpResourceId,
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
