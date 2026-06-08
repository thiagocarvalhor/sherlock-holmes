# Plano de Execucao: Enriquecimento CNPJ em Relatorios Auditaveis

## Objetivo

Incluir resultados de enriquecimento cadastral BrasilAPI nos relatorios auditaveis sem fazer chamadas de rede durante a geracao do relatorio.

## Escopo

### Inclui

- carregar JSON de enriquecimento CNPJ;
- aceitar enriquecimentos em `build_audit_report`;
- registrar contagem e CNPJs enriquecidos no resumo unitario;
- renderizar enriquecimentos CNPJ no Markdown;
- somar enriquecimentos no relatorio consolidado;
- permitir uso opcional nos scripts operacionais;
- validar com testes offline.

### Nao Inclui

- consultar BrasilAPI automaticamente;
- criar cache persistente;
- comparar socios ou CNAE contra dados manuais;
- tratar enriquecimento como prova de irregularidade.

## Arquivos Esperados

- `src/sherlock_holmes/reporting/audit.py`
- `src/sherlock_holmes/reporting/__init__.py`
- `scripts/generate_audit_report.py`
- `scripts/generate_audit_batch_report.py`
- `tests/test_audit_report.py`
- `documentation/reports/audit-report-cnpj-enrichment-001.md`

## Criterio de Conclusao

Dado um `record_comparison.json` e, opcionalmente, um JSON de enriquecimento BrasilAPI, o relatorio deve registrar CNPJ, razao social, situacao cadastral, municipio/UF, CNAE, quantidade de socios, fonte e data de coleta.
