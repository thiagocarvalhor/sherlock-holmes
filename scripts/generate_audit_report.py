"""Generate an auditable report from record comparison results."""

from __future__ import annotations

import argparse
from pathlib import Path

from sherlock_holmes.application.use_cases import (
    build_audit_report,
    load_cnpj_enrichments,
    load_comparison_results,
    load_document_references,
    write_audit_report_json,
    write_audit_report_markdown,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/processed/comparison/row67/record_comparison.json"
DEFAULT_OUTPUT_DIR = ROOT / "data/processed/reports/row67"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to record_comparison.json")
    parser.add_argument("--documents", default="", help="Optional JSON file with official document references")
    parser.add_argument("--cnpj-enrichment", default="", help="Optional JSON file with BrasilAPI CNPJ enrichments")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for report outputs")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    comparisons = load_comparison_results(input_path)
    documents = load_document_references(args.documents) if args.documents else []
    enrichments = load_cnpj_enrichments(args.cnpj_enrichment) if args.cnpj_enrichment else []
    report = build_audit_report(comparisons, official_documents=documents, cnpj_enrichments=enrichments)

    json_path = write_audit_report_json(report, output_path=output_dir / "audit_report.json")
    markdown_path = write_audit_report_markdown(report, output_path=output_dir / "audit_report.md")

    summary = report["summary"]
    print(f"Linha manual: {summary['source_row']}")
    print(f"Candidatos: {summary['candidates_count']}")
    print(f"Melhor candidato: {summary['best_candidate']} ({summary['best_score']:.4f})")
    print(f"Documentos oficiais: {summary['official_documents_count']}")
    print(f"CNPJs enriquecidos: {summary['cnpj_enrichments_count']}")
    print(f"JSON: {json_path}")
    print(f"Markdown: {markdown_path}")


if __name__ == "__main__":
    main()
