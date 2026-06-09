"""PNCP data helpers, constants and cached fetchers for Streamlit pages."""

from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd
import streamlit as st

from sherlock_holmes.adapters.outbound.pncp import PncpDocumentGateway
from sherlock_holmes.application.use_cases import list_contract_documents
from sherlock_holmes.pncp.client import (
    contract_detail_url,
    contract_file_download_url,
    fetch_contracts_by_publication,
    filter_records_by_terms,
    normalize_text,
)

KEYWORD_SUGGESTIONS: dict[str, list[str]] = {
    "limpeza": [
        "limpeza urbana",
        "limpeza pública",
        "resíduos sólidos",
        "varrição",
        "coleta",
        "triagem",
        "destinação",
        "serviços indivisíveis",
    ],
    "residuos": [
        "resíduos sólidos",
        "coleta",
        "triagem",
        "recicláveis",
        "destinação",
        "ecoponto",
    ],
    "obras": [
        "obras civis",
        "pavimentação",
        "drenagem",
        "contenção",
        "engenharia",
        "reparos",
    ],
    "ti": [
        "tecnologia da informação",
        "software",
        "licenças",
        "sistema",
        "nuvem",
        "suporte técnico",
    ],
}

PRESET_ORGAOS: dict[str, dict[str, str]] = {
    "Prefeitura de Belford Roxo": {"cnpj": "39485438000142", "unidade": ""},
    "SMSUB São Paulo": {"cnpj": "49269236000117", "unidade": "925004"},
    "Prefeitura de Belo Horizonte": {"cnpj": "18715383000140", "unidade": ""},
}

TABLE_COLUMNS: list[str] = [
    "numeroControlePNCP",
    "numeroContratoEmpenho",
    "processo",
    "nomeRazaoSocialFornecedor",
    "niFornecedor",
    "dataAssinatura",
    "dataVigenciaInicio",
    "dataVigenciaFim",
    "valorGlobal",
    "objetoContrato",
]


def normalize_topic_key(value: str) -> str:
    return normalize_text(value)


def suggested_terms(topic: str) -> list[str]:
    topic_key = normalize_topic_key(topic)
    terms: list[str] = []
    for key, suggestions in KEYWORD_SUGGESTIONS.items():
        if key in topic_key:
            terms.extend(suggestions)
    return list(dict.fromkeys(terms))


def records_to_dataframe(records: list[dict[str, Any]]) -> pd.DataFrame:
    rows = [{col: record.get(col) for col in TABLE_COLUMNS} for record in records]
    return pd.DataFrame(rows, columns=TABLE_COLUMNS)


def record_label(record: dict[str, Any]) -> str:
    number = record.get("numeroControlePNCP") or "sem PNCP"
    supplier = record.get("nomeRazaoSocialFornecedor") or "fornecedor não informado"
    value = float(record.get("valorGlobal") or 0)
    return f"{number} | {supplier} | R$ {value:,.2f}"


@st.cache_data(show_spinner=False, ttl=900)
def cached_contract_search(
    year: int,
    cnpj_orgao: str,
    codigo_unidade: str,
    page_size: int,
    max_pages: int,
) -> dict[str, Any]:
    result = fetch_contracts_by_publication(
        start_date=date(year, 1, 1),
        end_date=date(year, 12, 31),
        cnpj_orgao=cnpj_orgao,
        codigo_unidade=codigo_unidade,
        page_size=page_size,
        max_pages=max_pages,
    )
    return {"url": result.url, "payload": result.payload}


@st.cache_data(show_spinner=False, ttl=900)
def cached_contract_files(cnpj_orgao: str, year: int, sequencial: int) -> dict[str, Any]:
    result = list_contract_documents(
        cnpj_orgao,
        year,
        sequencial,
        gateway=PncpDocumentGateway(),
    )
    return {"url": result.url, "payload": result.payload}


__all__ = [
    "KEYWORD_SUGGESTIONS",
    "PRESET_ORGAOS",
    "TABLE_COLUMNS",
    "cached_contract_files",
    "cached_contract_search",
    "contract_detail_url",
    "contract_file_download_url",
    "filter_records_by_terms",
    "normalize_topic_key",
    "record_label",
    "records_to_dataframe",
    "suggested_terms",
]
