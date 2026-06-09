"""Compatibility wrapper for outbound PNCP contract helpers."""

from sherlock_holmes.adapters.outbound.pncp.contratos import (
    CONSULTA_BASE_URL,
    PNCP_BASE_URL,
    PNCP_FILE_BASE_URL,
    PncpRequestResult,
    contract_publication_url,
    contrato_arquivo_download_url,
    fetch_contracts_by_publication,
    get_contrato,
    get_contrato_url,
    list_contrato_arquivos,
    list_contrato_arquivos_url,
    search_contratos,
    search_contratos_url,
)

__all__ = [
    "CONSULTA_BASE_URL",
    "PNCP_BASE_URL",
    "PNCP_FILE_BASE_URL",
    "PncpRequestResult",
    "contract_publication_url",
    "contrato_arquivo_download_url",
    "fetch_contracts_by_publication",
    "get_contrato",
    "get_contrato_url",
    "list_contrato_arquivos",
    "list_contrato_arquivos_url",
    "search_contratos",
    "search_contratos_url",
]
