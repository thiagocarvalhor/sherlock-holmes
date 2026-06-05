# Plano de Execucao: Camada PNCP de Licitacoes e Compras

## Objetivo

Adicionar uma camada inicial para consultar licitacoes/compras no PNCP, listar seus detalhes, itens e arquivos associados.

Esta entrega complementa a reestruturacao inicial de contratos e prepara o projeto para localizar documentos oficiais antes de acionar extracao textual ou OCR.

## Contexto

A primeira entrega PNCP criou:

- `src/sherlock_holmes/pncp/ids.py`;
- `src/sherlock_holmes/pncp/dates.py`;
- `src/sherlock_holmes/pncp/contratos.py`;
- melhoria de paginacao e scoring em `scripts/run_pncp_api_smoke.py`.

Agora o foco e cobrir a parte de compras/licitacoes, que no PNCP aparece em endpoints como:

```text
/api/consulta/v1/contratacoes/publicacao
/api/consulta/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}
/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens
/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/arquivos
```

## Escopo

### Inclui

- criar modulo `licitacoes.py`;
- criar helpers de URL para compras/licitacoes;
- buscar contratacoes por data de publicacao;
- obter detalhe de uma compra/licitacao;
- listar itens;
- listar arquivos/anexos;
- aceitar `numeroControlePNCP` ou `cnpj/ano/sequencial` quando aplicavel;
- preservar payload e URL chamada.

### Nao inclui

- baixar arquivos;
- extrair texto de PDFs;
- OCR;
- resultados por item;
- atas de registro de preco;
- PCA;
- matching completo entre contrato e compra;
- mudancas relevantes no Streamlit.

## Arquivos a Criar ou Ajustar

```text
src/sherlock_holmes/pncp/licitacoes.py
src/sherlock_holmes/pncp/__init__.py
```

## Funcoes Prioritarias

```text
search_licitacoes_url
search_licitacoes
get_licitacao_url
get_licitacao
list_licitacao_itens_url
list_licitacao_itens
list_licitacao_arquivos_url
list_licitacao_arquivos
```

## Criterios de Sucesso

- modulo `licitacoes.py` criado;
- funcoes importaveis via `sherlock_holmes.pncp`;
- URLs geradas corretamente para busca, detalhe, itens e arquivos;
- validacao local sem rede passa;
- chamada real pequena pode buscar contratacoes por publicacao;
- detalhe/arquivos podem ser montados a partir de um `numeroControlePNCP` retornado pela busca.

## Validacao Local

Checagem sem rede:

```powershell
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -c "from sherlock_holmes.pncp import search_licitacoes_url; print(search_licitacoes_url(data_inicial='20250101', data_final='20250107', codigo_modalidade_contratacao=6, pagina=1, tamanho_pagina=10))"
```

Chamada real controlada, se rede estiver disponivel:

```powershell
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -c "from sherlock_holmes.pncp import search_licitacoes; r=search_licitacoes(data_inicial='20250101', data_final='20250107', codigo_modalidade_contratacao=6, uf='RJ', tamanho_pagina=10, max_pages=1); print(r.url); print(len(r.payload.get('data', [])) if isinstance(r.payload, dict) else type(r.payload))"
```

## Status

Concluida.

## Resultado da Entrega

Arquivo criado:

- `src/sherlock_holmes/pncp/licitacoes.py`

Arquivo atualizado:

- `src/sherlock_holmes/pncp/__init__.py`

Validacoes executadas:

- compilacao com `compileall`;
- checagem local de URLs;
- chamada real de busca de contratacoes por publicacao;
- chamada real de detalhe, itens e arquivos para `23274194000119-1-000191/2024`.

Relatorio:

- `documentation/reports/pncp-licitacoes-001.md`

## Proximo Passo

Criar camada inicial de arquivos/documentos para download ou referencia controlada, conectando contratos/compras aos anexos oficiais.
