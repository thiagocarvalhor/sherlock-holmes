"""Generate a consolidated audit report from comparison result files."""

from __future__ import annotations

import argparse
from pathlib import Path

from sherlock_holmes.reporting import (
    build_audit_report,
    build_batch_audit_report,
    load_cnpj_enrichments,
    load_comparison_results,
    load_document_references,
    write_batch_audit_report_json,
    write_batch_audit_report_markdown,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "data/processed/comparison"
DEFAULT_OUTPUT_DIR = ROOT / "data/processed/reports/batch"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR), help="Directory containing comparison outputs")
    parser.add_argument(
        "--documents-dir",
        default="",
        help="Optional directory containing document reference JSON files",
    )
    parser.add_argument(
        "--cnpj-enrichment-dir",
        default="",
        help="Optional directory containing BrasilAPI CNPJ enrichment JSON files",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for consolidated reports")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    documents_dir = Path(args.documents_dir) if args.documents_dir else None
    enrichment_dir = Path(args.cnpj_enrichment_dir) if args.cnpj_enrichment_dir else None
    output_dir = Path(args.output_dir)
    comparison_files = sorted(input_dir.glob("**/record_comparison.json"))
    if not comparison_files:
        raise SystemExit(f"No record_comparison.json files found under {input_dir}")

    reports = []
    for comparison_file in comparison_files:
        comparisons = load_comparison_results(comparison_file)
        documents = _load_documents_for(comparison_file, documents_dir)
        enrichments = _load_cnpj_enrichments_for(comparison_file, enrichment_dir)
        reports.append(
            build_audit_report(
                comparisons,
                official_documents=documents,
                cnpj_enrichments=enrichments,
                title=f"Relatorio Auditavel - {comparison_file.parent.name}",
            )
        )

    batch_report = build_batch_audit_report(reports)
    json_path = write_batch_audit_report_json(batch_report, output_path=output_dir / "audit_batch_report.json")
    markdown_path = write_batch_audit_report_markdown(batch_report, output_path=output_dir / "audit_batch_report.md")

    summary = batch_report["summary"]
    print(f"Linhas consolidadas: {summary['rows_count']}")
    print(f"Candidatos avaliados: {summary['total_candidates']}")
    print(f"Documentos oficiais: {summary['total_official_documents']}")
    print(f"CNPJs enriquecidos: {summary['total_cnpj_enrichments']}")
    print(f"Linhas para revisao: {summary['review_rows_count']}")
    print(f"JSON: {json_path}")
    print(f"Markdown: {markdown_path}")


def _load_documents_for(comparison_file: Path, documents_dir: Path | None) -> list[dict]:
    if documents_dir is None:
        return []

    row_name = comparison_file.parent.name
    candidates = [
        documents_dir / f"{row_name}.json",
        documents_dir / row_name / "documents.json",
        documents_dir / row_name / "official_documents.json",
    ]
    for path in candidates:
        if path.exists():
            return load_document_references(path)
    return []


def _load_cnpj_enrichments_for(comparison_file: Path, enrichment_dir: Path | None) -> list[dict]:
    if enrichment_dir is None:
        return []

    row_name = comparison_file.parent.name
    candidates = [
        enrichment_dir / f"{row_name}.json",
        enrichment_dir / row_name / "cnpj_enrichments.json",
        enrichment_dir / row_name / "cnpj_enrichment.json",
    ]
    for path in candidates:
        if path.exists():
            return load_cnpj_enrichments(path)
    return []


if __name__ == "__main__":
    main()
