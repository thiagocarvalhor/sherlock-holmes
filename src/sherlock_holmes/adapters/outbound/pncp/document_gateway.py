"""PNCP adapter for official contract document listings."""

from __future__ import annotations

from sherlock_holmes.pncp.client import PncpRequestResult, fetch_contract_files


class PncpDocumentGateway:
    """Fetch official document metadata from PNCP."""

    def __call__(
        self,
        cnpj_orgao: str,
        ano_contrato: int,
        sequencial_contrato: int,
        *,
        timeout: int = 30,
    ) -> PncpRequestResult:
        """Return official PNCP files for one contract."""

        return fetch_contract_files(
            cnpj_orgao,
            ano_contrato,
            sequencial_contrato,
            timeout=timeout,
        )


__all__ = ["PncpDocumentGateway"]
