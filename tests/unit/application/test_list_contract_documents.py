"""Tests for contract document listing use case and PNCP adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sherlock_holmes.adapters.outbound.pncp import PncpDocumentGateway
from sherlock_holmes.adapters.outbound.pncp.client import PncpRequestResult
from sherlock_holmes.application.ports import DocumentGateway
from sherlock_holmes.application.use_cases import list_contract_documents


@dataclass(frozen=True)
class FakeDocumentResult:
    url: str
    payload: Any


class FakeDocumentGateway:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int, int, int]] = []

    def __call__(
        self,
        cnpj_orgao: str,
        ano_contrato: int,
        sequencial_contrato: int,
        *,
        timeout: int = 30,
    ) -> FakeDocumentResult:
        self.calls.append((cnpj_orgao, ano_contrato, sequencial_contrato, timeout))
        return FakeDocumentResult(
            url=f"https://example.test/{cnpj_orgao}/{ano_contrato}/{sequencial_contrato}",
            payload=[{"sequencialDocumento": 1, "titulo": "Contrato"}],
        )


def test_list_contract_documents_uses_injected_gateway():
    gateway = FakeDocumentGateway()

    result = list_contract_documents(
        "39485438000142",
        2025,
        19,
        gateway=gateway,
        timeout=7,
    )

    assert result.url == "https://example.test/39485438000142/2025/19"
    assert result.payload == [{"sequencialDocumento": 1, "titulo": "Contrato"}]
    assert gateway.calls == [("39485438000142", 2025, 19, 7)]


def test_pncp_document_gateway_satisfies_document_port():
    assert isinstance(PncpDocumentGateway(), DocumentGateway)


def test_pncp_document_gateway_delegates_to_pncp_client(monkeypatch):
    calls = []

    def fake_fetch_contract_files(cnpj_orgao: str, ano: int, sequencial: int, *, timeout: int = 30):
        calls.append((cnpj_orgao, ano, sequencial, timeout))
        return PncpRequestResult(url="https://pncp.test/files", payload=[])

    monkeypatch.setattr(
        "sherlock_holmes.adapters.outbound.pncp.document_gateway.fetch_contract_files",
        fake_fetch_contract_files,
    )

    result = PncpDocumentGateway()("39485438000142", 2025, 19, timeout=5)

    assert result.url == "https://pncp.test/files"
    assert result.payload == []
    assert calls == [("39485438000142", 2025, 19, 5)]
