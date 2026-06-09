# Streamlit

O Streamlit é a interface de investigação do Sherlock Holmes.

## Fluxo principal

```text
1. Buscar documentos e contratos PNCP.
2. Escolher ou ranquear um contrato.
3. Comparar com uma linha manual.
4. Consultar CNPJ via BrasilAPI sob demanda.
5. Registrar status e notas de revisão.
6. Exportar relatório auditável em Markdown ou JSON.
```

## Comando

```powershell
.\.venv\Scripts\python.exe -m streamlit run scripts\pncp_streamlit_app.py
```

## Decisões importantes

- A busca PNCP vem antes da comparação.
- A comparação usa a linha manual apenas para priorizar e justificar candidatos.
- A investigação automática chama o caso de uso `application.use_cases.investigate_manual_row`.
- A comparação direta com o contrato selecionado chama `application.use_cases.compare_manual_record`.
- A indicação de revisão documental e OCR chama `application.use_cases.prepare_review`.
- A listagem de arquivos oficiais chama `application.use_cases.list_contract_documents`.
- A BrasilAPI é consultada sob demanda via `application.use_cases.enrich_cnpj`.
- OCR não é executado pela UI nesta fase.
- O indicador `Pode precisar OCR` é operacional, não uma execução real de OCR.
- Status e notas de revisão ainda ficam na sessão Streamlit.

## Arquivo de entrada

Por padrão, a UI usa:

```text
documentation/plans/pncp-api-smoke-sample.csv
```

Esse arquivo pode ser trocado na própria interface.
