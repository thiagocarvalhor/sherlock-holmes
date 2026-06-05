# Relatorio: Reestruturacao Inicial da Camada PNCP

## Objetivo

Registrar a primeira entrega tecnica da reestruturacao PNCP, conforme o plano `documentation/plans/pncp-refactor-execution-plan.md`.

## Alteracoes Realizadas

Foram criados os seguintes modulos:

- `src/sherlock_holmes/pncp/ids.py`
- `src/sherlock_holmes/pncp/dates.py`
- `src/sherlock_holmes/pncp/contratos.py`

Tambem foi atualizado:

- `src/sherlock_holmes/pncp/__init__.py`
- `scripts/run_pncp_api_smoke.py`

## Funcoes Criadas

### Identificadores

- `compact_digits`
- `normalize_cnpj`
- `parse_numero_controle_pncp`
- `resolve_pncp_contract_id`

### Datas

- `format_pncp_date`
- `parse_pncp_date`
- `validate_pncp_date_range`
- `default_date_range`

### Contratos

- `search_contratos_url`
- `search_contratos`
- `get_contrato_url`
- `get_contrato`
- `list_contrato_arquivos_url`
- `list_contrato_arquivos`
- `contrato_arquivo_download_url`

Tambem foram mantidos wrappers de compatibilidade para:

- `contract_publication_url`
- `fetch_contracts_by_publication`

## Validacoes Executadas

### Compilacao

Comando:

```powershell
.venv\Scripts\python.exe -m compileall src\sherlock_holmes\pncp
```

Resultado:

- sucesso;
- `__init__.py`, `contratos.py`, `dates.py` e `ids.py` compilados.

### Smoke PNCP Dry-run

Comando:

```powershell
.venv\Scripts\python.exe scripts\run_pncp_api_smoke.py --dry-run --limit 1 --run-id pncp-refactor-dry-run
```

Resultado:

- `source_row=67`;
- `status=dry-run`;
- `candidates=0`;
- resumo gerado em `data/processed/pncp/pncp-refactor-dry-run/match_summary.csv`.

### Smoke PNCP Real

Primeira tentativa:

- falhou por bloqueio de rede do sandbox;
- erro registrado como `URLError: WinError 10013`.

Segunda tentativa:

```powershell
.venv\Scripts\python.exe scripts\run_pncp_api_smoke.py --source-row 67 --run-id pncp-refactor-live-row67
```

Resultado:

- `source_row=67`;
- HTTP `200`;
- `totalRegistros=22`;
- `totalPaginas=3`;
- `candidates_count=10`;
- `top_score=8`;
- `top_numero_controle_pncp=39485438000142-2-000003/2025`;
- resumo gerado em `data/processed/pncp/pncp-refactor-live-row67/match_summary.csv`.

Observacao:

- a chamada real confirmou que a API respondeu e que o script continua operacional;
- o smoke atual consulta apenas a primeira pagina retornada pelo endpoint;
- a validacao nao confirma ainda o contrato `39485438000142-2-000018/2025` como top candidate;
- a melhoria de paginacao/scoring deve entrar na proxima etapa de matching ou evolucao do smoke.

### Checagem Direta das Novas Funcoes

Comando:

```powershell
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -c "from sherlock_holmes.pncp import parse_numero_controle_pncp, get_contrato_url, list_contrato_arquivos_url; rid=parse_numero_controle_pncp('39485438000142-2-000018/2025'); print(rid); print(get_contrato_url(numero_controle_pncp='39485438000142-2-000018/2025')); print(list_contrato_arquivos_url(numero_controle_pncp='39485438000142-2-000018/2025'))"
```

Resultado:

```text
PncpResourceId(orgao_cnpj='39485438000142', ano=2025, sequencial=18)
https://pncp.gov.br/api/pncp/v1/orgaos/39485438000142/contratos/2025/18
https://pncp.gov.br/api/pncp/v1/orgaos/39485438000142/contratos/2025/18/arquivos
```

## Conclusao

A primeira entrega tecnica da reestruturacao PNCP foi concluida.

O projeto agora possui modulos especificos para:

- identificadores PNCP;
- datas PNCP;
- operacoes de contratos.

Os scripts existentes continuam funcionando, e a chamada real controlada ao PNCP retornou HTTP `200`.

## Atualizacao: Paginacao e Scoring do Smoke

Apos a criacao dos modulos iniciais, o script `scripts/run_pncp_api_smoke.py` foi ajustado para:

- aceitar `--max-pages`;
- buscar multiplas paginas de contratos;
- usar `search_contratos_url` da nova camada `pncp.contratos` quando a URL base padrao for usada;
- remover candidatos duplicados por `numeroControlePNCP`;
- pontuar melhor correspondencia de valor e vigencia.

Validacao:

```powershell
.venv\Scripts\python.exe scripts\run_pncp_api_smoke.py --source-row 67 --max-pages 3 --run-id pncp-refactor-scoring-live-row67
```

Resultado:

- HTTP `200`;
- `totalRegistros=22`;
- `totalPaginas=3`;
- `candidates_count=20`;
- `top_score=23`;
- `top_numero_controle_pncp=39485438000142-2-000018/2025`;
- `top_numero_contrato_empenho=02SEMSEP2025/790/791`.

Interpretacao:

- a paginacao permitiu recuperar todos os registros da janela testada;
- a deduplicacao reduziu candidatos repetidos;
- o scoring passou a ranquear como top candidate o contrato esperado para a linha `67`.

## Proximos Passos

1. Iniciar a segunda entrega PNCP: licitacoes/compras e arquivos associados.
2. Avaliar extracao de detalhes e arquivos do contrato top candidate.
3. Preparar a futura camada de matching/comparacao usando o resultado do smoke.
