"""Audit report generation from comparison results."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_comparison_results(path: str | Path) -> list[dict[str, Any]]:
    """Load a record comparison JSON file."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Comparison results must be a JSON list.")
    return [item for item in payload if isinstance(item, dict)]


def summarize_comparisons(comparisons: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize ranked comparison results."""

    ranked = _rank_comparisons(comparisons)
    if not ranked:
        raise ValueError("At least one comparison result is required.")

    best = ranked[0]
    best_fields = _fields(best)
    status_counts = _count_by_key(ranked, "status")
    field_status_counts = _count_by_key(best_fields, "status")
    duplicate_candidates = _duplicate_values(ranked, "numero_controle_pncp")
    divergent_fields = [field for field in best_fields if field.get("status") == "divergent"]
    review_fields = [
        field
        for field in best_fields
        if field.get("status") in {"partial_match", "divergent", "missing_in_official", "missing_in_manual"}
    ]

    return {
        "source_row": str(best.get("source_row") or ""),
        "candidates_count": len(ranked),
        "best_candidate": str(best.get("numero_controle_pncp") or ""),
        "best_score": float(best.get("overall_score") or 0.0),
        "best_status": str(best.get("status") or ""),
        "candidate_status_counts": status_counts,
        "best_field_status_counts": field_status_counts,
        "duplicate_candidates_count": len(duplicate_candidates),
        "duplicate_candidates": duplicate_candidates,
        "divergent_fields_count": len(divergent_fields),
        "review_fields_count": len(review_fields),
        "recommended_next_action": _recommended_next_action(best, review_fields),
    }


def build_audit_report(
    comparisons: list[dict[str, Any]],
    *,
    title: str = "Relatorio Auditavel de Comparacao",
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a structured audit report from comparison results."""

    ranked = _rank_comparisons(comparisons)
    summary = summarize_comparisons(ranked)
    best = ranked[0]
    best_fields = _fields(best)
    review_fields = [
        field
        for field in best_fields
        if field.get("status") in {"partial_match", "divergent", "missing_in_official", "missing_in_manual"}
    ]

    return {
        "title": title,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "candidates": [_candidate_row(candidate, index) for index, candidate in enumerate(ranked, start=1)],
        "best_candidate_fields": [_field_row(field) for field in best_fields],
        "review_fields": [_field_row(field) for field in review_fields],
    }


def render_audit_report_markdown(report: dict[str, Any]) -> str:
    """Render a structured audit report as Markdown."""

    summary = report["summary"]
    lines = [
        f"# {report['title']}",
        "",
        "## Resumo",
        "",
        f"- Gerado em: `{report['generated_at']}`",
        f"- Linha manual: `{summary['source_row']}`",
        f"- Candidatos avaliados: `{summary['candidates_count']}`",
        f"- Melhor candidato: `{summary['best_candidate']}`",
        f"- Score: `{summary['best_score']:.4f}`",
        f"- Status: `{summary['best_status']}`",
        f"- Candidatos duplicados: `{summary['duplicate_candidates_count']}`",
        f"- Proxima acao recomendada: {summary['recommended_next_action']}",
        "",
        "## Candidatos",
        "",
        "| rank | numeroControlePNCP | score | status |",
        "|------|--------------------|-------|--------|",
    ]

    for candidate in report["candidates"]:
        lines.append(
            "| {rank} | {numero_controle_pncp} | {overall_score:.4f} | {status} |".format(**candidate)
        )

    lines.extend(
        [
            "",
            "## Melhor Candidato - Campo a Campo",
            "",
            "| campo | status | score | manual | oficial |",
            "|-------|--------|-------|--------|---------|",
        ]
    )
    for field in report["best_candidate_fields"]:
        lines.append(
            "| {field_name} | {status} | {similarity_score:.2f} | {manual_value} | {official_value} |".format(
                **_markdown_field(field)
            )
        )

    lines.extend(
        [
            "",
            "## Campos Para Revisao",
            "",
        ]
    )
    if report["review_fields"]:
        lines.extend(
            [
                "| campo | status | score | motivo |",
                "|-------|--------|-------|--------|",
            ]
        )
        for field in report["review_fields"]:
            lines.append(
                "| {field_name} | {status} | {similarity_score:.2f} | {notes} |".format(
                    **_markdown_field(field)
                )
            )
    else:
        lines.append("Nenhum campo pendente de revisao.")

    return "\n".join(lines) + "\n"


def write_audit_report_json(report: dict[str, Any], *, output_path: str | Path) -> Path:
    """Write a structured audit report as JSON."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_audit_report_markdown(report: dict[str, Any], *, output_path: str | Path) -> Path:
    """Write a structured audit report as Markdown."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_audit_report_markdown(report), encoding="utf-8")
    return path


def _rank_comparisons(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(comparisons, key=lambda item: float(item.get("overall_score") or 0.0), reverse=True)


def _fields(comparison: dict[str, Any]) -> list[dict[str, Any]]:
    fields = comparison.get("fields") or []
    return [field for field in fields if isinstance(field, dict)]


def _count_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "")
        counts[value] = counts.get(value, 0) + 1
    return counts


def _duplicate_values(rows: list[dict[str, Any]], key: str) -> list[str]:
    counts = _count_by_key(rows, key)
    return sorted(value for value, count in counts.items() if value and count > 1)


def _recommended_next_action(best: dict[str, Any], review_fields: list[dict[str, Any]]) -> str:
    status = str(best.get("status") or "")
    if status == "match" and not review_fields:
        return "registrar correspondencia como candidata a validacao final"
    if status == "partial_match":
        return "revisar campos parciais/divergentes e documentos oficiais"
    if status == "divergent":
        return "tratar como divergencia e revisar documentos oficiais"
    return "revisar manualmente o resultado"


def _candidate_row(candidate: dict[str, Any], rank: int) -> dict[str, Any]:
    return {
        "rank": rank,
        "source_row": str(candidate.get("source_row") or ""),
        "numero_controle_pncp": str(candidate.get("numero_controle_pncp") or ""),
        "overall_score": float(candidate.get("overall_score") or 0.0),
        "status": str(candidate.get("status") or ""),
    }


def _field_row(field: dict[str, Any]) -> dict[str, Any]:
    return {
        "field_name": str(field.get("field_name") or ""),
        "manual_value": _string_value(field.get("manual_value")),
        "official_value": _string_value(field.get("official_value")),
        "status": str(field.get("status") or ""),
        "similarity_score": float(field.get("similarity_score") or 0.0),
        "notes": str(field.get("notes") or ""),
        "manual_evidence_id": str(field.get("manual_evidence_id") or ""),
        "official_evidence_id": str(field.get("official_evidence_id") or ""),
    }


def _markdown_field(field: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(field)
    for key in ("manual_value", "official_value", "notes"):
        cleaned[key] = _markdown_cell(str(cleaned.get(key) or ""))
    return cleaned


def _markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _string_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value)
