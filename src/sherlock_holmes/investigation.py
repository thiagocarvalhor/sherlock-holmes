"""Live investigation: search PNCP for a manual row and compare candidates.

This module orchestrates the core investigation flow so both the Streamlit app
and operational scripts can reuse it:

    manual row -> PNCP search (date window from vigencia) -> compare each
    candidate -> ranked list of RecordComparison.

The PNCP fetch function is injectable (``fetch_fn``) so the flow can be tested
offline without touching the network.
"""

from __future__ import annotations

import csv
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from sherlock_holmes.pncp.client import (
    PncpRequestResult,
    compact_digits,
    fetch_contracts_by_publication,
)
from sherlock_holmes.validation import (
    RecordComparison,
    compare_records,
    evidence_from_manual_spreadsheet,
    evidence_from_official_api,
)

FetchFn = Callable[..., PncpRequestResult]

DEFAULT_WINDOW_DAYS = 45


def load_manual_rows(csv_path: str | Path) -> list[dict[str, str]]:
    """Load manual spreadsheet rows from a CSV file."""

    path = Path(csv_path)
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def _parse_iso_date(value: str | None) -> date | None:
    text = str(value or "").strip()
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def _infer_year(manual_row: dict[str, Any]) -> int:
    for key in ("vigencia_inicio", "vigencia_fim"):
        parsed = _parse_iso_date(manual_row.get(key))
        if parsed is not None:
            return parsed.year
    match = re.search(r"(20\d{2})", str(manual_row.get("numero_contrato", "")))
    if match:
        return int(match.group(1))
    return date.today().year


def build_search_window(
    manual_row: dict[str, Any], *, window_days: int = DEFAULT_WINDOW_DAYS
) -> tuple[date, date]:
    """Build a PNCP date window from a manual row's vigencia_inicio."""

    start = _parse_iso_date(manual_row.get("vigencia_inicio"))
    if start is not None and window_days > 0:
        return start - timedelta(days=window_days), start + timedelta(days=window_days)

    year = _infer_year(manual_row)
    return date(year, 1, 1), date(year, 12, 31)


@dataclass
class InvestigationResult:
    """Outcome of investigating one manual row against PNCP candidates."""

    source_row: str
    manual_row: dict[str, Any]
    query_url: str
    candidates_count: int
    comparisons: list[RecordComparison] = field(default_factory=list)
    best: RecordComparison | None = None


def investigate_row(
    manual_row: dict[str, Any],
    *,
    fetch_fn: FetchFn = fetch_contracts_by_publication,
    window_days: int = DEFAULT_WINDOW_DAYS,
    page_size: int = 500,
    max_pages: int = 20,
    timeout: int = 30,
) -> InvestigationResult:
    """Search PNCP for a manual row and compare every candidate contract."""

    source_row = str(manual_row.get("source_row", ""))
    cnpj = compact_digits(manual_row.get("cnpj"))
    start_date, end_date = build_search_window(manual_row, window_days=window_days)

    result = fetch_fn(
        start_date=start_date,
        end_date=end_date,
        cnpj_orgao=cnpj,
        page_size=page_size,
        max_pages=max_pages,
        timeout=timeout,
    )
    payload = result.payload if isinstance(result.payload, dict) else {}
    candidates = [item for item in payload.get("data", []) if isinstance(item, dict)]

    manual_evidence = evidence_from_manual_spreadsheet(
        evidence_id=f"manual_row{source_row}",
        field_name="",
        value=manual_row,
        source_row=source_row,
    )

    comparisons: list[RecordComparison] = []
    for candidate in candidates:
        numero = candidate.get("numeroControlePNCP", "")
        official_evidence = evidence_from_official_api(
            evidence_id=f"pncp_{numero}",
            source_url=result.url,
            method="pncp_contratos_search",
            value=candidate,
            metadata={"numeroControlePNCP": numero},
        )
        comparisons.append(
            compare_records(
                source_row=source_row,
                manual_record=manual_row,
                pncp_record=candidate,
                manual_evidence=manual_evidence,
                official_evidence=official_evidence,
            )
        )

    comparisons.sort(key=lambda c: c.overall_score, reverse=True)
    best = comparisons[0] if comparisons else None

    return InvestigationResult(
        source_row=source_row,
        manual_row=manual_row,
        query_url=result.url,
        candidates_count=len(candidates),
        comparisons=comparisons,
        best=best,
    )
