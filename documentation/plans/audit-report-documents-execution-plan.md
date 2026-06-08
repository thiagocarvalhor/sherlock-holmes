# Plano de Execucao: Documentos Oficiais em Relatorios Auditaveis

## Objetivo

Incluir referencias de documentos oficiais PNCP nos relatorios auditaveis sem acoplar o modulo de relatorio a chamadas de rede.

## Escopo

### Inclui

- carregar JSON de referencias documentais;
- aceitar documentos oficiais em `build_audit_report`;
- registrar contagem de documentos no resumo unitario;
- renderizar documentos oficiais no Markdown;
- somar documentos oficiais no relatorio consolidado;
- permitir uso opcional de documentos nos scripts operacionais;
- validar com testes offline.

### Nao Inclui

- buscar documentos automaticamente no PNCP durante a geracao do relatorio;
- baixar arquivos;
- processar OCR;
- enriquecer CNPJ dentro do relatorio.

## Arquivos Esperados

- `src/sherlock_holmes/reporting/audit.py`
- `src/sherlock_holmes/reporting/__init__.py`
- `scripts/generate_audit_report.py`
- `scripts/generate_audit_batch_report.py`
- `tests/test_audit_report.py`
- `documentation/reports/audit-report-documents-001.md`

## Criterio de Conclusao

Dado um `record_comparison.json` e, opcionalmente, um JSON de documentos oficiais, o projeto deve gerar relatorio JSON/Markdown com candidatos, divergencias, campos para revisao e documentos oficiais vinculados.
