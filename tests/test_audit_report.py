"""Tests for auditable comparison reports."""

from __future__ import annotations

import json

from sherlock_holmes.reporting import (
    build_audit_report,
    load_comparison_results,
    render_audit_report_markdown,
    summarize_comparisons,
    write_audit_report_json,
    write_audit_report_markdown,
)


def _comparison(numero: str, score: float, status: str) -> dict:
    return {
        "source_row": "67",
        "numero_controle_pncp": numero,
        "overall_score": score,
        "status": status,
        "fields": [
            {
                "field_name": "valor_contrato",
                "manual_value": "52801942.27",
                "official_value": "52801942.27",
                "status": "match",
                "similarity_score": 1.0,
                "manual_evidence_id": "manual_row67",
                "official_evidence_id": f"pncp_{numero}",
                "notes": "Values match after normalization.",
            },
            {
                "field_name": "objeto_contrato",
                "manual_value": "LIMPEZA URBANA",
                "official_value": "CONTRATACAO DE EMPRESA PARA COLETA",
                "status": "divergent",
                "similarity_score": 0.0,
                "manual_evidence_id": "manual_row67",
                "official_evidence_id": f"pncp_{numero}",
                "notes": "Values differ after normalization.",
            },
        ],
    }


def test_summarize_comparisons_identifies_best_candidate():
    summary = summarize_comparisons([
        _comparison("39485438000142-2-000003/2025", 0.35, "divergent"),
        _comparison("39485438000142-2-000019/2025", 0.85, "partial_match"),
        _comparison("39485438000142-2-000003/2025", 0.35, "divergent"),
    ])
    assert summary["source_row"] == "67"
    assert summary["candidates_count"] == 3
    assert summary["best_candidate"] == "39485438000142-2-000019/2025"
    assert summary["best_status"] == "partial_match"
    assert summary["duplicate_candidates_count"] == 1
    assert summary["duplicate_candidates"] == ["39485438000142-2-000003/2025"]
    assert summary["review_fields_count"] == 1
    assert summary["recommended_next_action"] == "revisar campos parciais/divergentes e documentos oficiais"


def test_build_audit_report_contains_ranked_candidates_and_review_fields():
    report = build_audit_report(
        [
            _comparison("39485438000142-2-000003/2025", 0.35, "divergent"),
            _comparison("39485438000142-2-000019/2025", 0.85, "partial_match"),
        ],
        generated_at="2026-06-07T12:00:00+00:00",
    )
    assert report["summary"]["best_candidate"] == "39485438000142-2-000019/2025"
    assert report["candidates"][0]["rank"] == 1
    assert report["candidates"][0]["overall_score"] == 0.85
    assert report["review_fields"][0]["field_name"] == "objeto_contrato"


def test_render_audit_report_markdown_includes_core_sections():
    report = build_audit_report([_comparison("39485438000142-2-000019/2025", 0.85, "partial_match")])
    markdown = render_audit_report_markdown(report)
    assert "# Relatorio Auditavel de Comparacao" in markdown
    assert "## Candidatos" in markdown
    assert "## Melhor Candidato - Campo a Campo" in markdown
    assert "39485438000142-2-000019/2025" in markdown


def test_write_audit_report_outputs_roundtrip(tmp_path):
    report = build_audit_report(
        [_comparison("39485438000142-2-000019/2025", 0.85, "partial_match")],
        generated_at="2026-06-07T12:00:00+00:00",
    )
    json_path = write_audit_report_json(report, output_path=tmp_path / "audit_report.json")
    markdown_path = write_audit_report_markdown(report, output_path=tmp_path / "audit_report.md")
    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded["summary"]["best_score"] == 0.85
    assert markdown_path.read_text(encoding="utf-8").startswith("# Relatorio Auditavel")


def test_load_comparison_results_reads_json_list(tmp_path):
    path = tmp_path / "record_comparison.json"
    path.write_text(json.dumps([_comparison("n", 1.0, "match")]), encoding="utf-8")
    assert load_comparison_results(path)[0]["numero_controle_pncp"] == "n"
