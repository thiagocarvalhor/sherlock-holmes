"""Procurement-oriented PNCP API helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from sherlock_holmes.pncp.dates import validate_pncp_date_range
from sherlock_holmes.pncp.ids import compact_digits, resolve_pncp_contract_id


CONSULTA_BASE_URL = "https://pncp.gov.br/api/consulta"
PNCP_BASE_URL = "https://pncp.gov.br/api/pncp"


@dataclass(frozen=True)
class PncpRequestResult:
    """Response body with the URL that generated it."""

    url: str
    payload: Any


def search_licitacoes_url(
    *,
    data_inicial: date | datetime | str,
    data_final: date | datetime | str,
    codigo_modalidade_contratacao: int,
    pagina: int,
    tamanho_pagina: int,
    uf: str = "",
    codigo_municipio_ibge: str = "",
    cnpj_orgao: str = "",
) -> str:
    """Build the procurement publication search URL."""

    from sherlock_holmes.pncp.client import build_url

    date_range = validate_pncp_date_range(data_inicial, data_final)
    return build_url(
        CONSULTA_BASE_URL,
        "/v1/contratacoes/publicacao",
        {
            "dataInicial": date_range.data_inicial,
            "dataFinal": date_range.data_final,
            "codigoModalidadeContratacao": codigo_modalidade_contratacao,
            "uf": uf.strip().upper(),
            "codigoMunicipioIbge": codigo_municipio_ibge.strip(),
            "cnpj": compact_digits(cnpj_orgao),
            "pagina": pagina,
            "tamanhoPagina": tamanho_pagina,
        },
    )


def search_licitacoes(
    *,
    data_inicial: date | datetime | str,
    data_final: date | datetime | str,
    codigo_modalidade_contratacao: int,
    uf: str = "",
    codigo_municipio_ibge: str = "",
    cnpj_orgao: str = "",
    tamanho_pagina: int = 50,
    max_pages: int = 3,
    timeout: int = 30,
) -> PncpRequestResult:
    """Fetch procurement publication results from PNCP, merging pages."""

    from sherlock_holmes.pncp.client import PncpApiError, request_json

    records: list[dict[str, Any]] = []
    first_url = ""
    last_payload: dict[str, Any] = {}

    for page in range(1, max_pages + 1):
        url = search_licitacoes_url(
            data_inicial=data_inicial,
            data_final=data_final,
            codigo_modalidade_contratacao=codigo_modalidade_contratacao,
            uf=uf,
            codigo_municipio_ibge=codigo_municipio_ibge,
            cnpj_orgao=cnpj_orgao,
            pagina=page,
            tamanho_pagina=tamanho_pagina,
        )
        if not first_url:
            first_url = url

        payload = request_json(url, timeout=timeout)
        if not isinstance(payload, dict):
            raise PncpApiError("Resposta inesperada da API de contratacoes.")

        last_payload = payload
        page_records = [item for item in payload.get("data", []) if isinstance(item, dict)]
        records.extend(page_records)

        total_pages = int(payload.get("totalPaginas") or page)
        if page >= total_pages:
            break

    merged_payload = {
        "data": records,
        "totalRegistros": last_payload.get("totalRegistros", len(records)),
        "totalPaginas": last_payload.get("totalPaginas", 0),
        "numeroPagina": last_payload.get("numeroPagina", 0),
        "paginasRestantes": last_payload.get("paginasRestantes", 0),
    }
    return PncpRequestResult(url=first_url, payload=merged_payload)


def get_licitacao_url(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
) -> str:
    """Build a procurement detail URL."""

    from sherlock_holmes.pncp.client import build_url

    resolved = resolve_pncp_contract_id(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return build_url(
        CONSULTA_BASE_URL,
        f"/v1/orgaos/{resolved.orgao_cnpj}/compras/{resolved.ano}/{resolved.sequencial}",
    )


def get_licitacao(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
    timeout: int = 30,
) -> PncpRequestResult:
    """Fetch procurement details from PNCP."""

    from sherlock_holmes.pncp.client import request_json

    url = get_licitacao_url(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return PncpRequestResult(url=url, payload=request_json(url, timeout=timeout))


def list_licitacao_itens_url(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
) -> str:
    """Build a procurement items listing URL."""

    from sherlock_holmes.pncp.client import build_url

    resolved = resolve_pncp_contract_id(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return build_url(
        PNCP_BASE_URL,
        f"/v1/orgaos/{resolved.orgao_cnpj}/compras/{resolved.ano}/{resolved.sequencial}/itens",
    )


def list_licitacao_itens(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
    timeout: int = 30,
) -> PncpRequestResult:
    """Fetch procurement items from PNCP."""

    from sherlock_holmes.pncp.client import request_json

    url = list_licitacao_itens_url(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return PncpRequestResult(url=url, payload=request_json(url, timeout=timeout))


def list_licitacao_arquivos_url(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
) -> str:
    """Build a procurement files listing URL."""

    from sherlock_holmes.pncp.client import build_url

    resolved = resolve_pncp_contract_id(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return build_url(
        PNCP_BASE_URL,
        f"/v1/orgaos/{resolved.orgao_cnpj}/compras/{resolved.ano}/{resolved.sequencial}/arquivos",
    )


def list_licitacao_arquivos(
    *,
    numero_controle_pncp: str | None = None,
    orgao_cnpj: str | None = None,
    ano: int | None = None,
    sequencial: int | None = None,
    timeout: int = 30,
) -> PncpRequestResult:
    """Fetch procurement file metadata from PNCP."""

    from sherlock_holmes.pncp.client import request_json

    url = list_licitacao_arquivos_url(
        numero_controle_pncp=numero_controle_pncp,
        orgao_cnpj=orgao_cnpj,
        ano=ano,
        sequencial=sequencial,
    )
    return PncpRequestResult(url=url, payload=request_json(url, timeout=timeout))
