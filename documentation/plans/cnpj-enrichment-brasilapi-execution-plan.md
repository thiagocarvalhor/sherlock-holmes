# Plano de Execucao: Enriquecimento de CNPJ via BrasilAPI

## Objetivo

Adicionar uma primeira camada de enriquecimento cadastral de CNPJ usando a BrasilAPI, mantendo fonte, data de coleta, payload bruto e campos padronizados.

## Escopo

### Inclui

- criar modulo `sherlock_holmes.enrichment`;
- consultar o endpoint publico de CNPJ da BrasilAPI;
- normalizar CNPJ antes da consulta;
- padronizar campos principais;
- preservar payload bruto;
- criar evidencia oficial de API a partir do enriquecimento;
- escrever resultado em JSON;
- validar comportamento com testes offline.

### Nao Inclui

- chamadas em massa;
- cache persistente;
- integracao visual no Streamlit;
- enriquecimento automatico de todos os candidatos;
- fallback para outras APIs.

## Endpoint de Referencia

```text
GET https://brasilapi.com.br/api/cnpj/v1/{cnpj}
```

## Arquivos Esperados

- `src/sherlock_holmes/enrichment/__init__.py`
- `src/sherlock_holmes/enrichment/brasilapi.py`
- `tests/test_brasilapi_enrichment.py`
- `documentation/reports/cnpj-enrichment-brasilapi-001.md`

## Criterio de Conclusao

Dado um CNPJ, o projeto deve conseguir montar a URL oficial, normalizar o identificador, transformar o payload em registro padronizado, salvar JSON e criar evidencia rastreavel.
