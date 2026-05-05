"""Run a small PNCP API smoke test from the manual smoke sample."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SAMPLE = ROOT_DIR / "documentation" / "plans" / "pncp-api-smoke-sample.csv"
DEFAULT_RAW_ROOT = ROOT_DIR / "data" / "raw" / "pncp"
DEFAULT_PROCESSED_ROOT = ROOT_DIR / "data" / "processed" / "pncp"
DEFAULT_BASE_URL = "https://pncp.gov.br/api/consulta"

SUMMARY_FIELDNAMES = [
    "source_row",
    "municipio",
    "uf",
    "numero_contrato",
    "cnpj",
    "query_url",
    "http_status",
    "elapsed_seconds",
    "total_registros",
    "total_paginas",
    "candidates_count",
    "top_score",
    "top_numero_controle_pncp",
    "top_numero_controle_pncp_compra",
    "top_numero_contrato_empenho",
    "raw_output_path",
    "candidates_output_path",
    "error",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run PNCP API smoke queries for contract samples.")
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--processed-root", type=Path, default=DEFAULT_PROCESSED_ROOT)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--source-row", action="append", default=[])
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--tamanho-pagina", type=int, default=10)
    parser.add_argument(
        "--date-window-days",
        type=int,
        default=45,
        help="Days before/after vigencia_inicio to query. Use 0 for the whole inferred year.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_sample(path: Path, limit: int | None) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    return rows[:limit] if limit is not None else rows


def filter_source_rows(rows: list[dict[str, str]], source_rows: list[str]) -> list[dict[str, str]]:
    if not source_rows:
        return rows
    allowed = {str(row) for row in source_rows}
    return [row for row in rows if row["source_row"] in allowed]


def compact_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def compact_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").casefold()).strip()


def contract_number_tokens(value: str) -> set[str]:
    tokens = {
        token.casefold()
        for token in re.split(r"[^0-9A-Za-z]+", value or "")
        if len(token) >= 3 and not re.fullmatch(r"20\d{2}", token)
    }
    digits = compact_digits(value)
    if len(digits) >= 6:
        tokens.add(digits)
    return tokens


def parse_iso_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def date_year(value: str) -> int | None:
    parsed = parse_iso_date(value)
    return parsed.year if parsed is not None else None


def build_contract_query(
    row: dict[str, str],
    tamanho_pagina: int,
    date_window_days: int,
) -> dict[str, str | int]:
    start_date = parse_iso_date(row.get("vigencia_inicio", ""))

    if start_date is not None and date_window_days > 0:
        data_inicial = start_date - timedelta(days=date_window_days)
        data_final = start_date + timedelta(days=date_window_days)
    else:
        year = date_year(row.get("vigencia_inicio", "")) or date_year(row.get("vigencia_fim", ""))
        if year is None:
            match = re.search(r"(20\d{2})", row.get("numero_contrato", ""))
            year = int(match.group(1)) if match else datetime.now().year
        data_inicial = datetime(year, 1, 1)
        data_final = datetime(year, 12, 31)

    params: dict[str, str | int] = {
        "dataInicial": data_inicial.strftime("%Y%m%d"),
        "dataFinal": data_final.strftime("%Y%m%d"),
        "pagina": 1,
        "tamanhoPagina": tamanho_pagina,
    }
    cnpj_orgao = compact_digits(row.get("cnpj", ""))
    if cnpj_orgao:
        params["cnpjOrgao"] = cnpj_orgao
    return params


def request_json(base_url: str, endpoint: str, params: dict[str, str | int], timeout: int) -> tuple[int, Any, str]:
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}?{urlencode(params)}"
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "sherlock-holmes-pncp-smoke/0.1"})

    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed public API URL.
            body = response.read()
            if not body:
                return response.status, None, url
            return response.status, json.loads(body.decode("utf-8")), url
    except HTTPError as exc:
        body = exc.read()
        parsed_body: Any
        try:
            parsed_body = json.loads(body.decode("utf-8")) if body else None
        except json.JSONDecodeError:
            parsed_body = body.decode("utf-8", errors="replace")
        return exc.code, parsed_body, url


def response_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("data"), list):
        return [item for item in payload["data"] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def score_candidate(row: dict[str, str], candidate: dict[str, Any]) -> int:
    candidate_blob = compact_text(json_text(candidate))
    candidate_digits = compact_digits(candidate_blob)
    score = 0

    cnpj = compact_digits(row.get("cnpj", ""))
    if cnpj and cnpj in candidate_digits:
        score += 5

    numero_contrato = row.get("numero_contrato", "")
    candidate_contract_number = compact_text(str(candidate.get("numeroContratoEmpenho", "")))
    candidate_process = compact_text(str(candidate.get("processo", "")))
    if numero_contrato and compact_text(numero_contrato) == candidate_contract_number:
        score += 5
    else:
        for token in contract_number_tokens(numero_contrato):
            if token in candidate_contract_number or token in candidate_process:
                score += 2
                break

    municipio = compact_text(row.get("municipio", ""))
    if municipio and municipio in candidate_blob:
        score += 2

    uf = compact_text(row.get("uf", ""))
    if uf and re.search(rf'"uf\w*"\s*:\s*"{re.escape(uf)}"', candidate_blob):
        score += 1

    empresa = compact_text(row.get("nome_empresa", ""))
    if empresa and empresa in candidate_blob:
        score += 3

    valor = row.get("valor_contrato", "")
    if valor and valor in candidate_blob:
        score += 2

    return score


def pick_candidates(row: dict[str, str], payload: Any) -> list[dict[str, Any]]:
    scored: list[dict[str, Any]] = []
    for candidate in response_records(payload):
        score = score_candidate(row, candidate)
        if score > 0:
            scored.append({"score": score, "record": candidate})
    return sorted(scored, key=lambda item: item["score"], reverse=True)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def write_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def relative_or_blank(path: Path | None) -> str:
    return path.relative_to(ROOT_DIR).as_posix() if path is not None else ""


def run() -> None:
    args = parse_args()
    run_id = args.run_id or datetime.now().strftime("pncp-api-smoke-%Y%m%d-%H%M%S")
    rows = filter_source_rows(load_sample(args.sample, args.limit), args.source_row)
    summary_rows: list[dict[str, Any]] = []

    for row in rows:
        source_row = row["source_row"]
        params = build_contract_query(row, args.tamanho_pagina, args.date_window_days)
        raw_output_path = args.raw_root / run_id / "contracts" / f"source_row_{source_row}.json"
        candidates_output_path = (
            args.processed_root / run_id / "candidates" / f"source_row_{source_row}.json"
        )

        started_at = time.perf_counter()
        error = ""
        status: int | str = ""
        payload: Any = None
        query_url = f"{args.base_url.rstrip('/')}/v1/contratos?{urlencode(params)}"
        candidates: list[dict[str, Any]] = []

        try:
            if args.dry_run:
                payload = {"dry_run": True, "params": params}
                status = "dry-run"
            else:
                status, payload, query_url = request_json(
                    args.base_url,
                    "/v1/contratos",
                    params,
                    args.timeout,
                )
                candidates = pick_candidates(row, payload)
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            error = f"{type(exc).__name__}: {exc}"
        finally:
            elapsed_seconds = round(time.perf_counter() - started_at, 6)

        write_json(
            raw_output_path,
            {
                "source_row": source_row,
                "manual_record": row,
                "request": {"url": query_url, "params": params},
                "http_status": status,
                "elapsed_seconds": elapsed_seconds,
                "response": payload,
                "error": error or None,
            },
        )
        write_json(candidates_output_path, candidates)

        top = candidates[0]["record"] if candidates else {}
        top_score = candidates[0]["score"] if candidates else ""
        total_registros = payload.get("totalRegistros", "") if isinstance(payload, dict) else ""
        total_paginas = payload.get("totalPaginas", "") if isinstance(payload, dict) else ""

        summary_rows.append(
            {
                "source_row": source_row,
                "municipio": row["municipio"],
                "uf": row["uf"],
                "numero_contrato": row["numero_contrato"],
                "cnpj": row["cnpj"],
                "query_url": query_url,
                "http_status": status,
                "elapsed_seconds": elapsed_seconds,
                "total_registros": total_registros,
                "total_paginas": total_paginas,
                "candidates_count": len(candidates),
                "top_score": top_score,
                "top_numero_controle_pncp": top.get("numeroControlePNCP", ""),
                "top_numero_controle_pncp_compra": top.get("numeroControlePNCPCompra", ""),
                "top_numero_contrato_empenho": top.get("numeroContratoEmpenho", ""),
                "raw_output_path": relative_or_blank(raw_output_path),
                "candidates_output_path": relative_or_blank(candidates_output_path),
                "error": error,
            }
        )

        print(
            f"source_row={source_row} status={status} "
            f"candidates={len(candidates)} elapsed={elapsed_seconds:.2f}s"
        )

    summary_path = args.processed_root / run_id / "match_summary.csv"
    write_summary(summary_path, summary_rows)
    print(f"Summary: {summary_path.relative_to(ROOT_DIR).as_posix()}")


if __name__ == "__main__":
    run()
