# Plano de Execucao: Paginacao PNCP — Linha 67

## Objetivo

Buscar as paginas 2 e 3 da consulta PNCP da linha 67 para cobrir todos os 22
contratos do orgao e identificar o contrato de limpeza urbana
(02/SEMSEP/2025/2025, R$ 52.801.942,27) que nao apareceu na pagina 1.

## Contexto

A entrega anterior (`record-comparison-001`) confirmou que nenhum dos 10
candidatos da pagina 1 corresponde ao registro manual. A API retornou
`totalRegistros=22` e `totalPaginas=3`. Os parametros da consulta original
estao salvos em:

```text
data/raw/pncp/pncp-refactor-live-row67/contracts/source_row_67.json
```

## Escopo

### Inclui

- script `scripts/fetch_row67_pages.py` que le os params salvos e busca as
  paginas 2 e 3, salvando cada resposta em arquivo separado;
- atualizacao de `scripts/compare_row67.py` para carregar todas as paginas
  disponíveis e comparar os 22 candidatos;
- saida atualizada em `data/processed/comparison/row67/`;
- relatorio em `documentation/reports/pncp-pagination-row67-001.md`.

### Nao inclui

- mudanca na logica de comparacao (`compare_records`);
- paginacao generica para outras linhas;
- interface Streamlit.

## Arquivos a Criar ou Ajustar

```text
scripts/fetch_row67_pages.py              (novo)
scripts/compare_row67.py                  (atualizar para multi-pagina)
data/raw/pncp/pncp-refactor-live-row67/contracts/source_row_67_page2.json  (gerado)
data/raw/pncp/pncp-refactor-live-row67/contracts/source_row_67_page3.json  (gerado)
```

## Status

Concluida.

## Resultado da Entrega

Arquivos criados:

- `scripts/fetch_row67_pages.py`

Arquivos atualizados:

- `scripts/compare_row67.py`

Arquivos gerados:

- `data/raw/pncp/pncp-refactor-live-row67/contracts/source_row_67_page2.json`
- `data/raw/pncp/pncp-refactor-live-row67/contracts/source_row_67_page3.json`
- `data/processed/comparison/row67/record_comparison.json`
- `data/processed/comparison/row67/record_comparison.csv`

Relatorio:

- `documentation/reports/pncp-pagination-row67-001.md`

## Criterio de Conclusao

- `fetch_row67_pages.py` buscar e salvar paginas 2 e 3 sem excecao;
- `compare_row67.py` comparar os 22 candidatos e identificar o melhor;
- se o contrato de limpeza urbana existir no PNCP, aparecer com score superior
  a qualquer candidato da pagina 1;
- artefatos JSON e CSV atualizados em `data/processed/comparison/row67/`;
- relatorio registrado.
