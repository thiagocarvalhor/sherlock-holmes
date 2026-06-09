"""BrasilAPI adapter for CNPJ enrichment."""

from __future__ import annotations

from sherlock_holmes.adapters.outbound.brasilapi.client import BrasilApiCnpjRecord, fetch_cnpj


class BrasilApiCnpjGateway:
    """Fetch normalized CNPJ records from BrasilAPI."""

    def __call__(self, cnpj: str, *, timeout: int = 30) -> BrasilApiCnpjRecord:
        """Return normalized BrasilAPI CNPJ data."""

        return fetch_cnpj(cnpj, timeout=timeout)


__all__ = ["BrasilApiCnpjGateway"]
