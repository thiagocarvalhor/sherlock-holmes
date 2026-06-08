"""Generate a consolidated audit report from comparison result files."""

from __future__ import annotations

import argparse
from pathlib import Path

from sherlock_holmes.reporting import (
    build_audit_report,
    build_batch_audit_report,
    load_comparison_results,
    write_batch_audit_report_json,
    write_batch_audit_report_markdown,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "data/processed/comparison"
DEFAULT_OUTPUT_DIR = ROOT / "data/processed/reports/batch"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR), help="Directory containing comparison outputs")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for consolidated reports")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    comparison_files = sorted(input_dir.glob("**/record_comparison.json"))
    if not comparison_files:
        raise SystemExit(f"No record_comparison.json files found under {input_dir}")

    reports = []
    for comparison_file in comparison_files:
        comparisons = load_comparison_results(comparison_file)
        reports.append(build_audit_report(comparisons, title=f"Relatorio Auditavel - {comparison_file.parent.name}"))

    batch_report = build_batch_audit_report(reports)
    json_path = write_batch_audit_report_json(batch_report, output_path=output_dir / "audit_batch_report.json")
    markdown_path = write_batch_audit_report_markdown(batch_report, output_path=output_dir / "audit_batch_report.md")

    summary = batch_report["summary"]
    print(f"Linhas consolidadas: {summary['rows_count']}")
    print(f"Candidatos avaliados: {summary['total_candidates']}")
    print(f"Linhas para revisao: {summary['review_rows_count']}")
    print(f"JSON: {json_path}")
    print(f"Markdown: {markdown_path}")


if __name__ == "__main__":
    main()
