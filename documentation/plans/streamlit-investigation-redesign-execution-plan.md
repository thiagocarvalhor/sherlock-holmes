# Plano de Execucao: Redesign do App Streamlit (Fluxo de Investigacao ao Vivo)

## Objetivo

Transformar o app Streamlit de duas paginas desconectadas em um fluxo unico de
investigacao ao vivo, com navegacao por abas, cards e badges de status.

Decisoes do usuario:
- **Integracao**: fluxo ao vivo — escolher linha da planilha -> busca PNCP
  automatica -> comparacao na hora.
- **Estetica**: abas no topo + cards e badges.

## Contexto

Hoje:
- `scripts/pncp_streamlit_app.py` faz busca PNCP ao vivo (pagina principal);
- `scripts/pages/comparacao_manual_pncp.py` so le um JSON pre-calculado da linha 67;
- as duas nao se conversam; navegacao via sidebar multipage.

Pecas reutilizaveis ja existentes:
- `sherlock_holmes.pncp.client.fetch_contracts_by_publication` (busca paginada);
- `sherlock_holmes.validation.compare_records` (comparacao completa);
- `sherlock_holmes.validation.evidence_*` (evidencias);
- CSV manual commitado: `documentation/plans/pncp-api-smoke-sample.csv` (5 linhas,
  inclui a linha 67).

## Arquitetura Proposta

### Backend (nucleo reutilizavel e testavel)

`src/sherlock_holmes/investigation.py` (novo):
- `load_manual_rows(csv_path) -> list[dict]` — le o CSV manual;
- `build_search_window(manual_row, window_days=45) -> tuple[date, date]` —
  janela de datas a partir de `vigencia_inicio` (fallback para o ano);
- `InvestigationResult` (dataclass) — `manual_row`, `query_url`,
  `candidates_count`, `comparisons: list[RecordComparison]` (ranqueada), `best`;
- `investigate_row(manual_row, *, fetch_fn=fetch_contracts_by_publication,
  window_days=45, page_size=500, max_pages=20) -> InvestigationResult` —
  busca candidatos, roda `compare_records` em cada, ranqueia por score.
  `fetch_fn` injetavel para testes offline (sem rede).

### Webapp (UI)

`src/sherlock_holmes/webapp/views.py` (novo):
- `render_busca_tab()` — explorador PNCP ao vivo (atual, polido);
- `render_comparacao_tab()` — seletor de linha manual -> botao Investigar ->
  cards de candidatos ranqueados + detalhe campo a campo com badges.

`src/sherlock_holmes/webapp/ui.py` (expandir):
- `inject_css()` — CSS unico (badges-pill, cards);
- `status_badge(status) -> str` (HTML);
- helpers de card/metrica.

`src/sherlock_holmes/webapp/pncp.py` e `comparison.py`: mantidos/adaptados;
adicionar `cached_investigate_row` (wrapper `st.cache_data`).

### Entry script (fino)

`scripts/pncp_streamlit_app.py`:
- `set_page_config`, `inject_css()`, `st.tabs(["🔍 Busca", "⚖️ Comparação"])`
  chamando as views. Sem logica de negocio.

`scripts/pages/` — **removido** (troca de multipage-sidebar para abas no topo).

## Estrutura Final

```text
src/sherlock_holmes/
  investigation.py        (novo — orquestracao busca+comparacao)
  webapp/
    __init__.py
    ui.py                 (expandido — css, badges, cards)
    pncp.py               (+ cached_investigate_row)
    comparison.py         (helpers de exibicao, adaptado)
    views.py              (novo — render_busca_tab, render_comparacao_tab)
scripts/
  pncp_streamlit_app.py   (fino — tabs -> views)
  (pages/ removido)
```

## Estetica

- Abas no topo via `st.tabs`.
- Status como badges-pill coloridos (match=verde, partial=amarelo,
  divergent=vermelho, missing/unresolved=cinza), via CSS injetado uma vez.
- Cards com `st.container(border=True)` agrupando registro manual, candidato e
  detalhe.
- Metricas-resumo (nº candidatos, melhor score, campos em match) no topo da aba.

## Testes

`tests/test_investigation.py`:
- `build_search_window` — janela correta a partir de `vigencia_inicio`;
- `investigate_row` com `fetch_fn` falso (candidatos sinteticos, incluindo o
  vencedor da linha 67) — assert ranking, best score e status;
- `load_manual_rows` — le o CSV sample commitado e acha a linha 67.

CI permanece offline: testes nao tocam a rede (fetch_fn injetado; load_manual_rows
usa o CSV commitado).

## Validacao Manual/Tecnica

- `pytest` verde (incluindo novos testes);
- `ruff check .` limpo;
- app sobe headless (HTTP 200);
- investigacao ao vivo da linha 67 retorna `39485438000142-2-000019/2025`
  como melhor candidato (score ~0.85, partial_match);
- abas Busca e Comparacao funcionais; badges e cards renderizando.

## Status

Concluida.

## Resultado da Entrega

Modulo `investigation.py` (orquestracao reutilizavel e testavel), `webapp/views.py`
(abas), `webapp/ui.py` expandido (css/badges/cards), entry script fino com
`st.tabs`, `scripts/pages/` removido. 38 testes verdes, ruff limpo, investigacao
ao vivo da linha 67 confirmada (22 candidatos, melhor `...000019/2025`, 0.85).

Detalhes em `documentation/reports/streamlit-investigation-redesign-001.md`.

## Criterio de Conclusao

- fluxo ao vivo: escolher linha -> investigar -> ver candidatos ranqueados e
  detalhe campo a campo, tudo na hora;
- navegacao por abas no topo;
- logica de orquestracao no pacote (`investigation.py`), nao na UI;
- entry script fino;
- testes, ruff e validacao do app verdes.
```
