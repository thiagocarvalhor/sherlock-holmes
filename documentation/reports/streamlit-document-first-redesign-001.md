# Relatorio: Streamlit Documento-Primeiro - Entrega 001

## Objetivo

Refatorar o app Streamlit para que a primeira experiencia seja a busca de documentos oficiais no PNCP, deixando a comparacao manual como segunda etapa.

## Alteracoes Realizadas

Arquivos atualizados:

- `scripts/pncp_streamlit_app.py`
- `src/sherlock_holmes/webapp/views.py`
- `src/sherlock_holmes/webapp/ui.py`
- `src/sherlock_holmes/webapp/pncp.py`
- `tests/test_app_render.py`

Arquivo criado:

- `documentation/plans/streamlit-document-first-redesign-execution-plan.md`

## Novo Fluxo

```text
Documentos PNCP
  -> escolher orgao/ano/tema
  -> buscar contratos
  -> selecionar contrato
  -> listar arquivos oficiais
  -> abrir contrato ou arquivo no PNCP

Comparacao manual
  -> escolher linha da planilha
  -> comparar com o contrato selecionado
  -> opcionalmente rodar investigacao automatica
```

## Decisoes de UX

- A pagina deixou de depender de abas como fluxo principal.
- A busca de documentos ficou no topo e funciona sem planilha manual.
- A comparacao aproveita o contrato selecionado na busca, reforcando o fluxo investigativo.
- A investigacao automatica foi mantida dentro de um expander para nao disputar foco com a comparacao direta.
- Labels e badges foram limpos para reduzir ruido visual.
- O preset `Prefeitura de Belford Roxo` foi adicionado para facilitar a validacao da linha `67`.

## Validacoes Executadas

- `ruff check .` - passou.
- `pytest` - 40 testes passaram.

## Observacoes

A entrega nao altera scoring, endpoints PNCP, download controlado, OCR ou regras de evidencia. A mudanca e focada na organizacao da interface.
