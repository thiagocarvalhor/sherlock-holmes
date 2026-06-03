"""Small client for PNCP public APIs used by the Streamlit explorer."""

from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass
from datetime import date
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


CONSULTA_BASE_URL = "https://pncp.gov.br/api/consulta"
PNCP_BASE_URL = "https://pncp.gov.br/api/pncp"
PNCP_FILE_BASE_URL = "https://pncp.gov.br/pncp-api"
USER_AGENT = "sherlock-holmes-pncp-explorer/0.1"


@dataclass(frozen=True)
class PncpRequestResult:
    """Response body with the URL that generated it."""

    url: str
    payload: Any


class PncpApiError(RuntimeError):
    """Raised when the PNCP API returns a non-success response."""


def compact_digits(value: str | None) -> str:
    """Return only digits from a string."""

    return "".join(char for char in str(value or "") if char.isdigit())


def normalize_text(value: Any) -> str:
    """Normalize text for accent-insensitive matching."""

    normalized = unicodedata.normalize("NFKD", str(value or ""))
    without_accents = "".join(char for char in normalized if not unicodedata.combining(char))
    return " ".join(without_accents.casefold().split())


def request_json(url: str, timeout: int = 30) -> Any:
    """Request JSON from the PNCP API."""

    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed public API URL.
            body = response.read()
            return json.loads(body.decode("utf-8")) if body else None
    except HTTPError as exc:
        body = exc.read()
        message = body.decode("utf-8", errors="replace") if body else str(exc)
        raise PncpApiError(f"PNCP HTTP {exc.code}: {message}") from exc


def build_url(base_url: str, endpoint: str, params: dict[str, str | int | None] | None = None) -> str:
    """Build a PNCP URL and skip empty query params."""

    cleaned_params = {
        key: value
        for key, value in (params or {}).items()
        if value is not None and str(value).strip() != ""
    }
    query = f"?{urlencode(cleaned_params)}" if cleaned_params else ""
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}{query}"


def contract_publication_url(
    *,
    start_date: date,
    end_date: date,
    cnpj_orgao: str,
    page: int,
    page_size: int,
    codigo_unidade: str = "",
) -> str:
    """Build the contract publication search URL."""

    return build_url(
        CONSULTA_BASE_URL,
        "/v1/contratos",
        {
            "dataInicial": start_date.strftime("%Y%m%d"),
            "dataFinal": end_date.strftime("%Y%m%d"),
            "cnpjOrgao": compact_digits(cnpj_orgao),
            "codigoUnidadeAdministrativa": codigo_unidade.strip(),
            "pagina": page,
            "tamanhoPagina": page_size,
        },
    )


def fetch_contracts_by_publication(
    *,
    start_date: date,
    end_date: date,
    cnpj_orgao: str,
    codigo_unidade: str = "",
    page_size: int = 500,
    max_pages: int = 20,
    timeout: int = 30,
) -> PncpRequestResult:
    """Fetch all pages from the contract publication endpoint."""

    records: list[dict[str, Any]] = []
    first_url = ""
    last_payload: dict[str, Any] = {}

    for page in range(1, max_pages + 1):
        url = contract_publication_url(
            start_date=start_date,
            end_date=end_date,
            cnpj_orgao=cnpj_orgao,
            codigo_unidade=codigo_unidade,
            page=page,
            page_size=page_size,
        )
        if not first_url:
            first_url = url
        payload = request_json(url, timeout=timeout)
        if not isinstance(payload, dict):
            raise PncpApiError("Resposta inesperada da API de contratos.")

        last_payload = payload
        page_records = [item for item in payload.get("data", []) if isinstance(item, dict)]
        records.extend(page_records)

        total_pages = int(payload.get("totalPaginas") or page)
        if page >= total_pages:
            break

    merged_payload = {
        "data": records,
        "totalRegistros": len(records),
        "totalPaginas": last_payload.get("totalPaginas", 0),
        "numeroPagina": last_payload.get("numeroPagina", 0),
        "paginasRestantes": last_payload.get("paginasRestantes", 0),
    }
    return PncpRequestResult(url=first_url, payload=merged_payload)


def contract_detail_url(cnpj_orgao: str, ano_contrato: int, sequencial_contrato: int) -> str:
    """Build a direct contract detail URL."""

    return build_url(
        PNCP_BASE_URL,
        f"/v1/orgaos/{compact_digits(cnpj_orgao)}/contratos/{ano_contrato}/{sequencial_contrato}",
    )


def contract_files_url(cnpj_orgao: str, ano_contrato: int, sequencial_contrato: int) -> str:
    """Build a contract files listing URL."""

    return build_url(
        PNCP_BASE_URL,
        f"/v1/orgaos/{compact_digits(cnpj_orgao)}/contratos/{ano_contrato}/{sequencial_contrato}/arquivos",
    )


def contract_file_download_url(
    cnpj_orgao: str,
    ano_contrato: int,
    sequencial_contrato: int,
    sequencial_documento: int,
) -> str:
    """Build the direct file download URL."""

    return build_url(
        PNCP_FILE_BASE_URL,
        (
            f"/v1/orgaos/{compact_digits(cnpj_orgao)}/contratos/"
            f"{ano_contrato}/{sequencial_contrato}/arquivos/{sequencial_documento}"
        ),
    )


def fetch_contract_files(
    cnpj_orgao: str,
    ano_contrato: int,
    sequencial_contrato: int,
    *,
    timeout: int = 30,
) -> PncpRequestResult:
    """Fetch file metadata for one contract."""

    url = contract_files_url(cnpj_orgao, ano_contrato, sequencial_contrato)
    return PncpRequestResult(url=url, payload=request_json(url, timeout=timeout))


def filter_records_by_terms(records: list[dict[str, Any]], terms: list[str]) -> list[dict[str, Any]]:
    """Filter records by terms contained in the contract object."""

    normalized_terms = [normalize_text(term) for term in terms if normalize_text(term)]
    if not normalized_terms:
        return records
    filtered = []
    for record in records:
        target = normalize_text(record.get("objetoContrato", ""))
        if any(term in target for term in normalized_terms):
            filtered.append(record)
    return filtered

