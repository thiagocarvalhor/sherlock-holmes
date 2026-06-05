# Relatorio: Streamlit — Tela de Comparacao Manual vs PNCP — Entrega 001

## Objetivo

Adicionar uma pagina Streamlit para explorar visualmente os candidatos PNCP
ranqueados e o detalhe campo a campo do melhor candidato.

## Artefatos Criados

- `scripts/pages/comparacao_manual_pncp.py`

## Funcionalidades

### Cabecalho — Registro manual

Exibe em metricas os campos do registro manual:
CNPJ, municipio, UF, valor, numero de contrato, vigencias e objeto.

### Tabela de candidatos

Exibe os 22 candidatos PNCP ordenados por score decrescente com colunas:
`numero_controle_pncp`, `score`, `status`, `objeto`, `valor`, `vigencia_inicio`.

Status colorido via `Styler.map`:
- match         → verde
- partial_match → amarelo
- divergent     → vermelho
- missing_*     → cinza
- unresolved    → cinza

### Detalhe campo a campo

Seletor de candidato (com score exibido no label). Exibe `RecordComparison`
campo a campo com colunas: `campo`, `manual`, `oficial`, `status`, `score`.

### Sidebar

Campo de texto para informar caminho alternativo do JSON de comparacao.

## Validacoes Executadas

- compilacao com `compileall` sem erros;
- carregamento do JSON e styling pandas verificados fora do Streamlit (sem warnings);
- app Streamlit respondendo HTTP 200 com a pagina acessivel;
- correcao de `Styler.applymap` (deprecated) para `Styler.map`.

## Para Rodar

```bash
py -3 -m streamlit run scripts/pncp_streamlit_app.py
```

A pagina aparece na sidebar de navegacao como "comparacao manual pncp".
