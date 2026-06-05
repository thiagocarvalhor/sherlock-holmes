# Relatorio: Redesign do App Streamlit (Investigacao ao Vivo) — Entrega 001

## Objetivo

Transformar o app de duas paginas desconectadas em um fluxo unico de
investigacao ao vivo, com abas no topo, cards e badges de status.

## Artefatos Criados

- `src/sherlock_holmes/investigation.py` — orquestracao reutilizavel:
  `load_manual_rows`, `build_search_window`, `investigate_row`,
  `InvestigationResult`. `fetch_fn` injetavel (testavel offline).
- `src/sherlock_holmes/webapp/views.py` — `render_comparacao_tab`,
  `render_busca_tab`, `cached_investigate_row`.
- `tests/test_investigation.py` — 5 testes offline.

## Artefatos Atualizados

- `src/sherlock_holmes/webapp/ui.py` — `inject_css`, `status_badge`,
  `field_row_html` (badges-pill e linhas de comparacao em HTML).
- `src/sherlock_holmes/webapp/comparison.py` — helpers baseados em
  `RecordComparison`: `candidates_dataframe`, `match_count`, `MANUAL_FIELDS`,
  `candidate_detail_url`.
- `scripts/pncp_streamlit_app.py` — entry fino: `inject_css` + `st.tabs`.

## Artefatos Removidos

- `scripts/pages/` — fim do multipage por sidebar; navegacao agora por abas.

## Fluxo de Investigacao ao Vivo

```text
linha da planilha (CONSOLIDADO / sample) 
  -> build_search_window (vigencia_inicio +/- 45 dias)
  -> fetch_contracts_by_publication (PNCP, paginado)
  -> compare_records em cada candidato
  -> ranking por score + melhor candidato
```

A logica vive no pacote (`investigation.py`), nao na UI. A UI apenas chama
`cached_investigate_row` e renderiza.

## Estetica

- Abas no topo (`st.tabs`): "⚖️ Comparação" e "🔍 Busca PNCP".
- Badges-pill coloridos por status (match/parcial/divergente/cinza) via CSS unico.
- Cards (`st.container(border=True)`): registro manual, melhor candidato.
- Metricas-resumo: candidatos avaliados, melhor score, campos coincidentes.
- Detalhe campo a campo como linhas HTML (manual -> oficial + badge).

## Validacoes Executadas

- `ruff check .` — **All checks passed**;
- `pytest` — **38 testes verdes** (5 novos de investigation);
- investigacao ao vivo da linha 67 (chamada real ao PNCP):
  - 22 candidatos avaliados;
  - melhor: `39485438000142-2-000019/2025`;
  - score 0.85, status `partial_match`;
- app Streamlit sobe headless (HTTP 200, healthz ok).

## Para Rodar

```bash
.venv/Scripts/python.exe -m streamlit run scripts/pncp_streamlit_app.py
```

## Notas

- O CSV manual default e o sample commitado
  (`documentation/plans/pncp-api-smoke-sample.csv`, 5 linhas incluindo a 67).
  O campo na sidebar aceita o manifest completo quando gerado.
- `scripts/compare_row67.py` e `scripts/fetch_row67_pages.py` permanecem como
  smokes; a logica equivalente agora vive em `investigation.py`.
