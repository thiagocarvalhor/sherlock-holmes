"""Fetch pages 2 and 3 of the PNCP contracts query for row 67."""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[5]
SOURCE_JSON = ROOT / "data/raw/pncp/pncp-refactor-live-row67/contracts/source_row_67.json"
OUT_DIR = ROOT / "data/raw/pncp/pncp-refactor-live-row67/contracts"

TIMEOUT = 30
DELAY_BETWEEN_PAGES = 2.0


def fetch_page(params: dict, page: int, timeout: int) -> tuple[int, dict, str]:
    page_params = {**params, "pagina": page}
    url = f"https://pncp.gov.br/api/consulta/v1/contratos?{urlencode(page_params)}"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "sherlock-holmes-pncp-smoke/0.1",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as resp:  # noqa: S310
            body = resp.read()
            return resp.status, json.loads(body.decode("utf-8")), url
    except HTTPError as exc:
        body = exc.read()
        try:
            parsed = json.loads(body.decode("utf-8")) if body else None
        except json.JSONDecodeError:
            parsed = body.decode("utf-8", errors="replace")
        return exc.code, parsed, url


def main() -> None:
    raw = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    original_params = raw["request"]["params"]
    total_pages = raw["response"]["totalPaginas"]

    base_params = {
        "dataInicial": original_params["dataInicial"],
        "dataFinal": original_params["dataFinal"],
        "tamanhoPagina": original_params["tamanhoPagina"],
        "cnpjOrgao": original_params["cnpjOrgao"],
    }

    print(f"Total de paginas: {total_pages}  |  Pagina 1 ja salva.")

    for page in range(2, total_pages + 1):
        out_path = OUT_DIR / f"source_row_67_page{page}.json"

        if out_path.exists():
            print(f"Pagina {page}: ja existe em {out_path.name}, pulando.")
            continue

        print(f"Buscando pagina {page}...", end=" ", flush=True)
        start = time.monotonic()
        status, data, url = fetch_page(base_params, page, TIMEOUT)
        elapsed = round(time.monotonic() - start, 3)
        print(f"status={status}  elapsed={elapsed}s")

        if status != 200 or not data:
            print(f"  ERRO na pagina {page}: status={status}")
            continue

        records_on_page = len(data.get("data", []))
        print(f"  {records_on_page} contratos retornados")

        payload = {
            "source_row": raw["source_row"],
            "page": page,
            "request": {
                "url": url,
                "params": {**base_params, "pagina": page},
            },
            "http_status": status,
            "elapsed_seconds": elapsed,
            "response": data,
        }
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  Salvo em {out_path.name}")

        if page < total_pages:
            time.sleep(DELAY_BETWEEN_PAGES)

    print("\nFetch concluido.")


if __name__ == "__main__":
    main()
