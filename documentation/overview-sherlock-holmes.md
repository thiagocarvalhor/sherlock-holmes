# Overview do Repositorio Sherlock Holmes

## Visao Geral

O `sherlock-holmes` e um projeto de investigacao tecnica para localizar, validar e comparar contratos publicos a partir de fontes oficiais, fontes manuais e documentos associados.

O novo posicionamento do projeto e:

```text
PNCP primeiro.
Documentos depois.
OCR apenas quando necessario.
Evidencia sempre.
```

Na pratica, o Sherlock Holmes deve evoluir para um pipeline auditavel capaz de:

- receber uma planilha manual ou demanda de investigacao;
- buscar contratos, licitacoes, orgaos, fornecedores e documentos no PNCP;
- comparar dados manuais com dados oficiais;
- identificar divergencias, ausencias e pontos que exigem revisao;
- preservar fontes, URLs, metadados e nivel de confianca;
- acionar parsing documental ou OCR somente quando os dados estruturados nao forem suficientes.

O projeto ainda nao e um sistema final de producao. Ele esta em fase de validacao, organizacao de arquitetura e construcao incremental de evidencias.

## Papel de Cada Camada

### PNCP Como Fonte Primaria

O PNCP deve ser tratado como a primeira fonte de verdade operacional do projeto sempre que oferecer dados estruturados suficientes.

Essa camada deve responder perguntas como:

- o contrato existe no PNCP?
- qual e o numero de controle PNCP?
- qual orgao contratou?
- qual fornecedor aparece nos dados oficiais?
- quais valores, vigencias e objetos estao registrados?
- quais documentos ou anexos estao vinculados?
- quais licitacoes, itens, atas, termos ou PCA se relacionam ao caso?

### Fonte Manual Como Entrada de Investigacao

Planilhas e bases manuais nao devem ser descartadas. Elas sao entradas importantes para investigacao, mas precisam ser comparadas com fontes oficiais.

Exemplos de campos manuais:

- municipio;
- UF;
- CNPJ;
- fornecedor;
- numero do contrato;
- vigencia;
- valor;
- objeto;
- URL ou fonte indicada.

O objetivo nao e assumir que a planilha esta certa ou errada. O objetivo e produzir uma comparacao rastreavel.

### Documentos Oficiais Como Evidencia Complementar

Quando a API nao trouxer todos os campos necessarios, o proximo passo deve ser consultar documentos oficiais vinculados ao contrato ou licitacao.

Exemplos:

- contrato em PDF;
- termo aditivo;
- edital;
- termo de referencia;
- ata;
- anexos;
- instrumentos de cobranca.

Antes de usar OCR, o projeto deve tentar extrair texto diretamente do documento quando houver camada textual disponivel.

### OCR Como Fallback

OCR continua sendo relevante, mas nao deve ser o centro do projeto.

Ele deve ser acionado quando:

- o campo necessario nao aparece na API;
- a informacao esta apenas em documento oficial;
- o documento e escaneado ou imagem;
- o PDF nao tem texto extraivel;
- uma divergencia exige consulta ao documento original.

O resultado de OCR deve ser registrado como evidencia com confianca menor ate passar por revisao humana ou validacao adicional.

### Evidencia e Confianca

Toda informacao relevante deve carregar uma origem clara.

Tipos de origem esperados:

- `official_api`: dado estruturado retornado pelo PNCP;
- `official_document`: dado extraido de documento oficial;
- `manual_spreadsheet`: dado vindo de planilha ou fonte manual;
- `ocr_extracted`: dado extraido por OCR;
- `llm_extracted`: dado inferido ou estruturado com auxilio de LLM;
- `human_reviewed`: dado revisado manualmente;
- `unresolved`: dado ainda sem confirmacao suficiente.

Niveis de confianca sugeridos:

- `high`: dado oficial estruturado;
- `medium`: dado extraido de documento oficial;
- `low`: dado extraido automaticamente sem revisao;
- `reviewed`: dado validado por pessoa;
- `unknown`: origem ou qualidade insuficiente.

## Diferenciacao do Sherlock Holmes

O Sherlock Holmes nao deve ser apenas mais um cliente da API do PNCP.

Projetos similares ajudam a delimitar o espaco:

- Licinexus MCP facilita acesso conversacional e estruturado a dados do PNCP e BrasilAPI.
- LicitaNow mostra dashboards e rankings sobre contratacoes publicas.
- n8n-nodes-pncp-aec aponta caminhos para automacao e alertas recorrentes.
- DeOlho inspira principios de transparencia, evidencia obrigatoria e responsabilidade.

A diferenciacao do Sherlock Holmes deve estar nesta combinacao:

```text
busca oficial
+ comparacao com fonte manual
+ rastreabilidade por campo
+ evidencia preservada
+ divergencias auditaveis
+ fallback documental
+ revisao humana
```

Em vez de apenas encontrar dados, o projeto deve explicar de onde cada dado veio, o quanto ele e confiavel e como ele se compara com outra fonte.

## Estrutura Principal

```text
sherlock-holmes/
|-- src/
|   `-- sherlock_holmes/
|       |-- ocr/
|       |-- pncp/
|       `-- preprocessing/
|-- scripts/
|-- documentation/
|   |-- context/
|   |-- plans/
|   |-- reports/
|   `-- source/
|-- notebooks/
|-- data/
|-- outputs/
|-- tests/
|-- requirements-ocr.txt
|-- requirements-streamlit.txt
`-- AGENTS.md
```

## Codigo Fonte

O codigo reutilizavel fica em `src/sherlock_holmes`.

### `src/sherlock_holmes/pncp`

Contem a camada atual de comunicacao com APIs publicas do PNCP.

Arquivo principal atual:

- `client.py`

Responsabilidades atuais:

- montar URLs da API;
- normalizar CNPJ e textos;
- executar requisicoes HTTP;
- buscar contratos por data de publicacao;
- buscar metadados de arquivos anexados a contratos;
- gerar URLs diretas para detalhes e downloads;
- filtrar contratos por termos no objeto contratual.

Evolucao esperada:

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

Funcoes prioritarias para evolucao:

- `search_contratos`;
- `get_contrato`;
- `list_contrato_arquivos`;
- `list_contrato_termos`;
- `search_licitacoes`;
- `get_licitacao`;
- `list_licitacao_itens`;
- `list_licitacao_arquivos`;
- `get_fornecedor_contratos`.

### `src/sherlock_holmes/ocr`

Contem a camada de OCR existente.

Arquivos principais:

- `extractors.py`;
- `manifest_runner.py`.

O `extractors.py` define uma interface comum para:

- `tesseract`;
- `paddleocr`;
- `doctr`.

Cada ferramenta retorna:

- texto extraido;
- saida bruta;
- confianca media, quando disponivel.

O `manifest_runner.py` executa OCR em lote a partir de um manifesto CSV, aplica pre-processamento, salva JSON por documento e gera um `summary.csv` com metricas consolidadas.

Essa camada deve continuar existindo, mas conectada ao fluxo documental do projeto.

### `src/sherlock_holmes/preprocessing`

Contem presets de pre-processamento de imagem.

Arquivo principal:

- `presets.py`.

Presets disponiveis:

- `none`: usa a imagem original;
- `basic`: converte para escala de cinza e aumenta contraste;
- `binarized`: converte para escala de cinza e aplica threshold de Otsu;
- `deskew_binarized`: tenta corrigir inclinacao e depois binariza.

Esses presets permitem comparar se tratamentos simples melhoram ou pioram o OCR.

### Camadas Futuras Esperadas

O roadmap sugere novas camadas:

```text
src/sherlock_holmes/enrichment/
|-- brasilapi.py

src/sherlock_holmes/validation/
|-- matcher.py
|-- comparer.py
`-- evidence.py
```

`enrichment` deve enriquecer CNPJ de orgaos e fornecedores com dados publicos.

`validation` deve concentrar matching, comparacao campo a campo, divergencias e evidencias.

## Scripts

A pasta `scripts` contem comandos operacionais e utilitarios.

### PNCP

- `generate_pncp_manual_manifest.py`
  - gera um manifesto intermediario a partir da planilha manual em `documentation/source`.

- `run_pncp_api_smoke.py`
  - executa consultas pequenas na API do PNCP;
  - salva respostas brutas em `data/raw/pncp`;
  - salva candidatos e resumos em `data/processed/pncp`.

- `pncp_streamlit_app.py`
  - abre uma interface Streamlit para explorar contratos do PNCP;
  - permite filtrar por orgao, ano, tema e palavras-chave;
  - lista contratos e arquivos associados.

### OCR

- `generate_ocr_sample_manifests.py`
  - cria amostras versionaveis para smoke test e benchmark.

- `run_ocr_smoke.py`
  - roda OCR em uma amostra pequena;
  - util para validar instalacao, compatibilidade e saida.

- `run_ocr_manifest.py`
  - roda OCR em qualquer manifesto CSV informado.

- `convert_pdf_to_ocr_images.py`
  - converte paginas de PDF em imagens para posterior OCR.

- `collect_ocr_text.py`
  - consolida textos extraidos por OCR.

## Fluxo Conceitual Alvo

```text
Planilha manual / demanda de investigacao
        |
        v
Normalizacao da entrada
        |
        v
Busca no PNCP
        |
        v
Contratos, licitacoes, orgaos, fornecedores e documentos candidatos
        |
        v
Comparacao com fonte manual
        |
        v
Registro de matches, divergencias e lacunas
        |
        v
Consulta a documentos/anexos quando necessario
        |
        v
Extracao direta de texto ou OCR como fallback
        |
        v
Relatorios auditaveis com evidencia e confianca
```

## Documentacao

A pasta `documentation` e parte central do projeto. Ela registra contexto, planejamento e decisoes.

### `documentation/context`

Guarda analises de contexto tecnico.

Exemplos:

- `tools-analysis.md`
  - levantamento de ferramentas de OCR, PDF, layout e extracao.

- `pncp-api-consultas.md`
  - notas sobre a API de consultas do PNCP.

### `documentation/plans`

Guarda planos de execucao e manifests pequenos versionaveis.

Exemplos importantes:

- `ocr-execution-plan-v1.md`
  - plano da rodada inicial de OCR.

- `pncp-api-execution-plan.md`
  - plano da validacao inicial da API PNCP.

- `ocr-smoke-sample-v1.csv`
  - amostra reduzida para smoke test OCR.

- `ocr-benchmark-sample-v1.csv`
  - amostra maior para benchmark OCR.

- `pncp-api-smoke-sample.csv`
  - amostra pequena para validacao da API PNCP.

### `documentation/reports`

Guarda relatorios de execucao, ambiente, resultados e decisoes.

Exemplos:

- `ocr-run-001-environment.md`;
- `ocr-run-001-smoke-dev.md`;
- `ocr-run-001-smoke-none.md`;
- `pncp-streamlit-explorer.md`;
- `ocr-pdf-conversion-setup.md`.

Esses arquivos contam o historico real do que ja foi executado, quais problemas apareceram e quais decisoes foram tomadas.

### `documentation/source`

Guarda fontes manuais ou documentos de referencia.

Exemplos:

- PDFs da documentacao do PNCP;
- planilhas de exemplo;
- arquivos usados como base para gerar manifests.

### `documentation/projetos-similares`

Pasta local ignorada pelo Git para guardar referencias externas, analises e planos exploratorios.

Ela serve para pesquisa e comparacao, nao como documentacao oficial versionada do projeto.

## Dados Locais

A pasta `data` e usada para dados de execucao, mas esta ignorada pelo Git.

Convencao geral:

```text
data/raw/
data/interim/
data/processed/
```

Uso esperado:

- `data/raw`: dados brutos baixados ou recebidos;
- `data/interim`: arquivos intermediarios, como imagens pre-processadas;
- `data/processed`: resultados finais de uma execucao local, como JSONs e CSVs consolidados.

Como esses arquivos podem ser grandes ou sensiveis, eles nao devem ser versionados por padrao.

## Notebooks

A pasta `notebooks` contem apoio para inspecao manual.

Arquivo atual:

- `ocr-result-review.ipynb`.

Ele serve para revisar visualmente:

- imagem original;
- imagem pre-processada;
- texto extraido;
- metricas de execucao;
- comparacao entre ferramentas.

Essa revisao e importante porque uma ferramenta pode gerar muito texto, mas ainda assim produzir uma saida pouco util.

## Dependencias

O projeto separa dependencias por frente de trabalho.

### OCR

Arquivo:

```powershell
requirements-ocr.txt
```

Inclui bibliotecas como:

- `Pillow`;
- `opencv-python`;
- `pytesseract`;
- `paddleocr`;
- `paddlepaddle`;
- `python-doctr`;
- `torch`;
- `torchvision`;
- `pandas`;
- `ipykernel`;
- `pypdfium2`.

### Streamlit

Arquivo:

```powershell
requirements-streamlit.txt
```

Inclui:

- `streamlit`;
- `pandas`.

## Comandos Uteis

Os comandos Python devem usar o ambiente virtual local:

```powershell
.venv\Scripts\python.exe
```

### Rodar Smoke da API PNCP

```powershell
.venv\Scripts\python.exe scripts\run_pncp_api_smoke.py --limit 1 --run-id pncp-api-smoke-local
```

### Rodar OCR em Smoke Test

```powershell
.venv\Scripts\python.exe scripts\run_ocr_smoke.py --tool tesseract --preset none --run-id ocr-smoke-local
```

### Rodar OCR Usando Manifesto Especifico

```powershell
.venv\Scripts\python.exe scripts\run_ocr_manifest.py --tool tesseract --preset none --manifest documentation\plans\ocr-smoke-sample-v1.csv --run-id ocr-manifest-local
```

### Abrir o Explorador PNCP em Streamlit

```powershell
.venv\Scripts\python.exe -m streamlit run scripts\pncp_streamlit_app.py
```

## Estado Atual do Projeto

### Frente PNCP

O projeto ja possui:

- plano de validacao da API;
- amostra de smoke;
- script para consultar a API;
- cliente reutilizavel em `src`;
- app Streamlit para exploracao;
- primeiras validacoes com retorno real da API.

Aprendizado principal ate agora:

- buscar contratos no PNCP sem filtros fortes pode retornar volume alto demais;
- quando o CNPJ do manifesto corresponde ao `cnpjOrgao`, a busca fica muito mais precisa;
- para varias linhas ainda e preciso confirmar se o CNPJ disponivel representa o orgao contratante ou outra entidade.

Proximo passo tecnico:

- estudar melhor a estrutura do Licinexus MCP;
- priorizar funcoes PNCP;
- reestruturar `src/sherlock_holmes/pncp` em modulos menores;
- preparar matching manual versus oficial.

### Frente OCR

O projeto ja possui:

- ambiente OCR configurado;
- runners para smoke test e execucao por manifesto;
- adapters para `Tesseract`, `PaddleOCR` e `docTR`;
- presets de pre-processamento;
- manifests de amostra;
- notebook de revisao;
- relatorios de ambiente e smoke test.

Resultados ja registrados indicam que, com preset `none`, as tres ferramentas executaram com sucesso no smoke completo de 30 imagens:

- `Tesseract + none`;
- `docTR + none`;
- `PaddleOCR + none`.

Proximo passo nessa frente:

- revisar qualitativamente os resultados do preset `none`;
- depois conectar OCR ao fluxo de documentos/anexos, em vez de trata-lo como trilha isolada.

## Ordem Recomendada de Execucao

1. Consolidar esta narrativa no overview e em um relatorio de decisao.
2. Estudar o Licinexus MCP como referencia tecnica para PNCP.
3. Reestruturar a camada PNCP em Python.
4. Adicionar enriquecimento de CNPJ via BrasilAPI.
5. Criar matching e comparacao manual versus oficial.
6. Criar modelo de evidencia e confianca.
7. Integrar documentos e OCR como fallback.
8. Evoluir Streamlit para investigacao e revisao.
9. Gerar relatorios auditaveis.
10. Avaliar MCP, LLM e automacao somente depois da base auditavel.

## Cuidados Importantes

- Nao versionar dados grandes ou locais em `data/raw`, `data/interim`, `data/processed`, `.cache`, `.venv`, `.local` ou `documentation/projetos-similares`.
- Registrar decisoes relevantes em `documentation/reports`.
- Atualizar planos em `documentation/plans` quando o escopo ou status operacional mudar.
- Nao aprovar ferramenta de OCR apenas por metrica automatica; revisao qualitativa continua necessaria.
- Preservar planilhas e PDFs originais em `documentation/source`.
- Separar dado oficial, dado manual, dado extraido e dado revisado.
- Nao apresentar divergencia como acusacao automatica.
- Nao fazer commits automaticamente sem confirmacao.

## Leitura Recomendada Para Novos Contribuidores

Para entender o projeto rapidamente, leia nesta ordem:

1. `AGENTS.md`
2. `documentation/overview-sherlock-holmes.md`
3. `documentation/plans/pncp-api-execution-plan.md`
4. `documentation/plans/ocr-execution-plan-v1.md`
5. `documentation/reports/ocr-run-001-environment.md`
6. `documentation/reports/ocr-run-001-smoke-none.md`
7. `src/sherlock_holmes/pncp/client.py`
8. `src/sherlock_holmes/ocr/extractors.py`
9. `src/sherlock_holmes/preprocessing/presets.py`

## Resumo em Uma Frase

O Sherlock Holmes e um pipeline tecnico e auditavel para localizar contratos publicos, comparar fontes manuais com dados oficiais, preservar evidencias e acionar documentos ou OCR apenas quando os dados estruturados nao forem suficientes.
