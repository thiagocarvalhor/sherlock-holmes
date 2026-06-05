# Plano de Execucao: Refatoracao do App Streamlit + Link entre Paginas

## Objetivo

Separar responsabilidades do app Streamlit em modulos reutilizaveis e adicionar
navegacao entre a pagina de busca PNCP e a pagina de comparacao manual.

## Contexto

O app atual (`scripts/pncp_streamlit_app.py`) mistura constantes, logica de
dados, cache e UI em 255 linhas. Com mais paginas chegando (BrasilAPI, revisao
documental, relatorios), essa estrutura vai dificultar manutencao e reuso.

A pagina `pages/comparacao_manual_pncp.py` tambem tem logica de carregamento
e helpers embutidos. Nao ha link entre as duas paginas.

## Estrutura Proposta

```text
scripts/
  pncp_streamlit_app.py          (pagina principal — so UI)
  pages/
    comparacao_manual_pncp.py    (pagina de comparacao — so UI)
  app/
    __init__.py
    pncp.py                      (constantes, helpers e cache PNCP)
    comparison.py                (carregamento, parsing e helpers de comparacao)
    ui.py                        (componentes visuais compartilhados)
```

## O Que Vai Para Cada Modulo

### app/pncp.py
- `KEYWORD_SUGGESTIONS`
- `PRESET_ORGAOS`
- `TABLE_COLUMNS`
- `normalize_topic_key()`
- `suggested_terms()`
- `records_to_dataframe()`
- `record_label()`
- `cached_contract_search()`
- `cached_contract_files()`

### app/comparison.py
- `DEFAULT_COMPARISON_JSON`
- `load_comparison()`
- `build_candidates_df()`
- `build_fields_df()`
- `_field_value()`
- `_manual_info()`
- `parse_numero_controle_pncp()` — extrai cnpj, ano e sequencial de
  `"39485438000142-2-000019/2025"` para montar a URL de detalhe

### app/ui.py
- `STATUS_COLORS`
- `STATUS_LABELS`
- `color_status()`

## Link entre Paginas

### Na pagina de comparacao
- Botao `st.link_button("Abrir no PNCP", detail_url)` no detalhe do candidato
  selecionado, usando `parse_numero_controle_pncp` + `contract_detail_url`

### Na pagina principal (sidebar)
- `st.page_link("pages/comparacao_manual_pncp.py", label="Comparacao Manual vs PNCP")`

## Arquivos a Criar ou Ajustar

```text
scripts/app/__init__.py                (novo — vazio)
scripts/app/pncp.py                    (novo)
scripts/app/comparison.py             (novo)
scripts/app/ui.py                      (novo)
scripts/pncp_streamlit_app.py         (refatorar — importar de app/)
scripts/pages/comparacao_manual_pncp.py (refatorar — importar de app/ + link)
```

## Status

Concluida.

## Resultado da Entrega

Arquivos criados:

- `scripts/app/__init__.py`
- `scripts/app/pncp.py`
- `scripts/app/comparison.py`
- `scripts/app/ui.py`

Arquivos atualizados:

- `scripts/pncp_streamlit_app.py`
- `scripts/pages/comparacao_manual_pncp.py`

Relatorio:

- `documentation/reports/streamlit-refactor-001.md`

## Criterio de Conclusao

- app sobe sem erros;
- pagina principal funciona igual ao estado anterior;
- pagina de comparacao funciona igual ao estado anterior;
- botao "Abrir no PNCP" aparece no detalhe do candidato selecionado;
- link "Comparacao Manual vs PNCP" aparece na sidebar da pagina principal;
- sem logica de negocio ou dados dentro dos arquivos de pagina.
