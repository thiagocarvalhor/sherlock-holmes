# Plano de Execucao: Selecao Explicavel de Contrato no Streamlit

## Objetivo

Melhorar a etapa de selecao de contrato na busca documental do Streamlit, evitando que o contrato escolhido pareca ser definido por um criterio invisivel.

## Problema

Na versao documento-primeiro, o campo `Selecionado` mostrava o primeiro item da lista filtrada. Isso era tecnicamente correto, mas pouco explicativo: o usuario podia interpretar que o sistema havia escolhido automaticamente o melhor contrato.

## Escopo

### Inclui

- trocar o texto `Selecionado` por `Contrato escolhido`;
- deixar claro quando a escolha e manual;
- permitir priorizacao opcional por uma linha da planilha manual;
- calcular score de comparacao para cada contrato filtrado quando houver linha manual;
- ordenar contratos por maior score quando a priorizacao estiver ligada;
- mostrar rank, score, status e quantidade de campos em match na tabela;
- reaproveitar a comparacao calculada na busca dentro da secao de comparacao manual;
- adicionar testes offline do ranking.

### Nao Inclui

- alterar a regra de scoring do nucleo;
- alterar filtros PNCP;
- baixar documentos automaticamente;
- confirmar correspondencia sem revisao humana.

## Criterio de Conclusao

O app deve permitir entender por que um contrato aparece no topo:

- sem linha manual: escolha manual sobre a lista filtrada;
- com linha manual: ranking por score de comparacao campo a campo.
