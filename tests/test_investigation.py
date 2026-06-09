"""Tests for the live investigation orchestration (offline, no network)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from sherlock_holmes.application.use_cases import (
    InvestigationResult,
    build_search_window,
    investigate_row,
    load_manual_rows,
)
from sherlock_holmes.investigation import investigate_row as legacy_investigate_row
from sherlock_holmes.pncp.client import PncpRequestResult

SAMPLE_CSV = (
    Path(__file__).resolve().parents[1]
    / "documentation"
    / "plans"
    / "pncp-api-smoke-sample.csv"
)

ROW67 = {
    "source_row": "67",
    "cnpj": "39485438000142",
    "municipio": "Belford Roxo",
    "uf": "RJ",
    "objeto_contrato": "LIMPEZA URBANA E MANEJO DE RESÍDUOS",
    "numero_contrato": "02/SEMSEP/2025/2025",
    "valor_contrato": "52801942.27",
    "vigencia_inicio": "2025-11-04",
    "vigencia_fim": "2026-11-03",
}

WINNER = {
    "numeroControlePNCP": "39485438000142-2-000019/2025",
    "orgaoEntidade": {"cnpj": "39485438000142"},
    "unidadeOrgao": {"municipioNome": "Belford Roxo", "ufSigla": "RJ"},
    "objetoContrato": "CONTRATAÇÃO DE EMPRESA PARA COLETA DE RESÍDUOS",
    "numeroContratoEmpenho": "02/SEMSEP/2025",
    "valorGlobal": 52801942.27,
    "dataVigenciaInicio": "2025-11-04",
    "dataVigenciaFim": "2026-11-03",
}

OTHER = {
    "numeroControlePNCP": "39485438000142-2-000003/2025",
    "orgaoEntidade": {"cnpj": "39485438000142"},
    "unidadeOrgao": {"municipioNome": "Belford Roxo", "ufSigla": "RJ"},
    "objetoContrato": "AQUISIÇÃO DE GÁS LIQUEFEITO",
    "numeroContratoEmpenho": "8/SEMED",
    "valorGlobal": 607380.0,
    "dataVigenciaInicio": "2025-08-05",
    "dataVigenciaFim": "2026-08-05",
}


def _fake_fetch(candidates):
    def fetch_fn(*, start_date, end_date, cnpj_orgao, page_size, max_pages, timeout):
        return PncpRequestResult(
            url="https://pncp.gov.br/api/consulta/v1/contratos?fake=1",
            payload={"data": candidates, "totalRegistros": len(candidates)},
        )

    return fetch_fn


def test_legacy_investigation_wrapper_exports_use_case():
    assert legacy_investigate_row is investigate_row


def test_build_search_window_from_vigencia():
    start, end = build_search_window(ROW67, window_days=45)
    assert start == date(2025, 9, 20)
    assert end == date(2025, 12, 19)


def test_build_search_window_fallback_to_year():
    row = {"numero_contrato": "02/SEMSEP/2024"}
    start, end = build_search_window(row, window_days=45)
    assert start == date(2024, 1, 1)
    assert end == date(2024, 12, 31)


def test_investigate_row_ranks_winner_first():
    result = investigate_row(ROW67, fetch_fn=_fake_fetch([OTHER, WINNER]))
    assert isinstance(result, InvestigationResult)
    assert result.candidates_count == 2
    assert result.best is not None
    assert result.best.numero_controle_pncp == "39485438000142-2-000019/2025"
    assert result.best.status == "partial_match"
    assert result.best.overall_score > result.comparisons[1].overall_score


def test_investigate_row_no_candidates():
    result = investigate_row(ROW67, fetch_fn=_fake_fetch([]))
    assert result.candidates_count == 0
    assert result.best is None
    assert result.comparisons == []


def test_load_manual_rows_reads_sample_with_row67():
    rows = load_manual_rows(SAMPLE_CSV)
    assert rows, "sample CSV should not be empty"
    by_row = {r["source_row"]: r for r in rows}
    assert "67" in by_row
    assert by_row["67"]["cnpj"] == "39485438000142"
