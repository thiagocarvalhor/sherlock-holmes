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
- A BrasilAPI é consultada sob demanda, não automaticamente.
- OCR não é executado pela UI nesta fase.
- O indicador `Pode precisar OCR` é operacional, não uma execução real de OCR.
- Status e notas de revisão ainda ficam na sessão Streamlit.

## Arquivo de entrada

Por padrão, a UI usa:

```text
documentation/plans/pncp-api-smoke-sample.csv
```

Esse arquivo pode ser trocado na própria interface.
