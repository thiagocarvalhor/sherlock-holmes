# Decisao de Reposicionamento do Sherlock Holmes

## Objetivo

Registrar a decisao de reposicionar o projeto `sherlock-holmes` como um pipeline tecnico e auditavel para busca, validacao, comparacao e preservacao de evidencias em contratos publicos.

## Decisao

O Sherlock Holmes nao deve ser tratado principalmente como um projeto de OCR.

O novo posicionamento do projeto e:

```text
PNCP primeiro.
Documentos depois.
OCR apenas quando necessario.
Evidencia sempre.
```

O PNCP passa a ser a fonte primaria sempre que oferecer dados estruturados suficientes. Documentos oficiais entram como evidencia complementar. OCR permanece importante, mas como fallback documental quando a API ou a extracao textual direta nao resolverem.

## Racional

A analise de projetos similares indicou que ja existem iniciativas focadas em acesso, visualizacao ou automacao de dados publicos:

- Licinexus MCP: acesso estruturado e conversacional a dados do PNCP e BrasilAPI.
- LicitaNow: dashboards e rankings com dados do PNCP.
- n8n-nodes-pncp-aec: automacao e alertas para licitacoes.
- DeOlho: principios de transparencia, evidencia obrigatoria e responsabilidade civica.

A diferenciacao do Sherlock Holmes deve estar na combinacao entre:

- busca oficial;
- comparacao com fonte manual;
- rastreabilidade por campo;
- evidencia preservada;
- divergencias auditaveis;
- fallback documental;
- revisao humana.

## Impacto no Projeto

### Camada PNCP

A camada PNCP passa a ser o nucleo tecnico prioritario.

Proximas evolucoes esperadas:

- reestruturar `src/sherlock_holmes/pncp` em modulos mais especificos;
- ampliar consultas para contratos, licitacoes, arquivos, termos, fornecedores e PCA;
- preservar URLs, parametros, payloads e metadados oficiais;
- preparar dados para comparacao com fontes manuais.

### Camada OCR

OCR deixa de ser uma trilha isolada de benchmark e passa a ser uma camada de apoio.

OCR deve ser acionado quando:

- o campo necessario nao existir na API;
- a informacao estiver apenas em documento oficial;
- o documento for escaneado ou imagem;
- um PDF nao tiver texto extraivel;
- uma divergencia exigir revisao do documento original.

Resultados de OCR devem ser registrados com origem, metodo e nivel de confianca.

### Camada de Validacao

O projeto deve evoluir para comparar dados manuais e oficiais campo a campo.

Status sugeridos:

- `match`;
- `partial_match`;
- `divergent`;
- `missing_in_manual`;
- `missing_in_pncp`;
- `requires_document_review`;
- `unresolved`.

### Modelo de Evidencia

Toda informacao relevante deve apontar para uma origem.

Tipos de origem sugeridos:

- `official_api`;
- `official_document`;
- `manual_spreadsheet`;
- `ocr_extracted`;
- `llm_extracted`;
- `human_reviewed`;
- `unresolved`.

## Artefatos Atualizados

- `documentation/overview-sherlock-holmes.md` foi atualizado com o novo posicionamento.
- `documentation/projetos-similares/plano-execucao-roadmap-sherlock-holmes.md` foi atualizado como plano local de acompanhamento.

## Proximo Passo Operacional

Estudar melhor a estrutura tecnica do Licinexus MCP antes de iniciar mudancas de codigo na camada PNCP.

Objetivos desse estudo:

- mapear tools e endpoints PNCP;
- identificar funcoes prioritarias para o Sherlock Holmes;
- separar o que e inspiracao de dominio do que pertence especificamente ao mundo MCP;
- criar uma matriz entre tools do Licinexus e funcoes Python desejadas no Sherlock.
