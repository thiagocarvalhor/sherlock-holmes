# CLI

Os scripts em `scripts/` são entradas operacionais para executar partes do pipeline.

## Relatório auditável unitário

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_report.py
```

Saídas locais:

```text
data/processed/reports/row67/audit_report.json
data/processed/reports/row67/audit_report.md
```

Opções relevantes:

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_report.py `
  --input data\processed\comparison\row67\record_comparison.json `
  --documents caminho\documents.json `
  --cnpj-enrichment caminho\cnpj_enrichments.json
```

## Relatório auditável consolidado

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_batch_report.py
```

Saídas locais:

```text
data/processed/reports/batch/audit_batch_report.json
data/processed/reports/batch/audit_batch_report.md
```

## Processamento documental

```powershell
.\.venv\Scripts\python.exe .\scripts\process_document_text.py --input caminho\documento.pdf --run-id exemplo
```

## Observação

Na reestruturação arquitetural, os scripts devem virar wrappers finos chamando casos de uso em `application/use_cases`.
