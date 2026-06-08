"""Tests for auditable comparison reports."""

from __future__ import annotations

import json

from sherlock_holmes.reporting import (
    build_audit_report,
    build_batch_audit_report,
    load_cnpj_enrichments,
    load_comparison_results,
    load_document_references,
    render_audit_report_markdown,
    render_batch_audit_report_markdown,
    summarize_comparisons,
    write_audit_report_json,
    write_audit_report_markdown,
    write_batch_audit_report_json,
    write_batch_audit_report_markdown,
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


def _document_reference() -> dict:
    return {
        "source": "pncp",
        "resource_type": "contract",
        "resource_id": "39485438000142/2025/19",
        "title": "Contrato limpeza urbana",
        "document_type": "Contrato",
        "sequence": 1,
        "url": "https://pncp.gov.br/documentos/contrato.pdf",
        "published_at": "2025-11-03",
    }


def _cnpj_enrichment() -> dict:
    return {
        "role": "orgao",
        "cnpj": "39485438000142",
        "razao_social": "MUNICIPIO DE BELFORD ROXO",
        "nome_fantasia": "",
        "cnae_fiscal": "8411600",
        "cnae_fiscal_descricao": "Administracao publica em geral",
        "municipio": "BELFORD ROXO",
        "uf": "RJ",
        "situacao_cadastral": "ATIVA",
        "data_inicio_atividade": "1990-01-01",
        "capital_social": 0.0,
        "socios": [{"nome_socio": "PREFEITO TESTE"}],
        "source_url": "https://brasilapi.com.br/api/cnpj/v1/39485438000142",
        "collected_at": "2026-06-07T12:00:00+00:00",
        "raw_payload": {"cnpj": "39485438000142"},
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
        official_documents=[_document_reference()],
        cnpj_enrichments=[_cnpj_enrichment()],
        generated_at="2026-06-07T12:00:00+00:00",
    )
    assert report["summary"]["best_candidate"] == "39485438000142-2-000019/2025"
    assert report["summary"]["official_documents_count"] == 1
    assert report["summary"]["cnpj_enrichments_count"] == 1
    assert report["summary"]["enriched_cnpjs"] == ["39485438000142"]
    assert report["summary"]["documents_review_required"] is True
    assert report["candidates"][0]["rank"] == 1
    assert report["candidates"][0]["overall_score"] == 0.85
    assert report["review_fields"][0]["field_name"] == "objeto_contrato"
    assert report["official_documents"][0]["title"] == "Contrato limpeza urbana"
    assert report["cnpj_enrichments"][0]["razao_social"] == "MUNICIPIO DE BELFORD ROXO"


def test_render_audit_report_markdown_includes_core_sections():
    report = build_audit_report(
        [_comparison("39485438000142-2-000019/2025", 0.85, "partial_match")],
        official_documents=[_document_reference()],
        cnpj_enrichments=[_cnpj_enrichment()],
    )
    markdown = render_audit_report_markdown(report)
    assert "# Relatorio Auditavel de Comparacao" in markdown
    assert "## Candidatos" in markdown
    assert "## Melhor Candidato - Campo a Campo" in markdown
    assert "## Documentos Oficiais Vinculados" in markdown
    assert "Contrato limpeza urbana" in markdown
    assert "## Enriquecimento CNPJ" in markdown
    assert "MUNICIPIO DE BELFORD ROXO" in markdown
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


def test_load_document_references_reads_nested_payload(tmp_path):
    path = tmp_path / "documents.json"
    path.write_text(json.dumps({"documents": [_document_reference()]}), encoding="utf-8")
    loaded = load_document_references(path)
    assert loaded[0]["resource_id"] == "39485438000142/2025/19"
    assert loaded[0]["sequence"] == 1
    assert loaded[0]["url"] == "https://pncp.gov.br/documentos/contrato.pdf"


def test_load_cnpj_enrichments_reads_nested_payload(tmp_path):
    path = tmp_path / "cnpj_enrichments.json"
    path.write_text(json.dumps({"cnpj_enrichments": [_cnpj_enrichment()]}), encoding="utf-8")
    loaded = load_cnpj_enrichments(path)
    assert loaded[0]["cnpj"] == "39485438000142"
    assert loaded[0]["socios_count"] == 1
    assert loaded[0]["source_url"] == "https://brasilapi.com.br/api/cnpj/v1/39485438000142"


def test_build_batch_audit_report_summarizes_multiple_rows():
    row67 = build_audit_report(
        [_comparison("39485438000142-2-000019/2025", 0.85, "partial_match")],
        official_documents=[_document_reference()],
        cnpj_enrichments=[_cnpj_enrichment()],
    )
    row68 = build_audit_report([_comparison("00000000000000-2-000001/2025", 1.0, "match")])
    batch = build_batch_audit_report([row67, row68], generated_at="2026-06-07T12:00:00+00:00")
    assert batch["summary"]["rows_count"] == 2
    assert batch["summary"]["total_candidates"] == 2
    assert batch["summary"]["total_official_documents"] == 1
    assert batch["summary"]["total_cnpj_enrichments"] == 1
    assert batch["summary"]["review_rows_count"] == 2
    assert batch["rows"][0]["official_documents_count"] == 1
    assert batch["rows"][0]["cnpj_enrichments_count"] == 1
    assert batch["rows"][0]["source_row"] == "67"


def test_render_batch_audit_report_markdown_includes_rows_table():
    row67 = build_audit_report([_comparison("39485438000142-2-000019/2025", 0.85, "partial_match")])
    batch = build_batch_audit_report([row67])
    markdown = render_batch_audit_report_markdown(batch)
    assert "# Relatorio Auditavel Multi-linha" in markdown
    assert "## Linhas" in markdown
    assert "39485438000142-2-000019/2025" in markdown


def test_write_batch_audit_report_outputs_roundtrip(tmp_path):
    row67 = build_audit_report([_comparison("39485438000142-2-000019/2025", 0.85, "partial_match")])
    batch = build_batch_audit_report([row67], generated_at="2026-06-07T12:00:00+00:00")
    json_path = write_batch_audit_report_json(batch, output_path=tmp_path / "audit_batch_report.json")
    markdown_path = write_batch_audit_report_markdown(batch, output_path=tmp_path / "audit_batch_report.md")
    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded["summary"]["rows_count"] == 1
    assert markdown_path.read_text(encoding="utf-8").startswith("# Relatorio Auditavel Multi-linha")
