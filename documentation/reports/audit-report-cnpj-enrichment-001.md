# Relatorio: Enriquecimento CNPJ em Relatorios Auditaveis - Entrega 001

## Objetivo

Registrar a inclusao de resultados BrasilAPI CNPJ nos relatorios auditaveis.

## Artefatos Criados

- `documentation/plans/audit-report-cnpj-enrichment-execution-plan.md`

## Artefatos Atualizados

- `src/sherlock_holmes/reporting/audit.py`
- `src/sherlock_holmes/reporting/__init__.py`
- `scripts/generate_audit_report.py`
- `scripts/generate_audit_batch_report.py`
- `tests/test_audit_report.py`
- `documentation/projetos-similares/plano-execucao-roadmap-sherlock-holmes.md`

## Funcionalidades

- `load_cnpj_enrichments` carrega JSON de enriquecimento BrasilAPI;
- `build_audit_report` aceita `cnpj_enrichments`;
- o resumo unitario registra `cnpj_enrichments_count` e `enriched_cnpjs`;
- o Markdown unitario inclui a secao `Enriquecimento CNPJ`;
- o relatorio consolidado soma `total_cnpj_enrichments`;
- `scripts/generate_audit_report.py` aceita `--cnpj-enrichment`;
- `scripts/generate_audit_batch_report.py` aceita `--cnpj-enrichment-dir`.

## Campos Registrados

- `role`;
- `cnpj`;
- `razao_social`;
- `nome_fantasia`;
- `cnae_fiscal`;
- `cnae_fiscal_descricao`;
- `municipio`;
- `uf`;
- `situacao_cadastral`;
- `data_inicio_atividade`;
- `capital_social`;
- `socios_count`;
- `source_url`;
- `collected_at`.

## Validacoes Automatizadas

- `ruff check .` - passou.
- `pytest` - 61 testes passaram.

## Observacoes

Esta entrega nao consulta a BrasilAPI. Ela apenas consome registros ja coletados pela camada `sherlock_holmes.enrichment.brasilapi`, mantendo a geracao do relatorio offline, reprodutivel e auditavel.
