# Relatorio: Relatorio Auditavel de Comparacao - Entrega 001

## Objetivo

Criar a primeira camada de relatorios auditaveis a partir dos resultados de comparacao manual versus PNCP.

## Artefatos Criados

- `src/sherlock_holmes/reporting/__init__.py`
- `src/sherlock_holmes/reporting/audit.py`
- `scripts/generate_audit_report.py`
- `tests/test_audit_report.py`
- `documentation/plans/audit-report-execution-plan.md`

## Funcionalidades

- carregar `record_comparison.json`;
- ordenar candidatos por score;
- identificar melhor candidato;
- calcular resumo de status;
- identificar campos que exigem revisao;
- identificar candidatos duplicados;
- gerar relatorio estruturado em JSON;
- gerar relatorio Markdown.

## Validacao Operacional

Script executado:

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_report.py
```

Artefatos gerados localmente:

- `data/processed/reports/row67/audit_report.json`
- `data/processed/reports/row67/audit_report.md`

Resultado:

- linha manual: `67`;
- candidatos avaliados: `22`;
- melhor candidato: `39485438000142-2-000019/2025`;
- score: `0.8500`;
- status: `partial_match`;
- proxima acao recomendada: revisar campos parciais/divergentes e documentos oficiais.

## Validacoes Automatizadas

- `ruff check .` - passou.
- `pytest` - 56 testes passaram.

## Observacoes

Os artefatos em `data/processed` continuam ignorados pelo Git. O modulo de relatorio e o script operacional sao versionados; os resultados gerados sao saidas de execucao.
