"""Compare manual row 67 against all PNCP candidates and generate reports."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from sherlock_holmes.domain.entities import (
    RecordComparison,
    compare_records,
    evidence_from_manual_spreadsheet,
    evidence_from_official_api,
)

ROOT = Path(__file__).resolve().parents[5]

RAW_DIR = ROOT / "data/raw/pncp/pncp-refactor-live-row67/contracts"
SOURCE_JSON = RAW_DIR / "source_row_67.json"
OUTPUT_DIR = ROOT / "data/processed/comparison/row67"
PNCP_API_URL = "https://pncp.gov.br/api/consulta/v1/contratos"


def load_all_candidates() -> tuple[str, dict, list[dict]]:
    """Return (source_row, manual_record, all candidates across all saved pages)."""
    page1 = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    source_row: str = page1["source_row"]
    manual_record: dict = page1["manual_record"]
    candidates: list[dict] = list(page1["response"]["data"])

    for extra_page in sorted(RAW_DIR.glob("source_row_67_page*.json")):
        extra = json.loads(extra_page.read_text(encoding="utf-8"))
        page_candidates = extra["response"].get("data", [])
        candidates.extend(page_candidates)
        print(f"  Pagina {extra['page']}: +{len(page_candidates)} candidatos ({extra_page.name})")

    return source_row, manual_record, candidates


def main() -> None:
    print("Carregando candidatos...")
    source_row, manual_record, candidates = load_all_candidates()

    print(f"Linha {source_row}: {len(candidates)} candidatos PNCP no total")
    print(f"Manual: CNPJ={manual_record['cnpj']}  valor={manual_record['valor_contrato']}")
    print()

    manual_ev = evidence_from_manual_spreadsheet(
        evidence_id=f"manual_row{source_row}",
        field_name="",
        value=manual_record,
        source_row=source_row,
        source_path=str(SOURCE_JSON),
    )

    results: list[RecordComparison] = []

    for candidate in candidates:
        numero_controle = candidate.get("numeroControlePNCP", "?")
        official_ev = evidence_from_official_api(
            evidence_id=f"pncp_{numero_controle}",
            source_url=PNCP_API_URL,
            method="pncp_contratos_search",
            value=candidate,
            metadata={"numeroControlePNCP": numero_controle},
        )
        result = compare_records(
            source_row=source_row,
            manual_record=manual_record,
            pncp_record=candidate,
            manual_evidence=manual_ev,
            official_evidence=official_ev,
        )
        results.append(result)

    results.sort(key=lambda r: r.overall_score, reverse=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = OUTPUT_DIR / "record_comparison.json"
    json_path.write_text(
        json.dumps(
            [_result_to_dict(r) for r in results],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    best = results[0]
    csv_path = OUTPUT_DIR / "record_comparison.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "field_name",
                "manual_value",
                "official_value",
                "status",
                "similarity_score",
                "notes",
            ],
        )
        writer.writeheader()
        for fc in best.fields:
            writer.writerow(
                {
                    "field_name": fc.field_name,
                    "manual_value": fc.manual_value,
                    "official_value": fc.official_value,
                    "status": fc.status,
                    "similarity_score": fc.similarity_score,
                    "notes": fc.notes,
                }
            )

    print("=== Resultado por candidato ===")
    for r in results:
        print(f"  {r.numero_controle_pncp:<40}  score={r.overall_score:.4f}  status={r.status}")

    print()
    print(f"Melhor candidato: {best.numero_controle_pncp}")
    print(f"  score={best.overall_score:.4f}  status={best.status}")
    print()
    print("Comparacao campo a campo (melhor candidato):")
    for fc in best.fields:
        print(f"  {fc.field_name:<20}  {fc.status:<22}  score={fc.similarity_score:.2f}")
        print(f"    manual  : {fc.manual_value}")
        print(f"    oficial : {fc.official_value}")

    print()
    print(f"JSON : {json_path}")
    print(f"CSV  : {csv_path}")


def _result_to_dict(result: RecordComparison) -> dict:
    return {
        "source_row": result.source_row,
        "numero_controle_pncp": result.numero_controle_pncp,
        "overall_score": result.overall_score,
        "status": result.status,
        "notes": result.notes,
        "fields": [asdict(fc) for fc in result.fields],
    }


if __name__ == "__main__":
    main()
