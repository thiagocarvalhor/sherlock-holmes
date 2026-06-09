"""Compare one manual record with one official contract record."""

from __future__ import annotations

from typing import Any

from sherlock_holmes.domain.entities import (
    RecordComparison,
    compare_records,
    evidence_from_manual_spreadsheet,
    evidence_from_official_api,
)


def compare_manual_record(
    manual_record: dict[str, Any],
    official_record: dict[str, Any],
    *,
    source_url: str = "",
    method: str = "pncp_contract_selected",
) -> RecordComparison:
    """Compare a manual row with one official PNCP contract record."""

    source_row = str(manual_record.get("source_row", ""))
    numero = str(official_record.get("numeroControlePNCP", ""))

    manual_evidence = evidence_from_manual_spreadsheet(
        evidence_id=f"manual_row{source_row}",
        field_name="",
        value=manual_record,
        source_row=source_row,
    )
    official_evidence = evidence_from_official_api(
        evidence_id=f"pncp_{numero}",
        source_url=source_url,
        method=method,
        value=official_record,
        metadata={"numeroControlePNCP": numero},
    )
    return compare_records(
        source_row=source_row,
        manual_record=manual_record,
        pncp_record=official_record,
        manual_evidence=manual_evidence,
        official_evidence=official_evidence,
    )


__all__ = ["compare_manual_record"]
