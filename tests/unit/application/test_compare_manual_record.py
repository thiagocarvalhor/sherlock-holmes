"""Tests for the manual-record comparison use case."""

from sherlock_holmes.application.use_cases import compare_manual_record
from sherlock_holmes.domain.entities import RecordComparison

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

CONTRACT = {
    "numeroControlePNCP": "39485438000142-2-000019/2025",
    "orgaoEntidade": {"cnpj": "39485438000142"},
    "unidadeOrgao": {"municipioNome": "Belford Roxo", "ufSigla": "RJ"},
    "objetoContrato": "CONTRATACAO DE EMPRESA PARA COLETA DE RESIDUOS",
    "numeroContratoEmpenho": "02/SEMSEP/2025",
    "valorGlobal": 52801942.27,
    "dataVigenciaInicio": "2025-11-04",
    "dataVigenciaFim": "2026-11-03",
}


def test_compare_manual_record_builds_record_comparison():
    comparison = compare_manual_record(
        MANUAL_ROW,
        CONTRACT,
        source_url="https://pncp.gov.br/app/contratos/39485438000142/2025/19",
        method="test_method",
    )

    assert isinstance(comparison, RecordComparison)
    assert comparison.source_row == "67"
    assert comparison.numero_controle_pncp == "39485438000142-2-000019/2025"
    assert comparison.status == "partial_match"

    by_field = {field.field_name: field for field in comparison.fields}
    assert by_field["cnpj"].status == "match"
    assert by_field["valor_contrato"].manual_evidence_id == "manual_row67"
    assert by_field["valor_contrato"].official_evidence_id == "pncp_39485438000142-2-000019/2025"
