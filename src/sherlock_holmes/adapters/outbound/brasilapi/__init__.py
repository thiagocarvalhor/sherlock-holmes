"""Outbound BrasilAPI adapter package."""

from sherlock_holmes.adapters.outbound.brasilapi.client import (
    BRASILAPI_CNPJ_BASE_URL,
    BrasilApiCnpjRecord,
    BrasilApiError,
    build_cnpj_url,
    evidence_from_cnpj_record,
    fetch_cnpj,
    record_from_payload,
    request_json,
    write_cnpj_record,
)
from sherlock_holmes.adapters.outbound.brasilapi.cnpj_gateway import BrasilApiCnpjGateway

__all__ = [
    "BRASILAPI_CNPJ_BASE_URL",
    "BrasilApiCnpjGateway",
    "BrasilApiCnpjRecord",
    "BrasilApiError",
    "build_cnpj_url",
    "evidence_from_cnpj_record",
    "fetch_cnpj",
    "record_from_payload",
    "request_json",
    "write_cnpj_record",
]
