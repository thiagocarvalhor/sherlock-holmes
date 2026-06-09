"""Enrich CNPJ data through an application gateway."""

from __future__ import annotations

from sherlock_holmes.application.ports import CnpjEnrichmentGateway, CnpjEnrichmentRecord


def enrich_cnpj(
    cnpj: str,
    *,
    gateway: CnpjEnrichmentGateway,
    timeout: int = 30,
) -> CnpjEnrichmentRecord:
    """Fetch normalized CNPJ enrichment data."""

    return gateway(cnpj, timeout=timeout)


__all__ = ["enrich_cnpj"]
