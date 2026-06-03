# Explorador PNCP em Streamlit

## Objetivo

Criar um aplicativo local para consultar contratos publicados no PNCP por órgão, ano e unidade administrativa opcional, com filtro temático por palavras-chave e acesso aos arquivos anexados de cada contrato.

## Artefatos

- `scripts/pncp_streamlit_app.py`: app Streamlit.
- `src/sherlock_holmes/pncp/client.py`: cliente simples para APIs públicas do PNCP.
- `requirements-streamlit.txt`: dependências do app.

## Fluxo implementado

1. Consulta contratos por data de publicação em `GET /api/consulta/v1/contratos`.
2. Pagina resultados até o limite configurado.
3. Filtra localmente o campo `objetoContrato` por palavras-chave.
4. Exibe tabela com identificadores, fornecedor, processo, valor, vigência e objeto.
5. Para um contrato selecionado, monta o endpoint direto de detalhe e consulta `GET /api/pncp/v1/orgaos/{cnpj}/contratos/{ano}/{sequencial}/arquivos`.
6. Exibe links clicáveis para os arquivos usando `https://pncp.gov.br/pncp-api/v1/.../arquivos/{sequencialDocumento}`.

## Observações

- A API de consulta não possui filtro semântico direto por tema. O filtro por limpeza urbana, resíduos e temas semelhantes é aplicado localmente sobre o objeto do contrato.
- O app inclui sugestões iniciais para limpeza, resíduos, obras e tecnologia.
- O preset de Belo Horizonte usa o CNPJ `18.715.383/0001-40`; validar conforme o órgão publicador específico quando a prefeitura publicar por secretarias/autarquias diferentes.
