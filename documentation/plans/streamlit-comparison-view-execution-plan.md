# Plano de Execucao: Streamlit — Tela de Comparacao Manual vs PNCP

## Objetivo

Adicionar uma pagina Streamlit que carrega o resultado de comparacao
(`record_comparison.json`) e permite explorar visualmente os candidatos
PNCP ranqueados e o detalhe campo a campo do melhor candidato.

## Contexto

O app atual (`scripts/pncp_streamlit_app.py`) e uma pagina unica de busca
PNCP ao vivo. O Streamlit 1.45.1 ja suporta multi-page via diretorio `pages/`
ao lado do arquivo principal.

O artefato de entrada desta tela e o JSON gerado por `compare_row67.py`:

```text
data/processed/comparison/row67/record_comparison.json
```

## Escopo

### Inclui

- nova pagina `scripts/pages/comparacao_manual_pncp.py`;
- carregamento do JSON de comparacao via seletor de arquivo ou caminho fixo;
- tabela de candidatos ranqueados por score com coluna de status colorido;
- detalhe campo a campo do candidato selecionado com status colorido por linha;
- indicacao clara do registro manual (cabecalho da tela).

### Nao inclui

- enriquecimento BrasilAPI;
- edicao ou revisao humana via UI;
- busca ao vivo no PNCP a partir desta tela;
- persistencia de selecao.

## Estrutura de Arquivos

```text
scripts/
  pncp_streamlit_app.py        (existente — pagina principal)
  pages/
    comparacao_manual_pncp.py  (novo)
```

## Layout da Tela

```
[cabecalho] Comparacao Manual vs PNCP
[info box]  Linha 67 | CNPJ 39485438000142 | Belford Roxo/RJ

[tabela]    Candidatos ranqueados
            numero_controle | score | status | objeto | valor | vigencia_inicio

[detalhe]   Campo a campo do candidato selecionado
            campo | manual | oficial | status | score
```

Cores de status:
- match         → verde
- partial_match → amarelo
- divergent     → vermelho
- missing_*     → cinza
- unresolved    → cinza

## Status

Concluida.

## Resultado da Entrega

Arquivos criados:

- `scripts/pages/comparacao_manual_pncp.py`

Relatorio:

- `documentation/reports/streamlit-comparison-view-001.md`

## Criterio de Conclusao

- pagina acessivel no Streamlit via sidebar de navegacao;
- tabela de candidatos exibida com score e status;
- selecao de candidato exibe comparacao campo a campo colorida;
- sem erros ao carregar o JSON da linha 67.
