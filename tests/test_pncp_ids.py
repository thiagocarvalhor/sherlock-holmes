"""Tests for PNCP identifier and CNPJ helpers."""

from __future__ import annotations

import pytest

from sherlock_holmes.pncp.ids import (
    PncpResourceId,
    compact_digits,
    normalize_cnpj,
    parse_numero_controle_pncp,
    resolve_pncp_contract_id,
)


def test_compact_digits_strips_mask():
    assert compact_digits("39.485.438/0001-42") == "39485438000142"
    assert compact_digits(None) == ""


def test_normalize_cnpj_accepts_masked():
    assert normalize_cnpj("39.485.438/0001-42") == "39485438000142"


def test_normalize_cnpj_rejects_wrong_length():
    with pytest.raises(ValueError):
        normalize_cnpj("123")


def test_parse_numero_controle_pncp_valid():
    resource = parse_numero_controle_pncp("39485438000142-2-000019/2025")
    assert resource == PncpResourceId(orgao_cnpj="39485438000142", ano=2025, sequencial=19)


@pytest.mark.parametrize("value", ["", "invalido", "39485438000142-2-19", "abc-2-000019/2025"])
def test_parse_numero_controle_pncp_invalid(value):
    with pytest.raises(ValueError):
        parse_numero_controle_pncp(value)


def test_resolve_from_control_number():
    resource = resolve_pncp_contract_id(numero_controle_pncp="39485438000142-2-000003/2025")
    assert resource.ano == 2025
    assert resource.sequencial == 3


def test_resolve_from_explicit_parts():
    resource = resolve_pncp_contract_id(orgao_cnpj="39.485.438/0001-42", ano=2025, sequencial=7)
    assert resource.orgao_cnpj == "39485438000142"
    assert resource.sequencial == 7


def test_resolve_requires_complete_parts():
    with pytest.raises(ValueError):
        resolve_pncp_contract_id(orgao_cnpj="39485438000142", ano=2025)
