# Plano de Execução: Validação Inicial da API PNCP

## Objetivo

Validar, de forma controlada e reproduzível, se o projeto Sherlock Holmes consegue reencontrar via API pública do PNCP os contratos previamente coletados de forma manual, baixar ou referenciar seus dados oficiais e preparar a base para extração de informações contratuais por texto direto, OCR ou outro mecanismo adequado ao tipo de documento.

Esta fase deve transformar a planilha manual inicial em um fluxo técnico verificável:

- ler registros de referência
- consultar a API pública
- localizar registros oficiais correspondentes
- comparar dados manuais e dados oficiais
- identificar quais informações já vêm estruturadas na API
- identificar quais informações exigem análise de documentos anexos

## Referência de Contexto

O contexto técnico da API de Consultas PNCP está documentado em:

- `documentation/context/pncp-api-consultas.md`

As fontes locais relacionadas estão em:

- `documentation/source/api_de_consultas.pdf`
- `documentation/source/manual_de_integracao_pncp.pdf`
- `documentation/source/exemplo_1.xlsx`

## Escopo da Fase Inicial

Esta fase terá foco exclusivo em validar a extração e conciliação de dados a partir de uma amostra manual já conhecida.

### Inclui

- leitura da aba `CONSOLIDADO` do arquivo `exemplo_1.xlsx`
- criação de manifesto intermediário para orientar as consultas
- foco inicial em linhas cuja fonte esteja marcada como `PNCP`
- consulta à API pública de consultas do PNCP
- persistência de respostas brutas da API
- comparação entre dados manuais e dados retornados pela API
- identificação de contratos que precisam de análise de documento anexo
- definição inicial de estratégia para texto direto versus OCR

### Não inclui

- coleta ampla de todo o PNCP
- integração autenticada para envio ou alteração de dados no PNCP
- credenciamento de sistema junto ao PNCP
- extração semântica final de todos os campos contratuais
- OCR em lote de todos os documentos
- banco de dados final de produção
- interface de usuário

## Critérios de Sucesso

Ao final desta fase, o projeto deve ter evidências suficientes para decidir como seguir com a extração via API e documentos do PNCP.

Critérios mínimos:

- manifesto intermediário gerado a partir de `exemplo_1.xlsx`
- linhas com `FONTE = PNCP` identificadas e normalizadas
- cliente mínimo da API funcionando
- pelo menos uma pequena amostra de contratos consultada via API
- respostas brutas salvas localmente em formato auditável
- resumo comparativo entre planilha manual e API
- lista de campos encontrados diretamente na API
- lista de campos que exigem documento/anexo
- recomendação clara para a próxima rodada

## Etapas de Execução

### 1. Preparar o manifesto manual

Objetivo:

- transformar a aba `CONSOLIDADO` em uma estrutura legível por máquina
- preservar os dados necessários para busca e comparação

Entradas:

- `documentation/source/exemplo_1.xlsx`
- aba `CONSOLIDADO`

Campos esperados:

- `source_row`
- `municipio`
- `uf`
- `regiao`
- `populacao`
- `faixa_populacional`
- `objeto_contrato`
- `nome_empresa`
- `revisao_empresas`
- `cnpj`
- `vigencia_inicio`
- `vigencia_fim`
- `valor_contrato`
- `numero_contrato`
- `fonte_texto`
- `fonte_url`

Regras:

- preservar o número da linha original da planilha
- normalizar cabeçalhos das linhas 4 e 5
- converter datas seriais do Excel para data ISO quando possível
- preservar valores originais além dos valores normalizados
- preservar hyperlinks da coluna `FONTE` quando existirem
- não editar a planilha original

Artefato sugerido:

- `data/interim/pncp/manual_manifest.csv`

Observação:

- `data/interim` está ignorado pelo Git
- se for necessário versionar uma amostra pequena, criar artefato separado em `documentation/plans`

Status atual:

- `exemplo_1.xlsx` identificado em `documentation/source`
- aba `CONSOLIDADO` localizada
- dados começam na linha `6`
- leitura inicial indicou `347` linhas de dados
- leitura inicial indicou `25` linhas com menção a `PNCP`
- script gerador criado em `scripts/generate_pncp_manual_manifest.py`
- manifesto intermediário gerado localmente em `data/interim/pncp/manual_manifest.csv`, com `345` linhas úteis
- amostra inicial de smoke gerada em `documentation/plans/pncp-api-smoke-sample.csv`, com `5` linhas marcadas como `PNCP`

### 2. Definir a amostra de smoke da API

Objetivo:

- escolher um subconjunto pequeno para validar o fluxo antes de ampliar

Estratégia:

- começar pelas linhas com `FONTE = PNCP`
- selecionar inicialmente cerca de `5` contratos
- priorizar registros com:
  - município e UF preenchidos
  - CNPJ preenchido
  - número de contrato preenchido
  - vigência ou ano inferível
  - valor preenchido, quando disponível

Campos úteis para matching:

- `municipio`
- `uf`
- `cnpj`
- `nome_empresa`
- `numero_contrato`
- `vigencia_inicio`
- `vigencia_fim`
- `valor_contrato`
- `objeto_contrato`

Artefato sugerido:

- `documentation/plans/pncp-api-smoke-sample.csv`

Status atual:

- amostra inicial selecionada em `documentation/plans/pncp-api-smoke-sample.csv`
- amostra contém `5` registros originados de linhas com `FONTE = PNCP`

### 3. Implementar cliente mínimo da API

Objetivo:

- criar um cliente simples e auditável para chamadas GET à API de Consultas PNCP

URL base:

```text
https://pncp.gov.br/api/consulta
```

Requisitos mínimos:

- montar URLs com parâmetros de query
- enviar requisições GET
- definir timeout
- registrar status HTTP
- tratar `200`, `204`, `400`, `422` e `500`
- retornar JSON quando houver corpo
- salvar resposta bruta
- registrar parâmetros usados

Endpoint prioritário:

```text
GET /v1/contratos
```

Endpoint complementar:

```text
GET /v1/contratacoes/publicacao
```

Status atual:

- cliente mínimo implementado em `scripts/run_pncp_api_smoke.py`
- runner usa `GET /v1/contratos`
- runner salva resposta bruta em `data/raw/pncp/<run_id>/...`
- runner salva resumo e candidatos em `data/processed/pncp/<run_id>/...`
- runner aceita `--source-row`, `--date-window-days`, `--tamanho-pagina`, `--limit` e `--dry-run`
- dry-run validado
- chamada real à API validada com status `200` em amostra controlada

#### Registro inicial de execução

Comandos validados:

```bash
python scripts/generate_pncp_manual_manifest.py
python scripts/run_pncp_api_smoke.py --dry-run --run-id pncp-api-smoke-dry-run
python scripts/run_pncp_api_smoke.py --limit 1 --run-id pncp-api-smoke-live-limit1-window
python scripts/run_pncp_api_smoke.py --run-id pncp-api-smoke-live-sample5-v2
python scripts/run_pncp_api_smoke.py --date-window-days 1 --run-id pncp-api-smoke-live-sample5-window1
```

Primeira tentativa real:

- `--limit 1` com janela anual estourou timeout de `30s`
- após reduzir a janela e o tamanho da página, a API retornou status `200`

Execução com `5` linhas e janela de `45` dias:

- linhas `67`, `70` e `83`: status `200`
- linhas `71` e `72`: timeout de `30s`
- nenhum candidato forte encontrado

Execução com `5` linhas e janela de `1` dia:

- linhas `67`, `70` e `72`: status `200`
- linhas `71` e `83`: timeout de `30s`
- nenhum candidato forte encontrado

Aprendizados:

- o cliente mínimo consegue chamar a API pública e salvar respostas brutas
- `/v1/contratos` sem filtro por `cnpjOrgao` retorna volumes muito altos
- janelas curtas ainda podem retornar dezenas de milhares de registros
- o filtro `cnpjOrgao` do endpoint exige CNPJ do órgão
- usar o CNPJ da planilha como `cnpjOrgao` tornou a busca muito mais precisa na linha `67`
- localizar contratos só por data de vigência e número de contrato não é suficiente
- o scoring foi ajustado para não considerar anos soltos, como `2025`, como evidência de match

Decisão técnica inicial:

- usar o campo `cnpj` do manifesto como `cnpjOrgao` quando ele representar o órgão contratante
- validar caso a caso se o CNPJ do manifesto é do órgão ou do fornecedor
- antes de expandir paginação ou volume, enriquecer o manifesto com URL PNCP, identificador PNCP ou confirmação do CNPJ do órgão

Validação posterior com `cnpjOrgao`:

- linha `67`: status `200`, `totalRegistros=22`, `totalPaginas=3`, `candidates_count=10`
- melhor candidato da linha `67`: `numeroControlePNCP=39485438000142-2-000018/2025`
- o candidato encontrado bate com Belford Roxo/RJ, vigência `2025-11-04` a `2026-11-03`, valor global `52801942.27` e objeto de limpeza urbana/manejo de resíduos
- linhas `70`, `71`, `72` e `83`: status `204` na janela testada
- interpretação: para a linha `67`, o campo `cnpj` do manifesto funcionou como `cnpjOrgao`; para as demais, o contrato pode estar fora da janela de publicação testada ou o CNPJ pode não ser o órgão contratante

#### Validação manual no Postman

A chamada da linha `67` também foi reproduzida manualmente no Postman:

```text
GET https://pncp.gov.br/api/consulta/v1/contratos?dataInicial=20250920&dataFinal=20251219&pagina=1&tamanhoPagina=10&cnpjOrgao=39485438000142
```

Parâmetros:

- `dataInicial=20250920`
- `dataFinal=20251219`
- `pagina=1`
- `tamanhoPagina=10`
- `cnpjOrgao=39485438000142`

Resultado esperado:

- status HTTP `200`
- `totalRegistros=22`
- `totalPaginas=3`
- registros retornados com `orgaoEntidade.cnpj=39485438000142`

Problema observado no Postman:

- se o valor de `cnpjOrgao` contiver quebra de linha ou espaço final, a API retorna `422`
- o erro aparece como `CNPJ do Órgão/Entidade inválido`
- no Postman, o símbolo `↵` no fim do valor indica quebra de linha

Regra prática:

- digitar `cnpjOrgao` manualmente ou garantir que o valor esteja sem máscara, espaço ou quebra de linha
- usar apenas números, por exemplo `39485438000142`
- ao usar a tabela `Params`, deixar a URL base sem query string manual

### 4. Localizar contratos da planilha via API

Objetivo:

- verificar se os contratos marcados como `PNCP` na planilha podem ser reencontrados via API pública

Estratégia inicial:

- para cada registro da amostra, consultar `/v1/contratos`
- usar janelas de data derivadas da vigência, do número do contrato ou de hipóteses de publicação
- filtrar candidatos retornados por:
  - número do contrato
  - CNPJ do fornecedor, quando aparecer na resposta ou no documento associado
  - órgão/município/UF
  - objeto
  - valor

Possíveis dificuldades:

- a data de publicação do contrato pode ser diferente da vigência
- o número do contrato pode ter variações de formatação
- CNPJ da planilha pode ser do fornecedor, enquanto alguns filtros da API usam CNPJ do órgão
- o município da planilha pode não mapear diretamente para o órgão contratante retornado

Regras:

- salvar todas as respostas candidatas antes de escolher um match
- registrar quando não houver candidato
- registrar quando houver múltiplos candidatos
- não descartar variações de formatação sem análise

Artefatos locais sugeridos:

- `data/raw/pncp/<run_id>/contracts/*.json`
- `data/processed/pncp/<run_id>/match_candidates.csv`
- `data/processed/pncp/<run_id>/match_summary.csv`

Status atual:

- etapa parcialmente executada
- primeira amostra de `5` linhas foi testada
- algumas chamadas a `/v1/contratos` responderam com status `200`
- algumas janelas apresentaram timeout mesmo com `tamanhoPagina=10`
- interpretação inicial: a busca por `/v1/contratos` sem `cnpjOrgao` ou identificador PNCP é ampla demais para matching confiável
- interpretação atualizada: quando o CNPJ do manifesto corresponde ao `cnpjOrgao`, a busca fica precisa e já encontrou um match forte na linha `67`

### 5. Comparar planilha manual e API

Objetivo:

- medir quais campos podem ser obtidos diretamente da API e quais exigem documentos

Campos a comparar:

- município/UF
- órgão contratante
- número do contrato
- fornecedor
- CNPJ do fornecedor
- objeto
- vigência inicial
- vigência final
- valor
- processo
- número de controle PNCP

Classificação sugerida por campo:

- `match`: valor encontrado e compatível
- `partial`: valor parecido, mas exige normalização ou revisão
- `missing_api`: valor está na planilha, mas não apareceu na API
- `missing_manual`: valor está na API, mas não estava na planilha
- `conflict`: valores parecem incompatíveis
- `needs_document`: campo provavelmente exige leitura de documento

Artefato sugerido:

- `documentation/reports/pncp-api-smoke-comparison.md`

Status atual:

- etapa parcialmente executada para a linha `67`
- a linha `67` encontrou candidato forte com `numeroControlePNCP=39485438000142-2-000018/2025`
- campos compatíveis na linha `67`: município/UF, número aproximado do contrato, vigência, valor global e objeto
- para as demais linhas da amostra, ainda falta ajustar janela de publicação ou confirmar se o CNPJ do manifesto é o CNPJ do órgão

### 6. Buscar documentos e anexos relacionados

Objetivo:

- identificar quais documentos oficiais estão disponíveis para os contratos ou contratações encontrados

Fontes possíveis:

- endpoints detalhados descritos no Manual de Integração
- URLs retornadas pela API
- links do sistema de origem
- hyperlinks existentes na planilha manual

Documentos prioritários:

- contrato
- termo aditivo
- edital
- termo de referência
- ata
- outros anexos com dados contratuais

Regras:

- salvar metadados antes de baixar arquivos
- registrar URL de origem
- registrar tipo de documento
- registrar extensão e content type
- evitar sobrescrever arquivos com o mesmo nome

Artefatos locais sugeridos:

- `data/raw/pncp/<run_id>/documents/metadata.csv`
- `data/raw/pncp/<run_id>/documents/files/...`

Status atual:

- etapa ainda não executada

### 7. Definir estratégia de extração textual

Objetivo:

- decidir quando usar extração textual direta e quando acionar OCR

Fluxo sugerido:

1. identificar tipo do arquivo
2. se for PDF com camada textual, tentar extração direta
3. se for PDF escaneado ou imagem, acionar OCR
4. se for página HTML, tentar extração do conteúdo da página
5. se for documento Office, avaliar conversão ou parser específico

Relação com OCR:

- o trabalho anterior de OCR deve ser reaproveitado para documentos escaneados
- o OCR não deve ser aplicado automaticamente quando houver texto extraível diretamente

Campos-alvo da extração:

- fornecedor
- CNPJ do fornecedor
- número do contrato
- objeto
- valor
- vigência
- órgão contratante
- data de assinatura
- processo administrativo

Status atual:

- etapa ainda não executada

### 8. Consolidar decisão da rodada

Objetivo:

- transformar os resultados do smoke em uma decisão prática para a próxima etapa

Perguntas a responder:

- a API pública permite reencontrar os contratos da planilha manual?
- quais campos já vêm estruturados?
- quais campos exigem documento?
- os documentos estão acessíveis por API, URL ou sistema de origem?
- o matching por número de contrato, CNPJ, município e objeto é suficiente?
- precisamos de uma etapa de busca mais flexível?
- qual será a próxima amostra?

Artefato esperado:

- `documentation/reports/pncp-api-smoke-decision.md`

Status atual:

- etapa ainda não executada

## Organização de Artefatos

### Arquivos versionáveis

Contexto e plano:

- `documentation/context/pncp-api-consultas.md`
- `documentation/plans/pncp-api-execution-plan.md`

Relatórios pequenos:

- `documentation/reports/pncp-api-*.md`

Amostras pequenas, se necessário:

- `documentation/plans/pncp-api-smoke-sample.csv`

### Arquivos locais não versionados

Dados brutos:

```text
data/raw/pncp/<run_id>/...
```

Dados intermediários:

```text
data/interim/pncp/<run_id>/...
```

Dados processados:

```text
data/processed/pncp/<run_id>/...
```

## Entregáveis da Fase Inicial

Ao final desta fase, os seguintes artefatos devem estar disponíveis:

- manifesto intermediário da planilha manual
- amostra inicial de smoke da API
- cliente mínimo da API PNCP
- respostas brutas de uma rodada pequena
- resumo de candidatos encontrados
- comparação entre planilha e API
- decisão sobre estratégia de matching
- decisão sobre estratégia de documentos e extração textual
- lista clara de próximos passos

## Próximo Passo Operacional

Investigar as demais linhas da amostra inicial (`70`, `71`, `72` e `83`) usando a estratégia com `cnpjOrgao`.

Para cada linha:

- confirmar se o CNPJ do manifesto é o CNPJ do órgão contratante
- testar janelas alternativas de `dataPublicacaoPncp`
- verificar se há link PNCP, número de controle ou outro identificador disponível na fonte manual
- registrar se o endpoint retorna `200`, `204`, `422` ou timeout
- quando houver match, registrar `numeroControlePNCP`, `numeroControlePncpCompra`, valor, vigência e documento associado
