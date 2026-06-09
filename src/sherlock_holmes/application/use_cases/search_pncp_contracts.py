"""Search PNCP contract candidates through an application gateway."""

from __future__ import annotations

from datetime import date

from sherlock_holmes.application.ports import PncpContractGateway, PncpContractSearchResult


def search_pncp_contracts(
    *,
    start_date: date,
    end_date: date,
    cnpj_orgao: str,
    gateway: PncpContractGateway,
    codigo_unidade: str = "",
    page_size: int = 500,
    max_pages: int = 20,
    timeout: int = 30,
) -> PncpContractSearchResult:
    """Fetch PNCP contract candidates using the configured gateway."""

    return gateway(
        start_date=start_date,
        end_date=end_date,
        cnpj_orgao=cnpj_orgao,
        codigo_unidade=codigo_unidade,
        page_size=page_size,
        max_pages=max_pages,
        timeout=timeout,
    )


__all__ = ["search_pncp_contracts"]
