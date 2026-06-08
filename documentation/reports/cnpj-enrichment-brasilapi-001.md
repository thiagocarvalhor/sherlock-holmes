# Relatorio: Enriquecimento de CNPJ via BrasilAPI - Entrega 001

## Objetivo

Adicionar uma primeira camada de enriquecimento cadastral de CNPJ usando a BrasilAPI.

## Referencia de API

Endpoint usado:

```text
GET https://brasilapi.com.br/api/cnpj/v1/{cnpj}
```

A referencia foi conferida na documentacao publica da BrasilAPI antes da implementacao.

## Artefatos Criados

- `src/sherlock_holmes/enrichment/__init__.py`
- `src/sherlock_holmes/enrichment/brasilapi.py`
- `tests/test_brasilapi_enrichment.py`
- `documentation/plans/cnpj-enrichment-brasilapi-execution-plan.md`

## Funcionalidades

- `build_cnpj_url` normaliza CNPJ e monta a URL oficial.
- `request_json` faz request JSON com `urllib`, sem dependencia nova.
- `fetch_cnpj` consulta a BrasilAPI e retorna um registro padronizado.
- `record_from_payload` transforma payload bruto em `BrasilApiCnpjRecord`.
- `write_cnpj_record` grava o resultado em JSON.
- `evidence_from_cnpj_record` cria evidencia `official_api` com confianca `high`.

## Campos Padronizados

- CNPJ;
- razao social;
- nome fantasia;
- CNAE fiscal;
- descricao do CNAE;
- municipio;
- UF;
- situacao cadastral;
- data de inicio de atividade;
- capital social;
- quantidade de socios.

O payload bruto e preservado em `raw_payload`.

## Validacoes Executadas

- `ruff check .` - passou.
- `pytest` - 48 testes passaram.

## Observacoes

A validacao automatizada foi offline, com `request_fn` injetavel. A entrega nao adiciona chamadas em massa, cache persistente ou interface Streamlit para enriquecimento.
