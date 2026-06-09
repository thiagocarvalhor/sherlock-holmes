# Relatórios auditáveis

Relatórios auditáveis são saídas estruturadas para revisão técnica.

## Conteúdo atual

Um relatório pode conter:

- resumo da comparação;
- candidatos avaliados;
- melhor candidato;
- campos comparados;
- campos para revisão;
- documentos oficiais vinculados;
- enriquecimentos CNPJ;
- status e notas de revisão quando exportado pelo Streamlit.

## Formatos

- JSON para consumo estruturado;
- Markdown para leitura e revisão humana.

## Gerar via script

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_report.py
.\.venv\Scripts\python.exe .\scripts\generate_audit_batch_report.py
```

## Gerar via Streamlit

Na tela de comparação:

1. selecione um contrato;
2. compare com uma linha manual;
3. revise status/notas;
4. clique em `Baixar Markdown` ou `Baixar JSON`.

## Decisão

O relatório não acusa automaticamente irregularidade. Ele organiza evidências e divergências para revisão.
