"""Port for official document providers."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


class DocumentListResult(Protocol):
    """Result returned by a document listing gateway."""

    url: str
    payload: Any


@runtime_checkable
class DocumentGateway(Protocol):
    """Fetch official documents linked to one public resource."""

    def __call__(
        self,
        cnpj_orgao: str,
        ano_contrato: int,
        sequencial_contrato: int,
        *,
        timeout: int = 30,
    ) -> DocumentListResult:
        """Return official document metadata for one contract."""
