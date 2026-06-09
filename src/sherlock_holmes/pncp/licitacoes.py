"""Compatibility wrapper for outbound PNCP procurement helpers."""

from sherlock_holmes.adapters.outbound.pncp.licitacoes import (
    CONSULTA_BASE_URL,
    PNCP_BASE_URL,
    PncpRequestResult,
    get_licitacao,
    get_licitacao_url,
    list_licitacao_arquivos,
    list_licitacao_arquivos_url,
    list_licitacao_itens,
    list_licitacao_itens_url,
    search_licitacoes,
    search_licitacoes_url,
)

__all__ = [
    "CONSULTA_BASE_URL",
    "PNCP_BASE_URL",
    "PncpRequestResult",
    "get_licitacao",
    "get_licitacao_url",
    "list_licitacao_arquivos",
    "list_licitacao_arquivos_url",
    "list_licitacao_itens",
    "list_licitacao_itens_url",
    "search_licitacoes",
    "search_licitacoes_url",
]
