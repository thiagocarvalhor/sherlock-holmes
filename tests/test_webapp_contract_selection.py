"""Offline tests for Streamlit contract selection helpers."""

from __future__ import annotations

import pytest

pytest.importorskip("streamlit")

from sherlock_holmes.enrichment import record_from_payload  # noqa: E402
from sherlock_holmes.webapp.views import (  # noqa: E402
    _build_webapp_audit_report,
    _cnpj_enrichment_targets,
    _cnpj_record_summary,
    _contract_candidates_dataframe,
    _official_documents_for_report,
    _rank_contract_candidates,
    _render_webapp_audit_markdown,
    _review_assessment,
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
    "anoContrato": 2025,
    "sequencialContrato": 19,
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

ENRICHMENT_CONTRACT = {
    "numeroControlePNCP": "39485438000142-2-000019/2025",
    "orgaoEntidade": {"cnpj": "39485438000142"},
    "nomeRazaoSocialFornecedor": "EMPRESA TESTE LTDA",
    "niFornecedor": "12.345.678/0001-95",
}

DOCUMENT_FILE = {
    "sequencialDocumento": 1,
    "titulo": "Contrato assinado",
    "tipoDocumentoNome": "Contrato",
    "dataPublicacaoPncp": "2025-11-03",
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


def test_cnpj_enrichment_targets_include_orgao_and_supplier_cnpjs():
    targets = _cnpj_enrichment_targets(ENRICHMENT_CONTRACT)
    assert targets == [
        {"role": "orgao", "label": "Orgao contratante", "cnpj": "39485438000142"},
        {"role": "fornecedor", "label": "EMPRESA TESTE LTDA", "cnpj": "12345678000195"},
    ]


def test_cnpj_enrichment_targets_skip_non_cnpj_supplier_identifier():
    contract = {**ENRICHMENT_CONTRACT, "niFornecedor": "123.456.789-10"}
    targets = _cnpj_enrichment_targets(contract)
    assert targets == [{"role": "orgao", "label": "Orgao contratante", "cnpj": "39485438000142"}]


def test_cnpj_record_summary_formats_main_fields():
    record = record_from_payload(
        {
            "cnpj": "12345678000195",
            "razao_social": "EMPRESA TESTE LTDA",
            "descricao_situacao_cadastral": "ATIVA",
            "municipio": "SAO PAULO",
            "uf": "SP",
            "socios": [{"nome_socio": "SOCIO TESTE"}],
        },
        source_url="https://brasilapi.com.br/api/cnpj/v1/12345678000195",
        collected_at="2026-06-07T12:00:00+00:00",
    )
    summary = _cnpj_record_summary(record)
    assert summary["razao_social"] == "EMPRESA TESTE LTDA"
    assert summary["municipio_uf"] == "SAO PAULO/SP"
    assert summary["socios_count"] == 1


def test_review_assessment_flags_document_review_and_possible_ocr():
    comparison = _rank_contract_candidates([WINNER], manual_row=MANUAL_ROW)[0].comparison
    assert comparison is not None
    documents = _official_documents_for_report(WINNER, [DOCUMENT_FILE])
    review = _review_assessment(comparison, documents)
    assert review["document_review_required"] is True
    assert review["document_review_status"] == "revisar_documento"
    assert review["ocr_status"] == "pode_precisar"
    assert review["documents_count"] == 1


def test_official_documents_for_report_adds_contract_context_and_download_url():
    documents = _official_documents_for_report(WINNER, [DOCUMENT_FILE])
    assert documents[0]["source"] == "pncp"
    assert documents[0]["resource_type"] == "contract"
    assert documents[0]["resource_id"] == "39485438000142/2025/19"
    assert documents[0]["numero_controle_pncp"] == "39485438000142-2-000019/2025"
    assert "arquivos/1" in documents[0]["url"]


def test_build_webapp_audit_report_includes_review_workflow():
    comparison = _rank_contract_candidates([WINNER], manual_row=MANUAL_ROW)[0].comparison
    assert comparison is not None
    documents = _official_documents_for_report(WINNER, [DOCUMENT_FILE])
    review = _review_assessment(comparison, documents)
    report = _build_webapp_audit_report(
        comparison,
        official_documents=documents,
        review=review,
        review_status="precisa_revisar_documento",
        review_notes="Conferir documento antes da validacao.",
    )
    assert report["summary"]["official_documents_count"] == 1
    assert report["review_workflow"]["review_status"] == "precisa_revisar_documento"
    assert report["review_workflow"]["ocr_status"] == "pode_precisar"
    markdown = _render_webapp_audit_markdown(report)
    assert "## Revisao Operacional" in markdown
    assert "Conferir documento antes da validacao." in markdown
