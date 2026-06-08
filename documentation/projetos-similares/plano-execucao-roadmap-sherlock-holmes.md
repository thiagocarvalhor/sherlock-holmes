# Plano de Execucao do Roadmap Sherlock Holmes

## 1. Objetivo

Transformar o roadmap estrategico do Sherlock Holmes em um plano de execucao pratico, incremental e auditavel.

Este plano parte da seguinte direcao:

```text
PNCP primeiro.
Documentos depois.
OCR apenas quando necessario.
Evidencia sempre.
```

O objetivo nao e abandonar o trabalho de OCR ja feito, mas reposiciona-lo como uma camada de fallback documental dentro de um pipeline maior de busca, validacao, comparacao e evidencia.

## Status Atual do Plano

Este documento deve ser atualizado a cada mudanca relevante no roadmap.

Legenda:

```text
[x] concluido
[~] em andamento
[ ] pendente
```

### Acompanhamento Geral

- [x] Fase 1: atualizar narrativa e documentacao estrategica.
- [x] Fase 2: estudar melhor o Licinexus MCP.
- [x] Fase 3: reestruturar a camada PNCP em Python, primeira versao.
- [x] Fase 4: adicionar enriquecimento de CNPJ via BrasilAPI, primeira versao.
  - [x] Client BrasilAPI CNPJ.
  - [x] Normalizacao de CNPJ, campos padronizados, payload bruto e evidencia.
  - [x] Integrar enriquecimento inicial na UI Streamlit.
  - [ ] Integrar enriquecimento em relatorios auditaveis.
- [x] Fase 5: criar camada de matching e comparacao, primeira versao.
  - [x] Comparacao campo a campo com evidencias dos dois lados.
  - [x] Comparacao de registros completos.
  - [x] Scoring/ranking de candidatos aplicado sobre a linha `67`.
  - [ ] Refinar matching textual, status documental e confirmacao humana.
- [x] Fase 6: criar modelo de evidencia e confianca.
- [x] Fase 7: reposicionar OCR como fallback documental, primeira versao.
- [~] Fase 8: evoluir Streamlit para investigacao.
  - [x] Tela de comparacao manual vs PNCP (visualizador de resultado).
  - [x] Refatoracao do app em modulos reutilizaveis (app/pncp.py, app/comparison.py, app/ui.py).
  - [x] Link entre paginas e botao "Abrir no PNCP" por candidato.
  - [x] Redesign: fluxo de investigacao ao vivo (escolher linha -> busca PNCP -> comparacao na hora), abas no topo, cards e badges. Logica em `investigation.py`.
  - [x] Redesign documento-primeiro: busca PNCP de contratos/arquivos no topo, comparacao manual como segunda etapa.
  - [x] Selecao explicavel de contrato: escolha manual clara ou ranking por score contra linha manual.
  - [x] Enriquecimento cadastral BrasilAPI sob demanda para orgao/fornecedor do contrato escolhido.
- [~] Fase 9: criar relatorios auditaveis.
  - [x] Primeira versao de relatorio auditavel a partir de `record_comparison.json`.
  - [x] Saida JSON e Markdown para a linha `67`.
  - [x] Relatorio multi-linha, primeira versao.
  - [x] Incluir documentos oficiais vinculados no relatorio unitario e consolidado.
  - [ ] Incluir enriquecimento CNPJ quando disponivel.
  - [ ] Incluir documentos que exigem revisao/OCR.
- [ ] Fase 10: avaliar MCP, LLM e automacao.

### Atualizacoes Recentes

- [x] `documentation/overview-sherlock-holmes.md` atualizado com PNCP como nucleo, OCR como fallback, evidencia por origem e diferenciacao frente a projetos similares.
- [x] Criar relatorio curto em `documentation/reports` registrando a decisao de reposicionamento.
- [x] Clonar Licinexus MCP em `C:\Users\thiag\Documents\projetos\licinexus-mcp`.
- [x] Criar analise inicial em `documentation/projetos-similares/analise-licinexus-para-sherlock.md`.
- [x] Definir escopo fechado da primeira entrega tecnica PNCP em `documentation/plans/pncp-refactor-execution-plan.md`.
- [x] Implementar primeira entrega tecnica PNCP.
- [x] Registrar resultado em `documentation/reports/pncp-refactor-001.md`.
- [x] Melhorar smoke PNCP com paginacao, deduplicacao e scoring.
- [x] Validar linha `67` retornando `39485438000142-2-000018/2025` como top candidate.
- [x] Criar plano da segunda entrega PNCP em `documentation/plans/pncp-licitacoes-execution-plan.md`.
- [x] Implementar camada inicial de licitacoes/compras.
- [x] Validar busca, detalhe, itens e arquivos com chamada real ao PNCP.
- [x] Criar plano da camada de arquivos/documentos em `documentation/plans/pncp-documents-execution-plan.md`.
- [x] Implementar referencias auditaveis de arquivos/documentos PNCP.
- [x] Validar referencia real de edital via PNCP.
- [x] Criar plano de download controlado em `documentation/plans/pncp-document-download-execution-plan.md`.
- [x] Implementar download controlado por referencia PNCP.
- [x] Validar download real em `data/raw/pncp/documents`.
- [x] Criar plano de identificacao de tipo e extracao textual direta em `documentation/plans/document-text-extraction-execution-plan.md`.
- [x] Implementar camada `sherlock_holmes.documents`.
- [x] Validar inventario de ZIP e extracao textual direta de PDF com `pypdfium2`.
- [x] Criar plano de processamento controlado de ZIP em `documentation/plans/document-archive-processing-execution-plan.md`.
- [x] Implementar listagem/extracao controlada de membros ZIP.
- [x] Salvar resultado de extracao textual direta em JSON.
- [x] Criar plano do script operacional em `documentation/plans/document-processing-script-execution-plan.md`.
- [x] Implementar `scripts/process_document_text.py`.
- [x] Validar processamento local de ZIP com PDF interno e saida em `data/processed`.
- [x] Criar plano de normalizacao/qualidade em `documentation/plans/document-text-quality-execution-plan.md`.
- [x] Implementar normalizacao inicial e metricas de qualidade.
- [x] Validar texto extraido como `good` e `should_consider_ocr=false`.
- [x] Criar plano de criterios de fallback OCR em `documentation/plans/ocr-fallback-criteria-execution-plan.md`.
- [x] Implementar decisao operacional `decide_ocr_fallback`.
- [x] Validar `direct_text_ok` para documento real e `consider_ocr` para caso sem texto.
- [x] Criar plano do modelo de evidencia em `documentation/plans/evidence-model-execution-plan.md`.
- [x] Implementar `EvidenceRecord` e helpers iniciais.
- [x] Validar escrita de evidencias em JSON.
- [x] Criar evidencia de planilha manual.
- [x] Criar comparacao campo a campo inicial.
- [x] Validar comparacao de valor e CNPJ.
- [x] Criar comparacao de registros completos e aplicar sobre a linha `67`.
- [x] Paginar busca PNCP (paginas 2 e 3) e identificar contrato de limpeza urbana da linha `67`.
- [x] Endurecimento de base: pacote instalavel (`pyproject.toml`), remocao de hacks de `sys.path`, testes pytest (33 verdes), ruff e CI no GitHub Actions.
- [x] Consolidar Fase 5 como primeira versao funcional: comparacao campo a campo, comparacao de registros completos, score/ranking, JSON/CSV e testes.
- [x] Refatorar Streamlit para fluxo documento-primeiro em `documentation/reports/streamlit-document-first-redesign-001.md`.
- [x] Melhorar selecao de contrato no Streamlit com ranking explicavel em `documentation/reports/streamlit-contract-selection-001.md`.
- [x] Implementar enriquecimento inicial de CNPJ via BrasilAPI em `documentation/reports/cnpj-enrichment-brasilapi-001.md`.
- [x] Integrar enriquecimento CNPJ no Streamlit em `documentation/reports/streamlit-cnpj-enrichment-001.md`.
- [x] Criar primeira versao de relatorio auditavel em `documentation/reports/audit-report-001.md`.
- [x] Criar relatorio auditavel multi-linha em `documentation/reports/audit-batch-report-001.md`.
- [x] Incluir documentos oficiais vinculados nos relatorios auditaveis em `documentation/reports/audit-report-documents-001.md`.

## 2. Pergunta Inicial: Precisamos Conhecer Melhor os Projetos Similares?

Sim, mas em niveis diferentes.

Para atualizar a documentacao estrategica do Sherlock Holmes, a documentacao local ja e suficiente.

Para implementar a nova camada PNCP em Python com mais seguranca, vale estudar melhor a estrutura tecnica do Licinexus MCP, porque ele ja organizou o dominio em ferramentas como:

- busca de licitacoes;
- detalhes de licitacoes;
- itens;
- arquivos;
- contratos;
- termos aditivos;
- atas de registro de preco;
- orgaos;
- fornecedores;
- PCA;
- enriquecimento de CNPJ.

Para Streamlit, automacao e dashboards, nao e necessario clonar tudo agora. A documentacao dos projetos similares ja traz inspiracao suficiente para planejar.

## 3. Decisao Sobre Clonar o Licinexus

### Recomendacao

Clonar o repositorio do Licinexus MCP dentro do VS Code faz sentido antes da fase de reestruturacao PNCP.

### Quando clonar

Clonar depois de concluir a primeira fase documental do Sherlock Holmes.

### Por que clonar

Para estudar:

- nomes e responsabilidades das ferramentas;
- organizacao de endpoints PNCP;
- parametros aceitos;
- tratamento de erro;
- padronizacao de respostas;
- separacao entre PNCP, BrasilAPI e camada MCP;
- quais endpoints ja foram priorizados por outro projeto real.

### O que nao fazer

- Nao copiar codigo diretamente sem avaliar licenca, contexto e diferencas de stack.
- Nao transformar o Sherlock Holmes em um clone do Licinexus.
- Nao trazer MCP como prioridade imediata.

### Uso esperado do clone

O clone deve servir como referencia tecnica e mapa de dominio, nao como dependencia do Sherlock Holmes.

## 4. Principios de Execucao

- Toda tarefa deve gerar um artefato claro: codigo, documento, relatorio, CSV ou JSON.
- Toda decisao relevante deve ser registrada em `documentation/reports` ou em plano versionavel.
- O PNCP deve ser tratado como fonte primaria sempre que trouxer dado estruturado suficiente.
- Documentos oficiais devem ser consultados quando o dado estruturado nao bastar.
- OCR deve ser acionado somente quando houver documento escaneado ou imagem sem texto extraivel.
- Dados oficiais, dados manuais, OCR, LLM e revisao humana devem ser claramente separados.
- Nenhum alerta ou divergencia deve ser apresentado como acusacao automatica.

## 5. Ordem Recomendada de Execucao

```text
1. Atualizar narrativa e documentacao estrategica.
2. Estudar melhor o Licinexus MCP.
3. Reestruturar a camada PNCP em Python.
4. Adicionar enriquecimento de CNPJ via BrasilAPI.
5. Criar camada de matching e comparacao.
6. Criar modelo de evidencia e confianca.
7. Reposicionar OCR como fallback documental.
8. Evoluir Streamlit para investigacao e revisao.
9. Criar relatorios auditaveis.
10. Avaliar MCP/LLM e automacoes futuras.
```

## 6. Fase 1: Atualizar Narrativa e Documentacao Estrategica

### Objetivo

Deixar claro no proprio repositorio que o Sherlock Holmes e um pipeline investigativo e auditavel, nao apenas um experimento de OCR.

### Tarefas

- [x] Atualizar o overview do repositorio.
- [x] Explicar PNCP como fonte primaria.
- [x] Explicar OCR como fallback.
- [x] Explicar a diferenca entre dado oficial, dado manual, dado extraido e dado revisado.
- [x] Criar uma secao de diferenciacao frente a conectores PNCP existentes.
- [x] Registrar a frase guia:

```text
PNCP primeiro.
Documentos depois.
OCR apenas quando necessario.
Evidencia sempre.
```

### Arquivos esperados

- [x] `documentation/overview-sherlock-holmes.md`
- [x] `documentation/reports/sherlock-holmes-repositioning-decision.md`

### Criterio de conclusao

A documentacao deve permitir que uma pessoa nova entenda:

- qual problema o Sherlock Holmes resolve;
- por que PNCP e o nucleo;
- quando OCR entra;
- por que evidencia e confianca sao centrais.

### Status

Concluida.

O overview foi atualizado e a decisao foi registrada em `documentation/reports/sherlock-holmes-repositioning-decision.md`.

## 7. Fase 2: Estudar Melhor o Licinexus MCP

### Objetivo

Entender a organizacao tecnica do Licinexus MCP para inspirar a reestruturacao da camada PNCP do Sherlock Holmes.

### Tarefas

- [x] Clonar o repositorio em uma pasta local de referencia.
- [x] Ler a estrutura de diretorios.
- [x] Identificar onde ficam tools, schemas, clients e adaptadores.
- [x] Mapear quais endpoints PNCP sao usados.
- [x] Comparar as tools do Licinexus com as funcoes atuais em `src/sherlock_holmes/pncp/client.py`.
- [x] Criar uma matriz simples: `tool Licinexus` versus `funcao desejada no Sherlock`.

### Perguntas a responder

- Quais ferramentas do Licinexus sao essenciais para o Sherlock agora?
- Quais ferramentas podem ficar para depois?
- Como ele trata detalhes de contrato, arquivos, licitacoes e fornecedores?
- Existem convencoes de parametros que vale reutilizar conceitualmente?
- Quais partes pertencem ao mundo MCP e nao devem entrar no Sherlock neste momento?

### Arquivo esperado

- [x] `documentation/projetos-similares/analise-licinexus-para-sherlock.md`

### Criterio de conclusao

Ter uma lista priorizada de funcoes PNCP para implementar em Python no Sherlock Holmes.

### Status

Concluida como analise inicial.

Antes de iniciar codigo, falta transformar a recomendacao tecnica em escopo fechado da primeira entrega PNCP.

## 8. Fase 3: Reestruturar a Camada PNCP em Python

### Objetivo

Transformar o modulo PNCP atual em uma camada mais modular, extensivel e alinhada ao dominio.

### Estrutura sugerida

```text
src/sherlock_holmes/pncp/
|-- client.py
|-- contratos.py
|-- licitacoes.py
|-- arquivos.py
|-- atas.py
|-- orgaos.py
|-- fornecedores.py
|-- pca.py
`-- schemas.py
```

### Tarefas

- Manter `client.py` como camada HTTP/base.
- Extrair funcoes de contratos para `contratos.py`.
- Criar funcoes para licitacoes.
- Criar funcoes para arquivos/anexos.
- Definir schemas ou dataclasses para respostas importantes.
- Padronizar erros e metadados de requisicao.
- Atualizar scripts existentes para usar a nova camada.

### Funcoes prioritarias

```text
search_contratos
get_contrato
list_contrato_arquivos
list_contrato_termos
search_licitacoes
get_licitacao
list_licitacao_itens
list_licitacao_arquivos
get_fornecedor_contratos
```

### Criterio de conclusao

O Sherlock deve conseguir consultar contratos, licitacoes e arquivos relacionados usando funcoes claras, testaveis e reutilizaveis.

## 9. Fase 4: Adicionar Enriquecimento de CNPJ

### Objetivo

Enriquecer orgaos e fornecedores com dados cadastrais publicos.

### Estrutura sugerida

```text
src/sherlock_holmes/enrichment/
|-- __init__.py
`-- brasilapi.py
```

### Tarefas

- [x] Criar client simples para BrasilAPI.
- [x] Normalizar CNPJ antes da consulta.
- [x] Salvar payload bruto quando usado em execucoes.
- [x] Padronizar campos principais.
- [~] Integrar enriquecimento nos fluxos de comparacao.

### Campos uteis

- razao social;
- nome fantasia;
- CNAE;
- municipio;
- UF;
- situacao cadastral;
- data de abertura;
- capital social;
- socios, quando disponivel.

### Criterio de conclusao

Dado um CNPJ de fornecedor ou orgao, o projeto consegue recuperar e registrar dados cadastrais com fonte e data de coleta.

### Status

Concluida como primeira versao funcional.

O modulo `sherlock_holmes.enrichment.brasilapi` cria URL oficial da BrasilAPI, normaliza CNPJ, transforma payload em registro padronizado, preserva payload bruto, escreve JSON e cria evidencia `official_api`.

Pendencias de refinamento:

- gerar relatorios de fornecedores enriquecidos;
- avaliar cache/persistencia para evitar chamadas repetidas.

## 10. Fase 5: Criar Camada de Matching e Comparacao

### Objetivo

Construir a principal diferenciacao do Sherlock Holmes: comparar uma fonte manual com dados oficiais.

### Estrutura sugerida

```text
src/sherlock_holmes/validation/
|-- __init__.py
|-- matcher.py
|-- comparer.py
`-- evidence.py
```

### Tarefas

- [x] Definir campos comparaveis entre planilha manual e PNCP.
- [x] Criar normalizadores para CNPJ, datas, valores e texto.
- [x] Criar scoring de candidatos.
- [x] Criar comparacao campo a campo.
- [x] Registrar divergencias.
- [x] Registrar casos inconclusivos.
- [ ] Refinar matching textual para descricoes resumidas versus objetos PNCP completos.
- [ ] Formalizar status de revisao documental e confirmacao humana.

### Status de comparacao

```text
match
partial_match
divergent
missing_in_manual
missing_in_pncp
requires_document_review
unresolved
```

### Criterio de conclusao

Dada uma linha manual e uma lista de candidatos PNCP, o projeto consegue indicar o melhor candidato, justificar o score e comparar campos principais.

### Status

Concluida como primeira versao funcional.

A camada `validation/comparison.py` compara campos e registros completos, a orquestracao em `investigation.py` ranqueia candidatos, e a linha `67` foi validada com busca paginada no PNCP. O melhor candidato identificado foi `39485438000142-2-000019/2025`, com score `0.85` e status `partial_match`.

Pendencias de refinamento:

- melhorar comparacao textual para objetos contratuais resumidos;
- diferenciar melhor `partial_match` forte de caso que exige revisao documental;
- formalizar confirmacao humana como evidencia revisada.

## 11. Fase 6: Criar Modelo de Evidencia e Confianca

### Objetivo

Garantir rastreabilidade por campo e evitar mistura entre fonte oficial, inferencia e extracao automatica.

### Tipos de origem

```text
official_api
official_document
manual_spreadsheet
ocr_extracted
llm_extracted
human_reviewed
unresolved
```

### Niveis de confianca

```text
high
medium
low
reviewed
unknown
```

### Tarefas

- Criar schema de evidencia.
- Registrar URL ou caminho de origem.
- Registrar data de coleta.
- Registrar metodo de obtencao.
- Associar cada campo comparado a uma evidencia.

### Criterio de conclusao

Todo campo relevante em uma comparacao deve poder apontar para uma fonte, um metodo e um nivel de confianca.

## 12. Fase 7: Reposicionar OCR Como Fallback Documental

### Objetivo

Conectar o trabalho de OCR existente ao novo pipeline.

### Quando usar OCR

- Campo nao existe na API.
- Documento oficial contem informacao necessaria.
- PDF nao possui texto extraivel.
- Anexo e imagem ou documento escaneado.
- Divergencia exige revisao do documento original.

### Tarefas

- Documentar regras de acionamento de OCR.
- Criar fluxo para baixar ou referenciar anexos.
- Detectar se PDF tem texto extraivel antes de OCR.
- Reaproveitar runners existentes.
- Registrar o resultado OCR como evidencia de menor confianca ate revisao humana.

### Criterio de conclusao

OCR deixa de ser uma trilha isolada e passa a ser acionado dentro do fluxo de investigacao quando necessario.

## 13. Fase 8: Evoluir Streamlit Para Investigacao

### Objetivo

Transformar o app Streamlit em uma interface de exploracao e revisao.

### Telas sugeridas

- busca PNCP;
- contratos encontrados;
- detalhe do contrato;
- arquivos/anexos;
- comparacao manual versus oficial;
- divergencias;
- fornecedor enriquecido;
- status de revisao documental;
- exportacao CSV.

### Criterio de conclusao

Um usuario deve conseguir consultar contratos, escolher candidatos, ver divergencias e acessar evidencias sem depender apenas de arquivos locais.

## 14. Fase 9: Criar Relatorios Auditaveis

### Objetivo

Gerar saidas claras para revisao tecnica.

### Relatorios esperados

- [~] contratos encontrados;
- [ ] contratos nao encontrados;
- [x] candidatos por linha manual;
- [x] comparacao campo a campo;
- [x] divergencias;
- [ ] fornecedores enriquecidos;
- [x] documentos oficiais vinculados;
- [ ] documentos que exigem revisao/OCR;
- [ ] documentos processados por OCR;
- [ ] relatorio final de evidencias.

### Criterio de conclusao

Cada execucao relevante deve gerar artefatos em CSV/JSON/Markdown suficientes para auditoria posterior.

### Status

Em andamento.

A primeira entrega criou `sherlock_holmes.reporting.audit` e `scripts/generate_audit_report.py`, gerando JSON e Markdown a partir do resultado de comparacao da linha `67`. A camada tambem ja aceita referencias de documentos oficiais previamente coletadas e soma esses documentos no relatorio consolidado.

Pendencias:

- incluir enriquecimento CNPJ quando disponivel;
- incluir documentos que exigem revisao/OCR.

## 15. Fase 10: Avaliar MCP, LLM e Automacao

### Objetivo

Planejar camadas futuras sem desviar o foco atual.

### Possibilidades futuras

- Criar MCP proprio do Sherlock.
- Usar LLM para consultar relatorios ja gerados.
- Criar automacoes recorrentes inspiradas em n8n.
- Gerar alertas por palavra-chave, CNPJ ou orgao.
- Integrar com planilhas, Notion, Slack, Teams ou email.

### Regra

LLM e automacao devem consumir dados estruturados e evidencias ja coletadas. Eles nao devem substituir a camada auditavel.

## 16. Primeira Sequencia Recomendada

### Sprint documental

1. [x] Atualizar `documentation/overview-sherlock-holmes.md`.
2. [x] Criar uma secao explicita de principios: fonte, evidencia, confianca e OCR como fallback.
3. [x] Criar um relatorio curto consolidando a decisao de reposicionamento.

### Sprint de estudo tecnico

1. [x] Clonar o Licinexus MCP fora do fluxo principal do Sherlock ou em pasta local ignorada.
2. [x] Mapear tools e endpoints.
3. [x] Criar `analise-licinexus-para-sherlock.md`.
4. [x] Priorizar funcoes PNCP para implementar.

### Sprint de implementacao PNCP

1. Reorganizar `src/sherlock_holmes/pncp`.
2. Criar funcoes de contratos e arquivos.
3. Adicionar funcoes de licitacoes.
4. Atualizar smoke tests/scripts.
5. Registrar resultados em `documentation/reports`.

## 17. Checklist de Prontidao Para Comecar Implementacao

Antes de mexer em codigo, confirmar:

- [x] overview atualizado;
- [x] decisao de reposicionamento registrada;
- [x] lista priorizada de funcoes PNCP;
- [x] entendimento minimo da estrutura do Licinexus;
- [x] escopo da primeira implementacao fechado;
- [x] criterio de validacao local definido.

## 18. Proximo Passo Imediato

O plano esta atualizado ate a consolidacao da Fase 5 como primeira versao funcional.

Proximos caminhos possiveis:

1. Iniciar Fase 4: enriquecimento de CNPJ via BrasilAPI.
2. Lapidar Fase 5: matching textual, revisao documental e confirmacao humana.
3. Avancar Fase 9: relatorios auditaveis.

A escolha do proximo passo fica pendente de decisao do usuario.
