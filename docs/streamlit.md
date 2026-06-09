# Streamlit

O Streamlit é a interface de investigação do Sherlock Holmes.

A implementação da interface fica em:

```text
src/sherlock_holmes/adapters/inbound/streamlit/
```

O arquivo `scripts/pncp_streamlit_app.py` é um wrapper fino para preservar o comando local.

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

## Deploy no Streamlit Community Cloud

O app publicado deve apontar para:

```text
Repository: thiagocarvalhor/sherlock-holmes
Branch: main
Main file path: streamlit_app.py
Python: 3.10
```

O arquivo `streamlit_app.py` existe para compatibilidade com o padrao do
Streamlit Cloud. Ele chama o mesmo entrypoint usado localmente pelo wrapper
`scripts/pncp_streamlit_app.py`.

As dependencias do deploy ficam em `requirements.txt`, que instala o pacote
local com o extra `webapp`. O arquivo `requirements-streamlit.txt` aponta para
a mesma instalacao para preservar compatibilidade com o deploy antigo.

## Decisões importantes

- A busca PNCP vem antes da comparação.
- A busca de contratos PNCP chama `application.use_cases.search_pncp_contracts` com adapter outbound.
- A comparação usa a linha manual apenas para priorizar e justificar candidatos.
- A investigação automática chama `application.use_cases.investigate_manual_row` usando o mesmo gateway PNCP de contratos.
- A comparação direta com o contrato selecionado chama `application.use_cases.compare_manual_record`.
- A indicação de revisão documental e OCR chama `application.use_cases.prepare_review`.
- A listagem de arquivos oficiais chama `application.use_cases.list_contract_documents`.
- A BrasilAPI é consultada sob demanda via `application.use_cases.enrich_cnpj` com adapter outbound.
- OCR não é executado pela UI nesta fase.
- O indicador `Pode precisar OCR` é operacional, não uma execução real de OCR.
- Status e notas de revisão ainda ficam na sessão Streamlit.

## Arquivo de entrada

Por padrão, a UI usa:

```text
documentation/plans/pncp-api-smoke-sample.csv
```

Esse arquivo pode ser trocado na própria interface.
