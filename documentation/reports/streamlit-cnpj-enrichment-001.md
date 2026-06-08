# Relatorio: Enriquecimento CNPJ no Streamlit - Entrega 001

## Objetivo

Conectar a camada BrasilAPI ao fluxo documento-primeiro do Streamlit.

## Alteracoes Realizadas

Arquivos atualizados:

- `src/sherlock_holmes/webapp/views.py`
- `tests/test_webapp_contract_selection.py`

Arquivo criado:

- `documentation/plans/streamlit-cnpj-enrichment-execution-plan.md`

## Novo Fluxo

```text
Contrato escolhido
  -> arquivos oficiais
  -> enriquecimento cadastral
      -> escolher CNPJ de orgao ou fornecedor
      -> consultar BrasilAPI sob demanda
      -> exibir campos padronizados, fonte e coleta
      -> inspecionar payload bruto
```

## Decisoes

- A consulta BrasilAPI e acionada por botao, nao automaticamente.
- Apenas identificadores com 14 digitos sao tratados como CNPJ.
- CPF ou identificador invalido de fornecedor e ignorado para enriquecimento.
- Resultado fica cacheado no Streamlit por 15 minutos.
- O payload bruto e exibido em expander para auditoria, sem poluir a tela principal.

## Campos Exibidos

- razao social;
- situacao cadastral;
- municipio/UF;
- socios;
- capital social;
- CNAE;
- data de inicio de atividade;
- fonte e timestamp de coleta.

## Validacoes Executadas

- `ruff check .` - passou.
- `pytest` - 51 testes passaram.

## Observacao Sobre Servidor Local

O app foi validado pela suite `streamlit.testing.v1.AppTest`. Ao tentar manter o Streamlit em background nesta sessao, o processo encerrou apos anunciar a URL; por isso nao houve validacao persistente de HTTP 200 nesta entrega.
