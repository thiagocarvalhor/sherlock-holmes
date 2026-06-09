"""Tests for BrasilAPI CNPJ enrichment helpers."""

from __future__ import annotations

import json

from sherlock_holmes.enrichment.brasilapi import (
    build_cnpj_url,
    evidence_from_cnpj_record,
    fetch_cnpj,
    record_from_payload,
    write_cnpj_record,
)


def _payload() -> dict:
    return {
        "cnpj": "39485438000142",
        "razao_social": "MUNICIPIO DE BELFORD ROXO",
        "nome_fantasia": "",
        "cnae_fiscal": 8411600,
        "cnae_fiscal_descricao": "Administracao publica em geral",
        "municipio": "BELFORD ROXO",
        "uf": "RJ",
        "descricao_situacao_cadastral": "ATIVA",
        "data_inicio_atividade": "1990-01-01",
        "capital_social": "0.00",
        "socios": [
            {"nome_socio": "PREFEITO TESTE", "qualificacao_socio": "Administrador"},
        ],
    }


def test_build_cnpj_url_normalizes_masked_cnpj():
    url = build_cnpj_url("39.485.438/0001-42")
    assert url == "https://brasilapi.com.br/api/cnpj/v1/39485438000142"


def test_record_from_payload_standardizes_main_fields():
    record = record_from_payload(
        _payload(),
        source_url="https://brasilapi.com.br/api/cnpj/v1/39485438000142",
        collected_at="2026-06-07T12:00:00+00:00",
    )
    assert record.cnpj == "39485438000142"
    assert record.razao_social == "MUNICIPIO DE BELFORD ROXO"
    assert record.cnae_fiscal == "8411600"
    assert record.situacao_cadastral == "ATIVA"
    assert record.capital_social == 0.0
    assert record.standardized()["socios_count"] == 1
    assert record.raw_payload["uf"] == "RJ"


def test_fetch_cnpj_uses_injected_request_function():
    calls = []

    def fake_request(url: str, timeout: int):
        calls.append((url, timeout))
        return _payload()

    record = fetch_cnpj("39.485.438/0001-42", timeout=7, request_fn=fake_request)
    assert record.cnpj == "39485438000142"
    assert calls == [("https://brasilapi.com.br/api/cnpj/v1/39485438000142", 7)]


def test_write_cnpj_record_roundtrip(tmp_path):
    record = record_from_payload(
        _payload(),
        source_url="https://brasilapi.com.br/api/cnpj/v1/39485438000142",
        collected_at="2026-06-07T12:00:00+00:00",
    )
    output_path = write_cnpj_record(record, output_path=tmp_path / "cnpj.json")
    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded["cnpj"] == "39485438000142"
    assert loaded["raw_payload"]["razao_social"] == "MUNICIPIO DE BELFORD ROXO"


def test_evidence_from_cnpj_record_is_official_api_evidence():
    record = record_from_payload(
        _payload(),
        source_url="https://brasilapi.com.br/api/cnpj/v1/39485438000142",
        collected_at="2026-06-07T12:00:00+00:00",
    )
    evidence = evidence_from_cnpj_record(record)
    assert evidence.source_type == "official_api"
    assert evidence.confidence_level == "high"
    assert evidence.method == "brasilapi_cnpj_v1"
    assert evidence.value["razao_social"] == "MUNICIPIO DE BELFORD ROXO"
    assert evidence.metadata["raw_payload"]["cnpj"] == "39485438000142"
