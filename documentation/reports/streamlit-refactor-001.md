# Relatorio: Refatoracao Streamlit + Link entre Paginas — Entrega 001

## Objetivo

Separar responsabilidades do app Streamlit em modulos reutilizaveis e adicionar
navegacao entre a pagina de busca PNCP e a pagina de comparacao manual.

## Artefatos Criados

- `scripts/app/__init__.py`
- `scripts/app/pncp.py` — constantes, helpers e cache PNCP
- `scripts/app/comparison.py` — carregamento, parsing e helpers de comparacao
- `scripts/app/ui.py` — STATUS_COLORS, STATUS_LABELS, color_status

## Artefatos Atualizados

- `scripts/pncp_streamlit_app.py` — importa de `app/pncp.py`, link para comparacao
- `scripts/pages/comparacao_manual_pncp.py` — importa de `app/`, link para explorador,
  botao "Abrir no PNCP" por candidato

## Links Adicionados

### Pagina principal → Comparacao
`st.page_link("pages/comparacao_manual_pncp.py", ...)` na sidebar da pagina principal.

### Pagina de comparacao → Explorador
`st.page_link("pncp_streamlit_app.py", ...)` na sidebar da pagina de comparacao.

### Pagina de comparacao → PNCP portal
`st.link_button("Abrir no PNCP", detail_url)` no detalhe do candidato selecionado.
URL construida via `parse_numero_controle_pncp()` + `contract_detail_url()`.

Exemplo validado:
`39485438000142-2-000019/2025` → `https://pncp.gov.br/api/pncp/v1/orgaos/39485438000142/contratos/2025/19`

## Validacoes Executadas

- compilacao com `compileall` sem erros para todos os arquivos;
- parsing de `numeroControlePNCP` validado para casos validos e invalido;
- URL de detalhe gerada igual ao padrao do app existente.
