"""Tests for field-by-field and record-level comparison."""

from __future__ import annotations

import pytest

from sherlock_holmes.validation import (
    compare_field_values,
    compare_records,
    evidence_from_manual_spreadsheet,
    evidence_from_official_api,
)


@pytest.fixture
def manual_ev():
    return evidence_from_manual_spreadsheet(
        evidence_id="manual_test",
        field_name="",
        value={},
        source_row="67",
    )


@pytest.fixture
def official_ev():
    return evidence_from_official_api(
        evidence_id="pncp_test",
        source_url="https://pncp.gov.br/api/consulta/v1/contratos",
        method="pncp_contratos_search",
    )


def _compare(field_name, manual, official, value_type, manual_ev, official_ev):
    return compare_field_values(
        field_name=field_name,
        manual_value=manual,
        official_value=official,
        manual_evidence=manual_ev,
        official_evidence=official_ev,
        value_type=value_type,
    )


def test_cnpj_match_ignores_mask(manual_ev, official_ev):
    result = _compare("cnpj", "39.485.438/0001-42", "39485438000142", "cnpj", manual_ev, official_ev)
    assert result.status == "match"
    assert result.similarity_score == 1.0


def test_number_match_within_tolerance(manual_ev, official_ev):
    result = _compare("valor", "52801942.27", 52801942.27, "number", manual_ev, official_ev)
    assert result.status == "match"


def test_number_divergent(manual_ev, official_ev):
    result = _compare("valor", "52801942.27", 1522778.0, "number", manual_ev, official_ev)
    assert result.status == "divergent"


def test_text_partial_match_by_containment(manual_ev, official_ev):
    result = _compare("numero", "02/SEMSEP/2025/2025", "02/SEMSEP/2025", "text", manual_ev, official_ev)
    assert result.status == "partial_match"
    assert result.similarity_score == pytest.approx(0.8)


def test_missing_in_manual(manual_ev, official_ev):
    result = _compare("uf", "", "RJ", "text", manual_ev, official_ev)
    assert result.status == "missing_in_manual"


def test_missing_in_official(manual_ev, official_ev):
    result = _compare("uf", "RJ", "", "text", manual_ev, official_ev)
    assert result.status == "missing_in_official"


def test_evidence_ids_are_linked(manual_ev, official_ev):
    result = _compare("uf", "RJ", "RJ", "text", manual_ev, official_ev)
    assert result.manual_evidence_id == "manual_test"
    assert result.official_evidence_id == "pncp_test"


# --- Record-level comparison: reproduces the validated row 67 winner ---

ROW67_MANUAL = {
    "cnpj": "39485438000142",
    "municipio": "Belford Roxo",
    "uf": "RJ",
    "objeto_contrato": "LIMPEZA URBANA E MANEJO DE RESÍDUOS",
    "numero_contrato": "02/SEMSEP/2025/2025",
    "valor_contrato": "52801942.27",
    "vigencia_inicio": "2025-11-04",
    "vigencia_fim": "2026-11-03",
}

ROW67_WINNER = {
    "numeroControlePNCP": "39485438000142-2-000019/2025",
    "orgaoEntidade": {"cnpj": "39485438000142"},
    "unidadeOrgao": {"municipioNome": "Belford Roxo", "ufSigla": "RJ"},
    "objetoContrato": "CONTRATAÇÃO DE EMPRESA ESPECIALIZADA PARA A EXECUÇÃO DE SERVIÇOS DE COLETA",
    "numeroContratoEmpenho": "02/SEMSEP/2025",
    "valorGlobal": 52801942.27,
    "dataVigenciaInicio": "2025-11-04",
    "dataVigenciaFim": "2026-11-03",
}


def test_compare_records_row67_winner(manual_ev, official_ev):
    result = compare_records(
        source_row="67",
        manual_record=ROW67_MANUAL,
        pncp_record=ROW67_WINNER,
        manual_evidence=manual_ev,
        official_evidence=official_ev,
    )
    assert result.numero_controle_pncp == "39485438000142-2-000019/2025"
    assert result.status == "partial_match"
    assert result.overall_score == pytest.approx(0.85)

    by_field = {f.field_name: f.status for f in result.fields}
    assert by_field["cnpj"] == "match"
    assert by_field["valor_contrato"] == "match"
    assert by_field["vigencia_fim"] == "match"
    assert by_field["numero_contrato"] == "partial_match"
    assert by_field["objeto_contrato"] == "divergent"


def test_compare_records_critical_divergent(manual_ev, official_ev):
    candidate = {**ROW67_WINNER, "valorGlobal": 1522778.0}
    result = compare_records(
        source_row="67",
        manual_record=ROW67_MANUAL,
        pncp_record=candidate,
        manual_evidence=manual_ev,
        official_evidence=official_ev,
    )
    assert result.status == "divergent"


def test_compare_records_perfect_match(manual_ev, official_ev):
    candidate = {
        **ROW67_WINNER,
        "objetoContrato": ROW67_MANUAL["objeto_contrato"],
        "numeroContratoEmpenho": ROW67_MANUAL["numero_contrato"],
    }
    result = compare_records(
        source_row="67",
        manual_record=ROW67_MANUAL,
        pncp_record=candidate,
        manual_evidence=manual_ev,
        official_evidence=official_ev,
    )
    assert result.status == "match"
    assert result.overall_score == pytest.approx(1.0)
