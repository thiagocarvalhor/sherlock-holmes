# Plano de Execucao: Reestruturacao Inicial da Camada PNCP

## Objetivo

Reestruturar a camada PNCP do Sherlock Holmes de forma incremental, sem quebrar os scripts atuais, preparando o projeto para a proxima fase: comparacao auditavel entre fonte manual e dados oficiais.

Esta entrega deve transformar o cliente PNCP atual em uma base mais modular, com funcoes reutilizaveis para contratos, identificadores PNCP e datas.

## Contexto

O Sherlock Holmes foi reposicionado como um pipeline tecnico e auditavel para localizar, validar e comparar contratos publicos.

Diretriz atual:

```text
PNCP primeiro.
Documentos depois.
OCR apenas quando necessario.
Evidencia sempre.
```

A analise do Licinexus MCP indicou que a camada PNCP deve separar melhor:

- adaptador HTTP;
- utilitarios de identificacao;
- utilitarios de data;
- funcoes de dominio;
- scripts de execucao;
- relatorios e evidencias.

## Escopo da Primeira Entrega

Esta primeira entrega deve ser pequena e segura.

### Inclui

- criar utilitario para CNPJ e numero de controle PNCP;
- criar utilitario para datas PNCP;
- criar modulo de contratos;
- preservar compatibilidade com `scripts/run_pncp_api_smoke.py`;
- preservar compatibilidade com `scripts/pncp_streamlit_app.py`;
- manter o comportamento atual de busca de contratos;
- adicionar funcao para listar arquivos de contrato;
- registrar criterios de validacao.

### Nao inclui

- reestruturar toda a camada PNCP;
- implementar licitacoes/compras;
- implementar atas de registro de preco;
- implementar PCA;
- implementar BrasilAPI;
- implementar matching completo;
- alterar o app Streamlit de forma relevante;
- criar MCP proprio;
- alterar OCR.

## Arquivos a Criar

```text
src/sherlock_holmes/pncp/ids.py
src/sherlock_holmes/pncp/dates.py
src/sherlock_holmes/pncp/contratos.py
```

## Arquivos que Podem Ser Ajustados

```text
src/sherlock_holmes/pncp/client.py
src/sherlock_holmes/pncp/__init__.py
scripts/run_pncp_api_smoke.py
scripts/pncp_streamlit_app.py
```

Os ajustes em scripts devem ser conservadores. O objetivo e passar a usar as novas funcoes aos poucos, nao reescrever o fluxo inteiro.

## Funcoes Prioritarias

### `ids.py`

Funcoes:

```text
normalize_cnpj
parse_numero_controle_pncp
resolve_pncp_contract_id
```

Responsabilidades:

- aceitar CNPJ com ou sem pontuacao;
- validar CNPJ com 14 digitos;
- converter `numeroControlePNCP` em `cnpj`, `ano` e `sequencial`;
- permitir que funcoes de detalhe aceitem tanto `numeroControlePNCP` quanto o trio `cnpj/ano/sequencial`.

Formato esperado de `numeroControlePNCP`:

```text
NNNNNNNNNNNNNN-D-NNNNNN/YYYY
```

Exemplo:

```text
39485438000142-2-000018/2025
```

### `dates.py`

Funcoes:

```text
format_pncp_date
parse_pncp_date
validate_pncp_date_range
default_date_range
```

Responsabilidades:

- trabalhar com formato `YYYYMMDD`;
- validar se a data existe;
- validar se `dataInicial <= dataFinal`;
- evitar janelas excessivamente grandes;
- facilitar janelas padrao para smoke e exploracao.

Regra inicial:

```text
PNCP_MAX_DATE_RANGE_DAYS = 365
```

### `contratos.py`

Funcoes:

```text
search_contratos
get_contrato
list_contrato_arquivos
```

Responsabilidades:

- centralizar chamadas relacionadas a contratos;
- aceitar filtros por periodo, CNPJ do orgao e CNPJ do fornecedor;
- preservar URL e payload retornado;
- listar arquivos oficiais associados a um contrato;
- evitar duplicacao de montagem de URL.

## Compatibilidade Esperada

### `client.py`

O arquivo `client.py` ainda pode manter funcoes existentes usadas pelo Streamlit.

Durante esta entrega, nao e obrigatorio remover funcoes antigas.

Preferencia:

- criar funcoes novas;
- migrar usos aos poucos;
- manter aliases quando isso reduzir risco.

### `run_pncp_api_smoke.py`

O script deve continuar:

- lendo `documentation/plans/pncp-api-smoke-sample.csv`;
- gerando respostas brutas em `data/raw/pncp`;
- gerando candidatos e resumo em `data/processed/pncp`;
- aceitando os argumentos atuais.

### `pncp_streamlit_app.py`

O app deve continuar abrindo e buscando contratos.

Se houver ajuste, deve ser pequeno e sem alterar a experiencia principal.

## Criterios de Sucesso

A entrega sera considerada concluida quando:

- `ids.py`, `dates.py` e `contratos.py` existirem;
- as funcoes novas forem importaveis;
- `scripts/run_pncp_api_smoke.py --dry-run` continuar funcionando;
- uma chamada real pequena da API continuar funcionando quando houver rede disponivel;
- a busca da linha `67` continuar encontrando candidato forte quando executada com parametros ja conhecidos;
- o app Streamlit nao perder os imports atuais;
- os resultados continuarem salvando URL, parametros, payload e erro quando houver.

## Validacao Local

Comandos sugeridos:

```powershell
.venv\Scripts\python.exe scripts\run_pncp_api_smoke.py --dry-run --limit 1 --run-id pncp-refactor-dry-run
```

Quando rede estiver disponivel:

```powershell
.venv\Scripts\python.exe scripts\run_pncp_api_smoke.py --source-row 67 --run-id pncp-refactor-live-row67
```

Validacao opcional, se o ambiente estiver pronto:

```powershell
.venv\Scripts\python.exe -m pytest
```

## Riscos

### Quebrar Imports Existentes

Risco:

- scripts e Streamlit ainda importam funcoes diretamente de `client.py`.

Mitigacao:

- manter funcoes antigas durante a primeira entrega;
- migrar imports apenas quando necessario;
- evitar remocao de APIs internas nesta fase.

### Mudanca de Comportamento da API PNCP

Risco:

- endpoints podem responder com `204`, `404`, `422`, timeout ou formatos diferentes.

Mitigacao:

- preservar payload bruto;
- padronizar erro sem esconder resposta oficial;
- manter chamadas pequenas nos smokes.

### Rede Indisponivel

Risco:

- validacao real pode falhar por rede, DNS, timeout ou instabilidade do PNCP.

Mitigacao:

- sempre rodar dry-run;
- registrar se a validacao real nao foi executada;
- nao bloquear refatoracao estrutural apenas por falha externa temporaria.

## Sequencia de Implementacao

1. Criar `ids.py`.
2. Criar `dates.py`.
3. Criar `contratos.py` usando `client.py` como base.
4. Ajustar imports internos se necessario.
5. Rodar dry-run do smoke PNCP.
6. Rodar chamada real controlada, se rede estiver disponivel.
7. Registrar resultado em `documentation/reports`, se houver execucao real relevante.
8. Atualizar este plano com status final da entrega.

## Status

Concluida.

## Resultado da Entrega

Arquivos criados:

- `src/sherlock_holmes/pncp/ids.py`
- `src/sherlock_holmes/pncp/dates.py`
- `src/sherlock_holmes/pncp/contratos.py`

Arquivo atualizado:

- `src/sherlock_holmes/pncp/__init__.py`
- `scripts/run_pncp_api_smoke.py`

Validacoes executadas:

- compilacao da camada PNCP com `compileall`;
- smoke PNCP em modo `dry-run`;
- smoke PNCP real para `source_row=67`, com HTTP `200`;
- checagem direta de parsing de `numeroControlePNCP` e montagem de URLs.
- smoke PNCP paginado com `--max-pages 3`, retornando `39485438000142-2-000018/2025` como top candidate.

Relatorio:

- `documentation/reports/pncp-refactor-001.md`

## Proximo Passo

Iniciar a segunda entrega PNCP: licitacoes/compras e arquivos associados, mantendo o smoke de contratos como base de validacao.
