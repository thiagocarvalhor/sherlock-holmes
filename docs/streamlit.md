# Streamlit

O Streamlit e a interface de investigacao do Sherlock Holmes.

## Fluxo principal

```text
1. Buscar documentos e contratos PNCP.
2. Escolher ou ranquear um contrato.
3. Comparar com uma linha manual.
4. Consultar CNPJ via BrasilAPI sob demanda.
5. Registrar status e notas de revisao.
6. Exportar relatorio auditavel em Markdown ou JSON.
```

## Comando

```powershell
.\.venv\Scripts\python.exe -m streamlit run scripts\pncp_streamlit_app.py
```

## Decisoes importantes

- A busca PNCP vem antes da comparacao.
- A comparacao usa a linha manual apenas para priorizar e justificar candidatos.
- A BrasilAPI e consultada sob demanda, nao automaticamente.
- OCR nao e executado pela UI nesta fase.
- O indicador `Pode precisar OCR` e operacional, nao uma execucao real de OCR.
- Status e notas de revisao ainda ficam na sessao Streamlit.

## Arquivo de entrada

Por padrao, a UI usa:

```text
documentation/plans/pncp-api-smoke-sample.csv
```

Esse arquivo pode ser trocado na propria interface.
