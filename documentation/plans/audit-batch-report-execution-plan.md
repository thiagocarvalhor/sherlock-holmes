# Plano de Execucao: Relatorio Auditavel Multi-linha

## Objetivo

Evoluir o relatorio auditavel para consolidar varias linhas manuais em uma saida unica.

## Escopo

### Inclui

- construir relatorio batch a partir de multiplos `record_comparison.json`;
- gerar resumo consolidado de linhas e candidatos;
- listar uma linha por investigacao com melhor candidato, score e status;
- destacar linhas que exigem revisao;
- gerar JSON e Markdown consolidados;
- criar script operacional que varre `data/processed/comparison`;
- validar com testes offline.

### Nao Inclui

- reexecutar buscas PNCP;
- enriquecer CNPJ automaticamente;
- incluir documentos/OCR;
- resolver duplicatas;
- dashboard Streamlit de exportacao.

## Arquivos Esperados

- `src/sherlock_holmes/reporting/audit.py`
- `src/sherlock_holmes/reporting/__init__.py`
- `scripts/generate_audit_batch_report.py`
- `tests/test_audit_report.py`
- `documentation/reports/audit-batch-report-001.md`

## Criterio de Conclusao

Dado um diretorio com um ou mais `record_comparison.json`, o projeto deve gerar um relatorio consolidado em JSON e Markdown com resumo geral e status por linha manual.
