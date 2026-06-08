# Plano de Execucao: Enriquecimento CNPJ no Streamlit

## Objetivo

Integrar a camada BrasilAPI ao app Streamlit para permitir enriquecimento cadastral sob demanda do orgao contratante e do fornecedor do contrato escolhido.

## Escopo

### Inclui

- detectar CNPJs validos no contrato selecionado;
- oferecer orgao e fornecedor como alvos de enriquecimento;
- consultar BrasilAPI sob demanda;
- cachear a consulta no Streamlit;
- exibir campos padronizados e fonte;
- permitir inspecionar payload bruto;
- validar helpers offline.

### Nao Inclui

- enriquecimento automatico em massa;
- cache persistente em disco;
- exportacao de relatorio;
- enriquecimento de CPF;
- fallback para outra API.

## Criterio de Conclusao

Depois de selecionar um contrato PNCP, o usuario deve conseguir consultar os dados cadastrais de CNPJs disponiveis no contrato, com fonte e data de coleta visiveis.
