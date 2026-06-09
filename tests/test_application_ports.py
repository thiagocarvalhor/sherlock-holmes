"""Tests for application port contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from sherlock_holmes.application.ports import (
    CnpjEnrichmentGateway,
    DocumentGateway,
    PncpContractGateway,
    ReportWriter,
    ReviewStatusStore,
)


@dataclass(frozen=True)
class _GatewayResult:
    url: str
    payload: Any


class _PncpGateway:
    def __call__(
        self,
        *,
        start_date: date,
        end_date: date,
        cnpj_orgao: str,
        page_size: int = 500,
        max_pages: int = 20,
        timeout: int = 30,
    ) -> _GatewayResult:
        return _GatewayResult(
            url=f"https://example.test/{cnpj_orgao}",
            payload={"start": start_date.isoformat(), "end": end_date.isoformat()},
        )


class _CnpjGateway:
    def __call__(self, cnpj: str, *, timeout: int = 30) -> Any:
        return {"cnpj": cnpj, "timeout": timeout}


class _DocumentGateway:
    def __call__(
        self,
        cnpj_orgao: str,
        ano_contrato: int,
        sequencial_contrato: int,
        *,
        timeout: int = 30,
    ) -> _GatewayResult:
        return _GatewayResult(
            url=f"https://example.test/{cnpj_orgao}/{ano_contrato}/{sequencial_contrato}",
            payload=[],
        )


class _ReportWriter:
    def write_json(self, report: dict[str, Any], *, output_path: str | Path) -> Path:
        return Path(output_path)

    def write_markdown(self, report: dict[str, Any], *, output_path: str | Path) -> Path:
        return Path(output_path)


class _ReviewStore:
    def __init__(self) -> None:
        self.status: dict[str, str] = {}
        self.notes: dict[str, str] = {}

    def get_status(self, key: str, *, default: str = "pendente") -> str:
        return self.status.get(key, default)

    def set_status(self, key: str, status: str) -> None:
        self.status[key] = status

    def get_notes(self, key: str, *, default: str = "") -> str:
        return self.notes.get(key, default)

    def set_notes(self, key: str, notes: str) -> None:
        self.notes[key] = notes


def test_fake_adapters_satisfy_application_ports():
    assert isinstance(_PncpGateway(), PncpContractGateway)
    assert isinstance(_CnpjGateway(), CnpjEnrichmentGateway)
    assert isinstance(_DocumentGateway(), DocumentGateway)
    assert isinstance(_ReportWriter(), ReportWriter)
    assert isinstance(_ReviewStore(), ReviewStatusStore)
