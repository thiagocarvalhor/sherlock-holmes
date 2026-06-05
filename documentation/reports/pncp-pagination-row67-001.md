# Relatorio: Paginacao PNCP Linha 67 — Entrega 001

## Objetivo

Buscar as paginas 2 e 3 da consulta PNCP da linha 67 para cobrir todos os 22
contratos e identificar o contrato de limpeza urbana que nao apareceu na pagina 1.

## Artefatos Criados

- `scripts/fetch_row67_pages.py` — busca e salva paginas adicionais
- `scripts/compare_row67.py` — atualizado para multi-pagina
- `data/raw/pncp/pncp-refactor-live-row67/contracts/source_row_67_page2.json`
- `data/raw/pncp/pncp-refactor-live-row67/contracts/source_row_67_page3.json`
- `data/processed/comparison/row67/record_comparison.json` (atualizado)
- `data/processed/comparison/row67/record_comparison.csv` (atualizado)

## Resultado da Validacao

### Paginas buscadas

| Pagina | Status HTTP | Contratos |
|--------|-------------|-----------|
| 1      | ja salvo    | 10        |
| 2      | 200         | 10        |
| 3      | 200         | 2         |

Total: 22 candidatos avaliados.

### Melhor candidato: 39485438000142-2-000019/2025

Score: 0.8500 — Status: `partial_match`

| campo           | status        | score | manual                   | oficial                                |
|-----------------|---------------|-------|--------------------------|----------------------------------------|
| cnpj            | match         | 1.00  | 39485438000142           | 39485438000142                         |
| municipio       | match         | 1.00  | Belford Roxo             | Belford Roxo                           |
| uf              | match         | 1.00  | RJ                       | RJ                                     |
| valor_contrato  | match         | 1.00  | 52801942.27              | 52801942.27                            |
| vigencia_inicio | match         | 1.00  | 2025-11-04               | 2025-11-04                             |
| vigencia_fim    | match         | 1.00  | 2026-11-03               | 2026-11-03                             |
| numero_contrato | partial_match | 0.80  | 02/SEMSEP/2025/2025      | 02/SEMSEP/2025                         |
| objeto_contrato | divergent     | 0.00  | LIMPEZA URBANA E MANEJO  | CONTRATACAO DE EMPRESA... (descricao longa) |

### Interpretacao

O contrato foi encontrado na pagina 2. Os campos financeiros e temporais
batem exatamente (valor R$ 52.801.942,27, vigencias identicas). O numero
de contrato difere por um sufixo extra na planilha manual (`/2025/2025` vs
`/2025`) — provavel variante de entrada de dados.

O objeto_contrato diverge porque a planilha manual traz uma descricao resumida
(`LIMPEZA URBANA E MANEJO DE RESIDUOS`) enquanto o PNCP registra a descricao
completa do objeto. A comparacao texto nao detecta a relacao de contencao
porque o texto do PNCP nao contem a abreviacao da planilha como substring exata.

### Observacao sobre duplicatas

Os contratos `39485438000142-2-000012/2025` e `39485438000142-2-000009/2025`
aparecem duas vezes no conjunto (paginas 1 e 2 sobrepostas). Nao afeta o
resultado final porque o candidato correto nao esta duplicado.

## Validacoes Executadas

- compilacao com `compileall` sem erros;
- `fetch_row67_pages.py` buscou e salvou paginas 2 e 3 com status HTTP 200;
- `compare_row67.py` carregou 22 candidatos e gerou JSON e CSV atualizados;
- melhor candidato identificado com score 0.85 e campos financeiros/temporais
  em `match` exato.

## Proximo Passo

Avaliar se o status `partial_match` para `numero_contrato` e `objeto_contrato`
e aceitavel como identificacao confirmada, ou se exige revisao documental.
Candidato natural para marcar como `human_reviewed` apos inspecao.
