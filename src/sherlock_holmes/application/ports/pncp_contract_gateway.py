"""Port for searching PNCP contract candidates."""

from __future__ import annotations

from datetime import date
from typing import Any, Protocol, runtime_checkable


class PncpContractSearchResult(Protocol):
    """Result returned by a PNCP contract search gateway."""

    url: str
    payload: Any


@runtime_checkable
class PncpContractGateway(Protocol):
    """Search contracts published by PNCP in a date window."""

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
    ) -> PncpContractSearchResult:
        """Return matching PNCP contracts and the query URL."""
