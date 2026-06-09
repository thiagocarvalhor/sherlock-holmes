"""Tests for domain review workflow decisions."""

from sherlock_holmes.domain.entities import FieldComparison, RecordComparison
from sherlock_holmes.domain.services import assess_review_needs


def _field(field_name: str, status: str) -> FieldComparison:
    return FieldComparison(
        field_name=field_name,
        manual_value="manual",
        official_value="official",
        status=status,
        similarity_score=1.0 if status == "match" else 0.0,
        manual_evidence_id="manual",
        official_evidence_id="official",
    )


def _comparison(*statuses: str) -> RecordComparison:
    fields = [_field(f"field_{index}", status) for index, status in enumerate(statuses, start=1)]
    return RecordComparison(
        source_row="67",
        numero_controle_pncp="39485438000142-2-000019/2025",
        fields=fields,
        overall_score=1.0,
        status="partial_match",
    )


def test_review_assessment_skips_document_review_for_full_match():
    assessment = assess_review_needs(_comparison("match"), [])

    assert assessment.document_review_required is False
    assert assessment.document_review_status == "nao_necessaria"
    assert assessment.ocr_status == "nao_necessario"
    assert assessment.review_fields == []


def test_review_assessment_flags_document_and_possible_ocr_when_documents_exist():
    assessment = assess_review_needs(_comparison("partial_match", "divergent"), [{"titulo": "Contrato"}])

    assert assessment.document_review_required is True
    assert assessment.document_review_status == "revisar_documento"
    assert assessment.ocr_status == "pode_precisar"
    assert assessment.review_fields_count == 2
    assert assessment.documents_count == 1


def test_review_assessment_flags_missing_documents_without_ocr_decision():
    assessment = assess_review_needs(_comparison("missing_in_official"), [])

    assert assessment.document_review_required is True
    assert assessment.document_review_status == "sem_documento"
    assert assessment.ocr_status == "nao_avaliado"
    assert assessment.to_dict()["review_fields"] == ["field_1"]
