# Relatorio: Selecao Explicavel de Contrato no Streamlit - Entrega 001

## Objetivo

Tornar explicavel o criterio de escolha do contrato na busca documental PNCP.

## Alteracoes Realizadas

Arquivos atualizados:

- `src/sherlock_holmes/webapp/views.py`
- `tests/test_app_render.py`

Arquivo criado:

- `tests/test_webapp_contract_selection.py`
- `documentation/plans/streamlit-contract-selection-execution-plan.md`

## Novo Comportamento

### Sem Linha Manual

O app deixa claro que a escolha do contrato e manual. A lista segue os contratos filtrados do PNCP e o usuario escolhe conscientemente o contrato a investigar.

### Com Linha Manual

A secao `Priorizacao pela planilha manual` permite escolher uma linha da planilha. Para cada contrato filtrado, o app executa a comparacao campo a campo ja existente e ordena a lista pelo maior score.

A tabela passa a exibir:

- `rank`;
- `score`;
- `status`;
- `matches`;
- identificadores e campos principais do contrato.

O seletor agora exibe score, status e quantidade de campos em match no label do contrato.

## Resultado Esperado Para a Busca de Belford Roxo

Com a priorizacao ligada para a linha `67`, os contratos de limpeza urbana deixam de depender apenas da ordem retornada pelo PNCP. A lista passa a ser ordenada pelo score contra a linha manual, e o criterio fica visivel para o usuario.

## Validacoes Executadas

- `ruff check .` - passou.
- `pytest` - 43 testes passaram.

## Observacoes

Esta entrega nao confirma automaticamente que um contrato e o correto. Ela melhora a ordenacao e a explicabilidade para apoiar a escolha humana antes da abertura dos documentos oficiais.
