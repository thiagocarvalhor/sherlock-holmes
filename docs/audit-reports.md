# Relatorios auditaveis

Relatorios auditaveis sao saidas estruturadas para revisao tecnica.

## Conteudo atual

Um relatorio pode conter:

- resumo da comparacao;
- candidatos avaliados;
- melhor candidato;
- campos comparados;
- campos para revisao;
- documentos oficiais vinculados;
- enriquecimentos CNPJ;
- status e notas de revisao quando exportado pelo Streamlit.

## Formatos

- JSON para consumo estruturado;
- Markdown para leitura e revisao humana.

## Gerar via script

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_report.py
.\.venv\Scripts\python.exe .\scripts\generate_audit_batch_report.py
```

## Gerar via Streamlit

Na tela de comparacao:

1. selecione um contrato;
2. compare com uma linha manual;
3. revise status/notas;
4. clique em `Baixar Markdown` ou `Baixar JSON`.

## Decisao

O relatorio nao acusa automaticamente irregularidade. Ele organiza evidencias e divergencias para revisao.
