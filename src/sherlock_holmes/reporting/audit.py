"""Audit report generation from comparison results."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_comparison_results(path: str | Path) -> list[dict[str, Any]]:
    """Load a record comparison JSON file."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Comparison results must be a JSON list.")
    return [item for item in payload if isinstance(item, dict)]


def load_document_references(path: str | Path) -> list[dict[str, Any]]:
    """Load PNCP document references from a JSON file."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    records = _document_payload_records(payload)
    return [_document_row(record) for record in records]


def load_cnpj_enrichments(path: str | Path) -> list[dict[str, Any]]:
    """Load BrasilAPI CNPJ enrichment records from a JSON file."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    records = _cnpj_payload_records(payload)
    return [_cnpj_enrichment_row(record) for record in records]


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
    official_documents: list[Any] | None = None,
    cnpj_enrichments: list[Any] | None = None,
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
    documents = _document_rows(official_documents or [])
    enrichments = _cnpj_enrichment_rows(cnpj_enrichments or [])
    summary["official_documents_count"] = len(documents)
    summary["cnpj_enrichments_count"] = len(enrichments)
    summary["enriched_cnpjs"] = sorted(enrichment["cnpj"] for enrichment in enrichments if enrichment["cnpj"])
    summary["documents_review_required"] = bool(documents and review_fields)

    return {
        "title": title,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "candidates": [_candidate_row(candidate, index) for index, candidate in enumerate(ranked, start=1)],
        "best_candidate_fields": [_field_row(field) for field in best_fields],
        "review_fields": [_field_row(field) for field in review_fields],
        "official_documents": documents,
        "cnpj_enrichments": enrichments,
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
        f"- Documentos oficiais vinculados: `{summary.get('official_documents_count', 0)}`",
        f"- CNPJs enriquecidos: `{summary.get('cnpj_enrichments_count', 0)}`",
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

    lines.extend(["", "## Documentos Oficiais Vinculados", ""])
    if report.get("official_documents"):
        lines.extend(
            [
                "| recurso | tipo | titulo | sequencia | publicado em | origem |",
                "|---------|------|--------|------------|--------------|--------|",
            ]
        )
        for document in report["official_documents"]:
            lines.append(
                "| {resource_id} | {document_type} | {title} | {sequence} | "
                "{published_at} | {source_ref} |".format(**_markdown_document(document))
            )
    else:
        lines.append("Nenhum documento oficial vinculado ao relatorio.")

    lines.extend(["", "## Enriquecimento CNPJ", ""])
    if report.get("cnpj_enrichments"):
        lines.extend(
            [
                "| cnpj | papel | razao social | situacao | municipio/UF | CNAE | socios | fonte |",
                "|------|-------|--------------|----------|--------------|------|--------|-------|",
            ]
        )
        for enrichment in report["cnpj_enrichments"]:
            lines.append(
                "| {cnpj} | {role} | {razao_social} | {situacao_cadastral} | {location} | "
                "{cnae} | {socios_count} | {source_url} |".format(**_markdown_cnpj_enrichment(enrichment))
            )
    else:
        lines.append("Nenhum enriquecimento CNPJ vinculado ao relatorio.")

    return "\n".join(lines) + "\n"


def build_batch_audit_report(
    reports: list[dict[str, Any]],
    *,
    title: str = "Relatorio Auditavel Multi-linha",
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a consolidated audit report from individual audit reports."""

    if not reports:
        raise ValueError("At least one audit report is required.")

    rows = [_batch_row(report, index) for index, report in enumerate(reports, start=1)]
    status_counts = _count_by_key(rows, "best_status")
    review_rows = [row for row in rows if row["review_fields_count"] > 0 or row["best_status"] != "match"]

    return {
        "title": title,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "summary": {
            "rows_count": len(rows),
            "total_candidates": sum(row["candidates_count"] for row in rows),
            "total_official_documents": sum(row["official_documents_count"] for row in rows),
            "total_cnpj_enrichments": sum(row["cnpj_enrichments_count"] for row in rows),
            "status_counts": status_counts,
            "review_rows_count": len(review_rows),
            "duplicate_candidates_total": sum(row["duplicate_candidates_count"] for row in rows),
        },
        "rows": rows,
        "review_rows": review_rows,
    }


def render_batch_audit_report_markdown(report: dict[str, Any]) -> str:
    """Render a consolidated audit report as Markdown."""

    summary = report["summary"]
    lines = [
        f"# {report['title']}",
        "",
        "## Resumo",
        "",
        f"- Gerado em: `{report['generated_at']}`",
        f"- Linhas consolidadas: `{summary['rows_count']}`",
        f"- Candidatos avaliados: `{summary['total_candidates']}`",
        f"- Documentos oficiais vinculados: `{summary.get('total_official_documents', 0)}`",
        f"- CNPJs enriquecidos: `{summary.get('total_cnpj_enrichments', 0)}`",
        f"- Linhas para revisao: `{summary['review_rows_count']}`",
        f"- Duplicatas detectadas: `{summary['duplicate_candidates_total']}`",
        "",
        "## Linhas",
        "",
        "| linha | melhor candidato | score | status | revisar campos | docs oficiais | CNPJs | candidatos |",
        "|-------|------------------|-------|--------|----------------|---------------|-------|------------|",
    ]

    for row in report["rows"]:
        lines.append(
            "| {source_row} | {best_candidate} | {best_score:.4f} | {best_status} | "
            "{review_fields_count} | {official_documents_count} | {cnpj_enrichments_count} | "
            "{candidates_count} |".format(**row)
        )

    lines.extend(["", "## Linhas Para Revisao", ""])
    if report["review_rows"]:
        lines.extend(
            [
                "| linha | motivo | proxima acao |",
                "|-------|--------|--------------|",
            ]
        )
        for row in report["review_rows"]:
            lines.append(
                "| {source_row} | {best_status}; {review_fields_count} campos | "
                "{recommended_next_action} |".format(**_markdown_row(row))
            )
    else:
        lines.append("Nenhuma linha pendente de revisao.")

    return "\n".join(lines) + "\n"


def write_batch_audit_report_json(report: dict[str, Any], *, output_path: str | Path) -> Path:
    """Write a consolidated audit report as JSON."""

    return write_audit_report_json(report, output_path=output_path)


def write_batch_audit_report_markdown(report: dict[str, Any], *, output_path: str | Path) -> Path:
    """Write a consolidated audit report as Markdown."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_batch_audit_report_markdown(report), encoding="utf-8")
    return path


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


def _batch_row(report: dict[str, Any], rank: int) -> dict[str, Any]:
    summary = report["summary"]
    return {
        "rank": rank,
        "source_row": str(summary.get("source_row") or ""),
        "best_candidate": str(summary.get("best_candidate") or ""),
        "best_score": float(summary.get("best_score") or 0.0),
        "best_status": str(summary.get("best_status") or ""),
        "candidates_count": int(summary.get("candidates_count") or 0),
        "review_fields_count": int(summary.get("review_fields_count") or 0),
        "divergent_fields_count": int(summary.get("divergent_fields_count") or 0),
        "duplicate_candidates_count": int(summary.get("duplicate_candidates_count") or 0),
        "official_documents_count": int(summary.get("official_documents_count") or 0),
        "cnpj_enrichments_count": int(summary.get("cnpj_enrichments_count") or 0),
        "enriched_cnpjs": [str(cnpj) for cnpj in summary.get("enriched_cnpjs", [])],
        "documents_review_required": bool(summary.get("documents_review_required") or False),
        "recommended_next_action": str(summary.get("recommended_next_action") or ""),
    }


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


def _document_payload_records(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("official_documents", "documents", "document_references", "data"):
            records = payload.get(key)
            if isinstance(records, list):
                return records
        if _has_document_reference_keys(payload):
            return [payload]
    raise ValueError("Document references must be a JSON list or an object containing a document list.")


def _document_rows(records: list[Any]) -> list[dict[str, Any]]:
    return [_document_row(record) for record in records]


def _document_row(record: Any) -> dict[str, Any]:
    data = _object_dict(record)
    reference = _object_dict(data.get("reference"))

    return {
        "source": _pick_document_value(data, reference, "source"),
        "resource_type": _pick_document_value(data, reference, "resource_type", "resourceType"),
        "resource_id": _pick_document_value(data, reference, "resource_id", "resourceId"),
        "numero_controle_pncp": _pick_document_value(
            data,
            reference,
            "numero_controle_pncp",
            "numeroControlePNCP",
        ),
        "title": _pick_document_value(data, reference, "title", "titulo", "nome"),
        "document_type": _pick_document_value(data, reference, "document_type", "tipoDocumentoNome", "tipo"),
        "sequence": _optional_int(_pick_document_value(data, reference, "sequence", "sequencialDocumento")),
        "url": _pick_document_value(data, reference, "url", "source_url"),
        "uri": _pick_document_value(data, reference, "uri"),
        "published_at": _pick_document_value(data, reference, "published_at", "dataPublicacaoPncp"),
        "local_path": _pick_document_value(data, reference, "local_path"),
    }


def _cnpj_payload_records(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("cnpj_enrichments", "enrichments", "records", "data"):
            records = payload.get(key)
            if isinstance(records, list):
                return records
        if _has_cnpj_enrichment_keys(payload):
            return [payload]
    raise ValueError("CNPJ enrichments must be a JSON list or an object containing an enrichment list.")


def _cnpj_enrichment_rows(records: list[Any]) -> list[dict[str, Any]]:
    return [_cnpj_enrichment_row(record) for record in records]


def _cnpj_enrichment_row(record: Any) -> dict[str, Any]:
    data = _object_dict(record)
    value = _object_dict(data.get("value"))
    metadata = _object_dict(data.get("metadata"))
    raw_payload = _object_dict(data.get("raw_payload"))
    standardized = _object_dict(data.get("standardized"))

    return {
        "role": _pick_enrichment_value(data, metadata, "role", "target_role", "label", "context"),
        "cnpj": _pick_enrichment_value(data, value, metadata, standardized, raw_payload, "cnpj"),
        "razao_social": _pick_enrichment_value(
            data,
            value,
            standardized,
            raw_payload,
            "razao_social",
            "razaoSocial",
        ),
        "nome_fantasia": _pick_enrichment_value(data, value, standardized, raw_payload, "nome_fantasia"),
        "cnae_fiscal": _pick_enrichment_value(data, value, standardized, raw_payload, "cnae_fiscal"),
        "cnae_fiscal_descricao": _pick_enrichment_value(
            data,
            value,
            standardized,
            raw_payload,
            "cnae_fiscal_descricao",
        ),
        "municipio": _pick_enrichment_value(data, value, standardized, raw_payload, "municipio"),
        "uf": _pick_enrichment_value(data, value, standardized, raw_payload, "uf"),
        "situacao_cadastral": _pick_enrichment_value(
            data,
            value,
            standardized,
            raw_payload,
            "situacao_cadastral",
            "descricao_situacao_cadastral",
        ),
        "data_inicio_atividade": _pick_enrichment_value(
            data,
            value,
            standardized,
            raw_payload,
            "data_inicio_atividade",
        ),
        "capital_social": _optional_float(
            _pick_enrichment_value(data, value, standardized, raw_payload, "capital_social")
        ),
        "socios_count": _socios_count(data, value, standardized, raw_payload),
        "source_url": _pick_enrichment_value(data, metadata, "source_url", "sourceUrl"),
        "collected_at": _pick_enrichment_value(data, metadata, "collected_at", "collectedAt"),
    }


def _has_cnpj_enrichment_keys(record: dict[str, Any]) -> bool:
    enrichment_keys = {
        "cnpj",
        "razao_social",
        "nome_fantasia",
        "source_url",
        "raw_payload",
        "value",
        "metadata",
    }
    return any(key in record for key in enrichment_keys)


def _pick_enrichment_value(*sources_and_keys: Any) -> str:
    first_key_index = next(
        (index for index, item in enumerate(sources_and_keys) if isinstance(item, str)),
        len(sources_and_keys),
    )
    sources = sources_and_keys[:first_key_index]
    keys = sources_and_keys[first_key_index:]
    for source in sources:
        if not isinstance(source, dict):
            continue
        for key in keys:
            value = source.get(key)
            if value is not None and value != "":
                return str(value)
    return ""


def _socios_count(*sources: dict[str, Any]) -> int:
    for source in sources:
        socios_count = source.get("socios_count")
        if socios_count is not None and socios_count != "":
            try:
                return int(float(str(socios_count)))
            except ValueError:
                return 0
        socios = source.get("socios")
        if isinstance(socios, list):
            return len(socios)
    return 0


def _has_document_reference_keys(record: dict[str, Any]) -> bool:
    document_keys = {
        "title",
        "titulo",
        "nome",
        "url",
        "uri",
        "resource_id",
        "resourceId",
        "numero_controle_pncp",
        "numeroControlePNCP",
    }
    return any(key in record for key in document_keys)


def _object_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, dict):
        return dict(value)
    return {
        key: getattr(value, key)
        for key in (
            "source",
            "resource_type",
            "resource_id",
            "title",
            "document_type",
            "sequence",
            "url",
            "uri",
            "published_at",
            "local_path",
            "cnpj",
            "razao_social",
            "nome_fantasia",
            "cnae_fiscal",
            "cnae_fiscal_descricao",
            "municipio",
            "uf",
            "situacao_cadastral",
            "data_inicio_atividade",
            "capital_social",
            "socios",
            "source_url",
            "collected_at",
        )
        if hasattr(value, key)
    }


def _pick_document_value(data: dict[str, Any], reference: dict[str, Any], *keys: str) -> str:
    for source in (data, reference):
        for key in keys:
            value = source.get(key)
            if value is not None and value != "":
                return str(value)
    return ""


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def _markdown_field(field: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(field)
    for key in ("manual_value", "official_value", "notes"):
        cleaned[key] = _markdown_cell(str(cleaned.get(key) or ""))
    return cleaned


def _markdown_document(document: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(document)
    source_ref = cleaned.get("url") or cleaned.get("uri") or cleaned.get("local_path") or ""
    cleaned["source_ref"] = _markdown_cell(str(source_ref))
    for key in ("resource_id", "document_type", "title", "published_at", "sequence"):
        cleaned[key] = _markdown_cell(str(cleaned.get(key) or ""))
    return cleaned


def _markdown_cnpj_enrichment(enrichment: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(enrichment)
    municipio = str(cleaned.get("municipio") or "")
    uf = str(cleaned.get("uf") or "")
    cnae = str(cleaned.get("cnae_fiscal") or "")
    cnae_description = str(cleaned.get("cnae_fiscal_descricao") or "")
    cleaned["location"] = "/".join(part for part in (municipio, uf) if part)
    cleaned["cnae"] = " - ".join(part for part in (cnae, cnae_description) if part)
    for key in (
        "cnpj",
        "role",
        "razao_social",
        "situacao_cadastral",
        "location",
        "cnae",
        "socios_count",
        "source_url",
    ):
        cleaned[key] = _markdown_cell(str(cleaned.get(key) or ""))
    return cleaned


def _markdown_row(row: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(row)
    for key in ("source_row", "best_status", "recommended_next_action"):
        cleaned[key] = _markdown_cell(str(cleaned.get(key) or ""))
    return cleaned


def _markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _string_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value)
