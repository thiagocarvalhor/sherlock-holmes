# Plano de Execucao: Streamlit Documento-Primeiro

## Objetivo

Reestruturar o app Streamlit para comecar pela busca de documentos oficiais no PNCP e deixar a comparacao manual como segunda etapa do fluxo.

## Motivacao

A versao anterior estava organizada em abas e exigia que o usuario entendesse a diferenca entre "Comparacao" e "Busca PNCP" antes de agir. A nova organizacao deve deixar a primeira acao mais clara:

```text
buscar documentos oficiais
selecionar contrato e arquivo
comparar com a fonte manual
```

## Escopo

### Inclui

- remover a experiencia principal baseada em abas;
- criar uma pagina unica com secao inicial de documentos PNCP;
- manter busca avulsa de contratos e arquivos oficiais;
- permitir comparar uma linha manual com o contrato selecionado na busca;
- manter investigacao automatica como opcao secundaria;
- limpar labels visuais e badges de status;
- atualizar testes de render do Streamlit.

### Nao Inclui

- alterar regras de scoring;
- alterar endpoints PNCP;
- baixar documentos automaticamente;
- integrar OCR;
- criar relatorio final exportavel.

## Arquivos Esperados

- `scripts/pncp_streamlit_app.py`
- `src/sherlock_holmes/webapp/views.py`
- `src/sherlock_holmes/webapp/ui.py`
- `src/sherlock_holmes/webapp/pncp.py`
- `tests/test_app_render.py`

## Criterio de Conclusao

O app deve abrir em uma pagina unica onde a primeira secao e `Documentos PNCP` e a segunda e `Comparacao manual`, sem quebrar testes existentes.
