"""Enrich CNPJ data through an application gateway."""

from __future__ import annotations

from sherlock_holmes.application.ports import CnpjEnrichmentGateway, CnpjEnrichmentRecord
from sherlock_holmes.enrichment import fetch_cnpj


def enrich_cnpj(
    cnpj: str,
    *,
    gateway: CnpjEnrichmentGateway = fetch_cnpj,
    timeout: int = 30,
) -> CnpjEnrichmentRecord:
    """Fetch normalized CNPJ enrichment data."""

    return gateway(cnpj, timeout=timeout)


__all__ = ["enrich_cnpj"]
