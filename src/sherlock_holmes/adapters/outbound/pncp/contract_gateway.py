"""PNCP adapter for official contract searches."""

from __future__ import annotations

from datetime import date

from sherlock_holmes.adapters.outbound.pncp.client import PncpRequestResult, fetch_contracts_by_publication


class PncpContractSearchGateway:
    """Fetch official contract candidates from PNCP."""

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
        """Return PNCP contracts published in the requested date window."""

        return fetch_contracts_by_publication(
            start_date=start_date,
            end_date=end_date,
            cnpj_orgao=cnpj_orgao,
            codigo_unidade=codigo_unidade,
            page_size=page_size,
            max_pages=max_pages,
            timeout=timeout,
        )


__all__ = ["PncpContractSearchGateway"]
