# Smoke Inicial da API PNCP

## Objetivo

Registrar a primeira validação operacional da extração via API pública do PNCP usando a amostra manual derivada de `documentation/source/exemplo_1.xlsx`.

Plano relacionado:

- `documentation/plans/pncp-api-execution-plan.md`

Contexto relacionado:

- `documentation/context/pncp-api-consultas.md`

## Artefatos Criados

Scripts:

- `scripts/generate_pncp_manual_manifest.py`
- `scripts/run_pncp_api_smoke.py`

Amostra versionável:

- `documentation/plans/pncp-api-smoke-sample.csv`

Artefatos locais gerados:

- `data/interim/pncp/manual_manifest.csv`
- `data/raw/pncp/<run_id>/...`
- `data/processed/pncp/<run_id>/...`

## Manifesto Manual

Comando executado:

```bash
python scripts/generate_pncp_manual_manifest.py
```

Resultado:

- `345` linhas úteis no manifesto local
- `25` linhas identificadas com fonte PNCP
- `5` linhas selecionadas para a amostra inicial de smoke

Linhas da amostra:

- linha `67`: Belford Roxo/RJ, contrato `02/SEMSEP/2025/2025`
- linha `70`: Ananindeua/PA, contrato `082025/2025`
- linha `71`: Ananindeua/PA, contrato `052025/2025`
- linha `72`: Vila Velha/ES, contrato `299/2025`
- linha `83`: Montes Claros/MG, contrato `2762501/2025`

## Cliente da API

Endpoint testado:

```text
GET https://pncp.gov.br/api/consulta/v1/contratos
```

Estratégia inicial:

- usar a data de início da vigência como referência
- consultar janela em torno da vigência inicial
- começar pela primeira página
- salvar resposta bruta e candidatos

Parâmetros usados nos testes:

- `pagina=1`
- `tamanhoPagina=10` após ajuste conservador
- `date-window-days=45` e depois `date-window-days=1`

## Execuções

### Dry-run

Comando:

```bash
python scripts/run_pncp_api_smoke.py --dry-run --run-id pncp-api-smoke-dry-run
```

Resultado:

- leitura da amostra funcionou
- URLs foram montadas
- artefatos locais foram escritos

### Chamada real com 1 linha

Primeira tentativa:

```bash
python scripts/run_pncp_api_smoke.py --limit 1 --run-id pncp-api-smoke-live-limit1
```

Resultado:

- falhou no sandbox sem permissão de rede
- erro registrado: `WinError 10013`

Segunda tentativa com permissão de rede:

```bash
python scripts/run_pncp_api_smoke.py --limit 1 --run-id pncp-api-smoke-live-limit1
```

Resultado:

- a janela anual estourou timeout de `30s`
- a estratégia foi ajustada para janela menor e página menor

Terceira tentativa:

```bash
python scripts/run_pncp_api_smoke.py --limit 1 --run-id pncp-api-smoke-live-limit1-window
```

Resultado:

- status HTTP `200`
- resposta em aproximadamente `0.77s`
- `totalRegistros=590508`
- nenhum candidato forte após correção do scoring

### Chamada real com 5 linhas

Execução com janela de `45` dias:

```bash
python scripts/run_pncp_api_smoke.py --run-id pncp-api-smoke-live-sample5-v2
```

Resultado:

- linhas `67`, `70` e `83`: status `200`
- linhas `71` e `72`: timeout de `30s`
- nenhum candidato forte encontrado

Execução com janela de `1` dia:

```bash
python scripts/run_pncp_api_smoke.py --date-window-days 1 --run-id pncp-api-smoke-live-sample5-window1
```

Resultado:

- linhas `67`, `70` e `72`: status `200`
- linhas `71` e `83`: timeout de `30s`
- nenhum candidato forte encontrado

## Aprendizados

O cliente mínimo da API funciona e a API pública respondeu com status `200` em chamadas controladas.

A consulta direta em `/v1/contratos` sem filtro por CNPJ do órgão é ampla demais. Mesmo janelas de poucos dias podem retornar dezenas de milhares de registros.

O CNPJ disponível na planilha aparenta ser, na maior parte dos casos, CNPJ do fornecedor ou entidade contratada, enquanto o filtro `cnpjOrgao` do endpoint `/v1/contratos` espera o CNPJ do órgão contratante.

A estratégia inicial de localizar contratos apenas por janela de vigência, número do contrato e CNPJ da planilha não foi suficiente para encontrar candidatos fortes na primeira página.

Algumas janelas de data do endpoint `/v1/contratos` apresentaram timeout mesmo com `tamanhoPagina=10`.

## Ajustes Aplicados

- `scripts/run_pncp_api_smoke.py` passou a usar `tamanhoPagina=10` por padrão
- o runner passou a aceitar `--source-row`
- o runner passou a aceitar `--date-window-days`
- o scoring foi corrigido para não considerar anos soltos, como `2025`, como evidência de match

## Interpretação

O smoke técnico foi parcialmente aprovado:

- aprovado para leitura do manifesto
- aprovado para montagem de chamadas
- aprovado para persistência de respostas brutas
- aprovado para chamadas reais simples à API
- ainda não aprovado como estratégia de matching

O principal bloqueio não é acesso à API, mas sim a falta de um identificador mais restritivo para consultar contratos.

## Próximos Passos Recomendados

1. Extrair ou obter CNPJ do órgão contratante para cada município/contrato da amostra.
2. Testar `/v1/contratos` com `cnpjOrgao` quando o CNPJ do órgão estiver disponível.
3. Avaliar uso de endpoints detalhados do Manual de Integração quando houver `numeroControlePNCP` ou identificadores derivados.
4. Investigar se há URLs PNCP ou identificadores ocultos/hyperlinks na planilha original para as linhas marcadas como `PNCP`.
5. Só depois expandir paginação ou tentar matching em volume maior.

## Decisão Inicial

A próxima rodada deve priorizar enriquecimento do manifesto com identificadores do órgão contratante ou links PNCP, antes de tentar varrer grandes volumes de contratos por data.
