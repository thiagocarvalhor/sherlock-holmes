"""Port for CNPJ enrichment providers."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


class CnpjEnrichmentRecord(Protocol):
    """Normalized CNPJ enrichment record returned by an external provider."""

    cnpj: str
    source_url: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full enrichment record."""

    def standardized(self) -> dict[str, Any]:
        """Return the standardized fields used by comparison and reporting."""


@runtime_checkable
class CnpjEnrichmentGateway(Protocol):
    """Fetch normalized CNPJ enrichment data."""

    def __call__(self, cnpj: str, *, timeout: int = 30) -> CnpjEnrichmentRecord:
        """Return enrichment data for one CNPJ."""
