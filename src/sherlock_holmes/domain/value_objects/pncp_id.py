"""PNCP resource identifiers."""

from __future__ import annotations

import re
from dataclasses import dataclass

from sherlock_holmes.domain.value_objects.cnpj import normalize_cnpj

NUMERO_CONTROLE_PNCP_RE = re.compile(r"^(\d{14})-(\d+)-(\d+)/(\d{4})$")


@dataclass(frozen=True)
class PncpResourceId:
    """Resolved PNCP resource identifier."""

    orgao_cnpj: str
    ano: int
    sequencial: int


def parse_numero_controle_pncp(numero_controle_pncp: str) -> PncpResourceId:
    """Parse a PNCP control number into agency CNPJ, year, and sequence."""

    match = NUMERO_CONTROLE_PNCP_RE.match(str(numero_controle_pncp or "").strip())
    if not match:
        raise ValueError("Invalid numeroControlePNCP format. Expected NNNNNNNNNNNNNN-D-NNNNNN/YYYY.")

    cnpj, _kind, sequencial, ano = match.groups()
    return PncpResourceId(
        orgao_cnpj=cnpj,
        ano=int(ano),
        sequencial=int(sequencial),
    )


def resolve_pncp_contract_id(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
) -> PncpResourceId:
    """Resolve a contract identifier from numeroControlePNCP or explicit parts."""

    if numero_controle_pncp:
        return parse_numero_controle_pncp(numero_controle_pncp)

    if orgao_cnpj is None or ano is None or sequencial is None:
        raise ValueError("Provide either numero_controle_pncp or all of orgao_cnpj, ano, and sequencial.")

    return PncpResourceId(
        orgao_cnpj=normalize_cnpj(orgao_cnpj),
        ano=int(ano),
        sequencial=int(sequencial),
    )


__all__ = [
    "NUMERO_CONTROLE_PNCP_RE",
    "PncpResourceId",
    "parse_numero_controle_pncp",
    "resolve_pncp_contract_id",
]
