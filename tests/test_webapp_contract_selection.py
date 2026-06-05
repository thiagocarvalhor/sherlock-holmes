"""Offline tests for Streamlit contract selection helpers."""

from __future__ import annotations

import pytest

pytest.importorskip("streamlit")

from sherlock_holmes.webapp.views import (  # noqa: E402
    _contract_candidates_dataframe,
    _rank_contract_candidates,
)

MANUAL_ROW = {
    "source_row": "67",
    "cnpj": "39485438000142",
    "municipio": "Belford Roxo",
    "uf": "RJ",
    "objeto_contrato": "LIMPEZA URBANA E MANEJO DE RESIDUOS",
    "numero_contrato": "02/SEMSEP/2025/2025",
    "valor_contrato": "52801942.27",
    "vigencia_inicio": "2025-11-04",
    "vigencia_fim": "2026-11-03",
}

WINNER = {
    "numeroControlePNCP": "39485438000142-2-000019/2025",
    "orgaoEntidade": {"cnpj": "39485438000142"},
    "unidadeOrgao": {"municipioNome": "Belford Roxo", "ufSigla": "RJ"},
    "objetoContrato": "CONTRATACAO DE EMPRESA PARA COLETA DE RESIDUOS",
    "numeroContratoEmpenho": "02/SEMSEP/2025",
    "valorGlobal": 52801942.27,
    "dataVigenciaInicio": "2025-11-04",
    "dataVigenciaFim": "2026-11-03",
}

OTHER = {
    "numeroControlePNCP": "39485438000142-2-000003/2025",
    "orgaoEntidade": {"cnpj": "39485438000142"},
    "unidadeOrgao": {"municipioNome": "Belford Roxo", "ufSigla": "RJ"},
    "objetoContrato": "AQUISICAO DE GAS LIQUEFEITO",
    "numeroContratoEmpenho": "8/SEMED",
    "valorGlobal": 607380.0,
    "dataVigenciaInicio": "2025-08-05",
    "dataVigenciaFim": "2026-08-05",
}


def test_rank_contract_candidates_preserves_manual_selection_without_reference_row():
    candidates = _rank_contract_candidates([OTHER, WINNER], manual_row=None)
    assert [c.contract["numeroControlePNCP"] for c in candidates] == [
        "39485438000142-2-000003/2025",
        "39485438000142-2-000019/2025",
    ]
    assert all(candidate.comparison is None for candidate in candidates)


def test_rank_contract_candidates_prioritizes_best_manual_match():
    candidates = _rank_contract_candidates([OTHER, WINNER], manual_row=MANUAL_ROW)
    assert candidates[0].contract["numeroControlePNCP"] == "39485438000142-2-000019/2025"
    assert candidates[0].comparison is not None
    assert candidates[0].comparison.status == "partial_match"
    assert candidates[0].comparison.overall_score > candidates[1].comparison.overall_score


def test_contract_candidates_dataframe_exposes_explanation_columns():
    candidates = _rank_contract_candidates([OTHER, WINNER], manual_row=MANUAL_ROW)
    dataframe = _contract_candidates_dataframe(candidates)
    assert list(dataframe.columns[:4]) == ["rank", "score", "status", "matches"]
    assert dataframe.iloc[0]["rank"] == 1
    assert dataframe.iloc[0]["status"] == "partial_match"
