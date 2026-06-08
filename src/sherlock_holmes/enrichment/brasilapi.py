"""BrasilAPI CNPJ enrichment client."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from sherlock_holmes.pncp.ids import normalize_cnpj
from sherlock_holmes.validation.evidence import EvidenceRecord, evidence_from_official_api

BRASILAPI_CNPJ_BASE_URL = "https://brasilapi.com.br/api/cnpj/v1"
USER_AGENT = "sherlock-holmes-cnpj-enrichment/0.1"

RequestJsonFn = Callable[[str, int], Any]


class BrasilApiError(RuntimeError):
    """Raised when BrasilAPI returns a non-success response or invalid payload."""


@dataclass(frozen=True)
class BrasilApiCnpjRecord:
    """Normalized CNPJ enrichment result with raw payload preserved."""

    cnpj: str
    razao_social: str = ""
    nome_fantasia: str = ""
    cnae_fiscal: str = ""
    cnae_fiscal_descricao: str = ""
    municipio: str = ""
    uf: str = ""
    situacao_cadastral: str = ""
    data_inicio_atividade: str = ""
    capital_social: float | None = None
    socios: list[dict[str, Any]] = field(default_factory=list)
    source_url: str = ""
    collected_at: str = ""
    raw_payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full record, including raw payload."""

        return asdict(self)

    def standardized(self) -> dict[str, Any]:
        """Return the auditable fields used by comparison/reporting flows."""

        return {
            "cnpj": self.cnpj,
            "razao_social": self.razao_social,
            "nome_fantasia": self.nome_fantasia,
            "cnae_fiscal": self.cnae_fiscal,
            "cnae_fiscal_descricao": self.cnae_fiscal_descricao,
            "municipio": self.municipio,
            "uf": self.uf,
            "situacao_cadastral": self.situacao_cadastral,
            "data_inicio_atividade": self.data_inicio_atividade,
            "capital_social": self.capital_social,
            "socios_count": len(self.socios),
        }


def build_cnpj_url(cnpj: str, *, base_url: str = BRASILAPI_CNPJ_BASE_URL) -> str:
    """Build a BrasilAPI CNPJ URL from a masked or compact CNPJ."""

    return f"{base_url.rstrip('/')}/{normalize_cnpj(cnpj)}"


def request_json(url: str, timeout: int = 30) -> Any:
    """Request JSON from BrasilAPI."""

    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed public API URL.
            body = response.read()
            return json.loads(body.decode("utf-8")) if body else None
    except HTTPError as exc:
        body = exc.read()
        message = body.decode("utf-8", errors="replace") if body else str(exc)
        raise BrasilApiError(f"BrasilAPI HTTP {exc.code}: {message}") from exc
    except json.JSONDecodeError as exc:
        raise BrasilApiError(f"BrasilAPI returned invalid JSON: {exc}") from exc


def fetch_cnpj(
    cnpj: str,
    *,
    timeout: int = 30,
    request_fn: RequestJsonFn = request_json,
) -> BrasilApiCnpjRecord:
    """Fetch and normalize CNPJ data from BrasilAPI."""

    url = build_cnpj_url(cnpj)
    payload = request_fn(url, timeout)
    if not isinstance(payload, dict):
        raise BrasilApiError("BrasilAPI returned an unexpected CNPJ payload.")
    return record_from_payload(payload, source_url=url)


def record_from_payload(
    payload: dict[str, Any],
    *,
    source_url: str,
    collected_at: str | None = None,
) -> BrasilApiCnpjRecord:
    """Normalize a BrasilAPI CNPJ payload into the project record format."""

    cnpj = normalize_cnpj(str(payload.get("cnpj") or ""))
    return BrasilApiCnpjRecord(
        cnpj=cnpj,
        razao_social=str(payload.get("razao_social") or ""),
        nome_fantasia=str(payload.get("nome_fantasia") or ""),
        cnae_fiscal=str(payload.get("cnae_fiscal") or ""),
        cnae_fiscal_descricao=str(payload.get("cnae_fiscal_descricao") or ""),
        municipio=str(payload.get("municipio") or ""),
        uf=str(payload.get("uf") or ""),
        situacao_cadastral=str(
            payload.get("descricao_situacao_cadastral")
            or payload.get("situacao_cadastral")
            or ""
        ),
        data_inicio_atividade=str(payload.get("data_inicio_atividade") or ""),
        capital_social=_float_or_none(payload.get("capital_social")),
        socios=[socio for socio in payload.get("socios", []) if isinstance(socio, dict)],
        source_url=source_url,
        collected_at=collected_at or datetime.now(timezone.utc).isoformat(),
        raw_payload=dict(payload),
    )


def write_cnpj_record(record: BrasilApiCnpjRecord, *, output_path: Path) -> Path:
    """Persist one enriched CNPJ record as JSON."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(record.to_dict(), file, ensure_ascii=False, indent=2)
    return output_path


def evidence_from_cnpj_record(
    record: BrasilApiCnpjRecord,
    *,
    evidence_id: str | None = None,
) -> EvidenceRecord:
    """Create high-confidence official API evidence from a BrasilAPI record."""

    return evidence_from_official_api(
        evidence_id=evidence_id or f"brasilapi_cnpj_{record.cnpj}",
        source_url=record.source_url,
        method="brasilapi_cnpj_v1",
        value=record.standardized(),
        field_name="cnpj_enrichment",
        metadata={
            "cnpj": record.cnpj,
            "collected_at": record.collected_at,
            "raw_payload": record.raw_payload,
        },
    )


def _float_or_none(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None
