"""List official documents for one contract through an application gateway."""

from __future__ import annotations

from sherlock_holmes.application.ports import DocumentGateway, DocumentListResult


def list_contract_documents(
    cnpj_orgao: str,
    ano_contrato: int,
    sequencial_contrato: int,
    *,
    gateway: DocumentGateway,
    timeout: int = 30,
) -> DocumentListResult:
    """Fetch official document metadata for one contract."""

    return gateway(
        cnpj_orgao,
        ano_contrato,
        sequencial_contrato,
        timeout=timeout,
    )


__all__ = ["list_contract_documents"]
