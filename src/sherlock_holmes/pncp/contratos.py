"""Contract-oriented PNCP API helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from sherlock_holmes.pncp.dates import format_pncp_date, validate_pncp_date_range
from sherlock_holmes.pncp.ids import compact_digits, resolve_pncp_contract_id


CONSULTA_BASE_URL = "https://pncp.gov.br/api/consulta"
PNCP_BASE_URL = "https://pncp.gov.br/api/pncp"
PNCP_FILE_BASE_URL = "https://pncp.gov.br/pncp-api"


@dataclass(frozen=True)
class PncpRequestResult:
    """Response body with the URL that generated it."""

    url: str
    payload: Any


def search_contratos_url(
    *,
    data_inicial: date | datetime | str,
    data_final: date | datetime | str,
    pagina: int,
    tamanho_pagina: int,
    cnpj_orgao: str = "",
    cnpj_fornecedor: str = "",
    codigo_unidade: str = "",
) -> str:
    """Build the contract search URL."""

    from sherlock_holmes.pncp.client import build_url

    date_range = validate_pncp_date_range(data_inicial, data_final)
    return build_url(
        CONSULTA_BASE_URL,
        "/v1/contratos",
        {
            "dataInicial": date_range.data_inicial,
            "dataFinal": date_range.data_final,
            "cnpjOrgao": compact_digits(cnpj_orgao),
            "cnpjFornecedor": compact_digits(cnpj_fornecedor),
            "codigoUnidadeAdministrativa": codigo_unidade.strip(),
            "pagina": pagina,
            "tamanhoPagina": tamanho_pagina,
        },
    )


def search_contratos(
    *,
    data_inicial: date | datetime | str,
    data_final: date | datetime | str,
    cnpj_orgao: str = "",
    cnpj_fornecedor: str = "",
    codigo_unidade: str = "",
    tamanho_pagina: int = 500,
    max_pages: int = 20,
    timeout: int = 30,
) -> PncpRequestResult:
    """Fetch contract search results from PNCP, merging pages."""

    from sherlock_holmes.pncp.client import PncpApiError, request_json

    records: list[dict[str, Any]] = []
    first_url = ""
    last_payload: dict[str, Any] = {}

    for page in range(1, max_pages + 1):
        url = search_contratos_url(
            data_inicial=data_inicial,
            data_final=data_final,
            cnpj_orgao=cnpj_orgao,
            cnpj_fornecedor=cnpj_fornecedor,
            codigo_unidade=codigo_unidade,
            pagina=page,
            tamanho_pagina=tamanho_pagina,
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


def get_contrato_url(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
) -> str:
    """Build a direct contract detail URL."""

    from sherlock_holmes.pncp.client import build_url

    resolved = resolve_pncp_contract_id(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return build_url(
        PNCP_BASE_URL,
        f"/v1/orgaos/{resolved.orgao_cnpj}/contratos/{resolved.ano}/{resolved.sequencial}",
    )


def get_contrato(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
    timeout: int = 30,
) -> PncpRequestResult:
    """Fetch contract details from PNCP."""

    from sherlock_holmes.pncp.client import request_json

    url = get_contrato_url(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return PncpRequestResult(url=url, payload=request_json(url, timeout=timeout))


def list_contrato_arquivos_url(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
) -> str:
    """Build a contract files listing URL."""

    from sherlock_holmes.pncp.client import build_url

    resolved = resolve_pncp_contract_id(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return build_url(
        PNCP_BASE_URL,
        (
            f"/v1/orgaos/{resolved.orgao_cnpj}/contratos/"
            f"{resolved.ano}/{resolved.sequencial}/arquivos"
        ),
    )


def list_contrato_arquivos(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
    timeout: int = 30,
) -> PncpRequestResult:
    """Fetch file metadata for one contract."""

    from sherlock_holmes.pncp.client import request_json

    url = list_contrato_arquivos_url(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return PncpRequestResult(url=url, payload=request_json(url, timeout=timeout))


def contrato_arquivo_download_url(
    *,
    sequencial_documento: int,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
) -> str:
    """Build a direct file download URL for a contract attachment."""

    from sherlock_holmes.pncp.client import build_url

    resolved = resolve_pncp_contract_id(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return build_url(
        PNCP_FILE_BASE_URL,
        (
            f"/v1/orgaos/{resolved.orgao_cnpj}/contratos/"
            f"{resolved.ano}/{resolved.sequencial}/arquivos/{sequencial_documento}"
        ),
    )


def contract_publication_url(
    *,
    start_date: date,
    end_date: date,
    cnpj_orgao: str,
    page: int,
    page_size: int,
    codigo_unidade: str = "",
) -> str:
    """Compatibility wrapper for the previous contract search URL helper."""

    return search_contratos_url(
        data_inicial=format_pncp_date(start_date),
        data_final=format_pncp_date(end_date),
        cnpj_orgao=cnpj_orgao,
        codigo_unidade=codigo_unidade,
        pagina=page,
        tamanho_pagina=page_size,
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
    """Compatibility wrapper for the previous paged contract search."""

    return search_contratos(
        data_inicial=start_date,
        data_final=end_date,
        cnpj_orgao=cnpj_orgao,
        codigo_unidade=codigo_unidade,
        tamanho_pagina=page_size,
        max_pages=max_pages,
        timeout=timeout,
    )
