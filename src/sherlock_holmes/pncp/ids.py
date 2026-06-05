"""Identifiers and CNPJ helpers for PNCP resources."""

from __future__ import annotations

import re
from dataclasses import dataclass


NUMERO_CONTROLE_PNCP_RE = re.compile(r"^(\d{14})-(\d+)-(\d+)/(\d{4})$")


@dataclass(frozen=True)
class PncpResourceId:
    """Resolved PNCP resource identifier."""

    orgao_cnpj: str
    ano: int
    sequencial: int


def compact_digits(value: str | None) -> str:
    """Return only digits from a string."""

    return "".join(char for char in str(value or "") if char.isdigit())


def normalize_cnpj(value: str | None) -> str:
    """Return a 14-digit CNPJ or raise ValueError."""

    digits = compact_digits(value)
    if len(digits) != 14:
        raise ValueError(f"Invalid CNPJ: {value!r} (expected 14 digits)")
    return digits


def parse_numero_controle_pncp(numero_controle_pncp: str) -> PncpResourceId:
    """Parse a PNCP control number into agency CNPJ, year, and sequence."""

    match = NUMERO_CONTROLE_PNCP_RE.match(str(numero_controle_pncp or "").strip())
    if not match:
        raise ValueError(
            "Invalid numeroControlePNCP format. Expected NNNNNNNNNNNNNN-D-NNNNNN/YYYY."
        )

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
        raise ValueError(
            "Provide either numero_controle_pncp or all of orgao_cnpj, ano, and sequencial."
        )

    return PncpResourceId(
        orgao_cnpj=normalize_cnpj(orgao_cnpj),
        ano=int(ano),
        sequencial=int(sequencial),
    )
