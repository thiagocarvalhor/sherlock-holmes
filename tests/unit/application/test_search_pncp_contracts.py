"""Tests for PNCP contract search use case and adapter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from sherlock_holmes.adapters.outbound.pncp.client import PncpRequestResult
from sherlock_holmes.adapters.outbound.pncp.contract_gateway import PncpContractSearchGateway
from sherlock_holmes.application.use_cases import search_pncp_contracts


@dataclass
class FakeContractGateway:
    """Capture arguments passed by the PNCP search use case."""

    calls: list[dict[str, Any]]

    def __call__(
        self,
        *,
        start_date: date,
        end_date: date,
        cnpj_orgao: str,
        codigo_unidade: str = "",
        page_size: int = 500,
        max_pages: int = 20,
        timeout: int = 30,
    ) -> PncpRequestResult:
        self.calls.append(
            {
                "start_date": start_date,
                "end_date": end_date,
                "cnpj_orgao": cnpj_orgao,
                "codigo_unidade": codigo_unidade,
                "page_size": page_size,
                "max_pages": max_pages,
                "timeout": timeout,
            }
        )
        return PncpRequestResult(url="https://example.test/contracts", payload={"data": []})


def test_search_pncp_contracts_delegates_to_gateway():
    gateway = FakeContractGateway(calls=[])

    result = search_pncp_contracts(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        cnpj_orgao="39.485.438/0001-42",
        codigo_unidade="925004",
        page_size=100,
        max_pages=3,
        timeout=12,
        gateway=gateway,
    )

    assert result.url == "https://example.test/contracts"
    assert gateway.calls == [
        {
            "start_date": date(2025, 1, 1),
            "end_date": date(2025, 12, 31),
            "cnpj_orgao": "39.485.438/0001-42",
            "codigo_unidade": "925004",
            "page_size": 100,
            "max_pages": 3,
            "timeout": 12,
        }
    ]


def test_pncp_contract_search_gateway_delegates_to_client(monkeypatch):
    calls: list[dict[str, Any]] = []

    def fake_fetch_contracts_by_publication(**kwargs: Any) -> PncpRequestResult:
        calls.append(kwargs)
        return PncpRequestResult(url="https://example.test/pncp", payload={"data": [{"id": 1}]})

    monkeypatch.setattr(
        "sherlock_holmes.adapters.outbound.pncp.contract_gateway.fetch_contracts_by_publication",
        fake_fetch_contracts_by_publication,
    )

    result = PncpContractSearchGateway()(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        cnpj_orgao="39485438000142",
        codigo_unidade="",
        page_size=500,
        max_pages=20,
        timeout=30,
    )

    assert result.payload == {"data": [{"id": 1}]}
    assert calls == [
        {
            "start_date": date(2025, 1, 1),
            "end_date": date(2025, 12, 31),
            "cnpj_orgao": "39485438000142",
            "codigo_unidade": "",
            "page_size": 500,
            "max_pages": 20,
            "timeout": 30,
        }
    ]
