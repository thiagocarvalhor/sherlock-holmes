"""Tests for CNPJ enrichment use case."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sherlock_holmes.adapters.outbound.brasilapi import BrasilApiCnpjGateway
from sherlock_holmes.application.use_cases import enrich_cnpj
from sherlock_holmes.enrichment import BrasilApiCnpjRecord


@dataclass(frozen=True)
class FakeCnpjRecord:
    cnpj: str
    source_url: str
    timeout: int

    def to_dict(self) -> dict[str, Any]:
        return {"cnpj": self.cnpj, "source_url": self.source_url, "timeout": self.timeout}

    def standardized(self) -> dict[str, Any]:
        return {"cnpj": self.cnpj}


def test_enrich_cnpj_uses_injected_gateway():
    calls = []

    def fake_gateway(cnpj: str, *, timeout: int = 30) -> FakeCnpjRecord:
        calls.append((cnpj, timeout))
        return FakeCnpjRecord(cnpj=cnpj, source_url=f"https://example.test/{cnpj}", timeout=timeout)

    record = enrich_cnpj("39485438000142", gateway=fake_gateway, timeout=7)

    assert record.cnpj == "39485438000142"
    assert record.source_url == "https://example.test/39485438000142"
    assert record.standardized() == {"cnpj": "39485438000142"}
    assert calls == [("39485438000142", 7)]


def test_brasilapi_cnpj_gateway_delegates_to_client(monkeypatch):
    calls: list[tuple[str, int]] = []

    def fake_fetch_cnpj(cnpj: str, *, timeout: int = 30) -> BrasilApiCnpjRecord:
        calls.append((cnpj, timeout))
        return BrasilApiCnpjRecord(
            cnpj=cnpj,
            razao_social="Municipio de Belford Roxo",
            source_url=f"https://example.test/{cnpj}",
        )

    monkeypatch.setattr(
        "sherlock_holmes.adapters.outbound.brasilapi.cnpj_gateway.fetch_cnpj",
        fake_fetch_cnpj,
    )

    record = BrasilApiCnpjGateway()("39485438000142", timeout=9)

    assert record.razao_social == "Municipio de Belford Roxo"
    assert calls == [("39485438000142", 9)]
