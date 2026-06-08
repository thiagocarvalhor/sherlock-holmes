# Plano de Execucao: Relatorio Auditavel de Comparacao

## Objetivo

Criar a primeira camada de relatorios auditaveis do Sherlock Holmes a partir dos resultados de comparacao manual versus PNCP.

## Escopo

### Inclui

- criar modulo `sherlock_holmes.reporting`;
- carregar JSON de comparacao de registros;
- calcular resumo auditavel;
- identificar melhor candidato;
- listar candidatos ranqueados;
- listar campos comparados do melhor candidato;
- separar divergencias e pendencias de revisao;
- gerar saida JSON;
- gerar saida Markdown;
- criar script operacional para o caso da linha `67`;
- validar com testes offline.

### Nao Inclui

- banco de dados;
- relatorio multi-linha;
- enriquecimento BrasilAPI embutido no relatorio;
- OCR/documentos processados no relatorio;
- interface Streamlit para exportacao.

## Arquivos Esperados

- `src/sherlock_holmes/reporting/__init__.py`
- `src/sherlock_holmes/reporting/audit.py`
- `scripts/generate_audit_report.py`
- `tests/test_audit_report.py`
- `documentation/reports/audit-report-001.md`

## Criterio de Conclusao

Dado um arquivo `record_comparison.json`, o projeto deve gerar um relatorio Markdown e um JSON com candidatos, melhor candidato, campos comparados, divergencias e recomendacao de proxima acao.
