# CLI

Os scripts em `scripts/` sao entradas operacionais para executar partes do pipeline.

## Relatorio auditavel unitario

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_report.py
```

Saidas locais:

```text
data/processed/reports/row67/audit_report.json
data/processed/reports/row67/audit_report.md
```

Opcoes relevantes:

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_report.py `
  --input data\processed\comparison\row67\record_comparison.json `
  --documents caminho\documents.json `
  --cnpj-enrichment caminho\cnpj_enrichments.json
```

## Relatorio auditavel consolidado

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_batch_report.py
```

Saidas locais:

```text
data/processed/reports/batch/audit_batch_report.json
data/processed/reports/batch/audit_batch_report.md
```

## Processamento documental

```powershell
.\.venv\Scripts\python.exe .\scripts\process_document_text.py --input caminho\documento.pdf --run-id exemplo
```

## Observacao

Na reestruturacao arquitetural, os scripts devem virar wrappers finos chamando casos de uso em `application/use_cases`.
