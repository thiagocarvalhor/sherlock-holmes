"""Tests for review preparation use case."""

from sherlock_holmes.application.use_cases import prepare_review
from sherlock_holmes.domain.entities import FieldComparison, RecordComparison
from sherlock_holmes.domain.services import ReviewAssessment


def test_prepare_review_returns_operational_recommendation():
    comparison = RecordComparison(
        source_row="67",
        numero_controle_pncp="39485438000142-2-000019/2025",
        fields=[
            FieldComparison(
                field_name="objeto_contrato",
                manual_value="LIMPEZA URBANA",
                official_value="COLETA DE RESIDUOS",
                status="divergent",
                similarity_score=0.0,
                manual_evidence_id="manual_row67",
                official_evidence_id="pncp_39485438000142-2-000019/2025",
            )
        ],
        overall_score=0.85,
        status="partial_match",
    )

    assessment = prepare_review(comparison, [{"titulo": "Contrato"}])

    assert isinstance(assessment, ReviewAssessment)
    assert assessment.document_review_required is True
    assert assessment.document_review_status == "revisar_documento"
    assert assessment.ocr_status == "pode_precisar"
    assert assessment.to_dict()["review_fields"] == ["objeto_contrato"]
