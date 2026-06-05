# Overview do Repositório Sherlock Holmes

## Visão Geral

O repositório `sherlock-holmes` é um projeto de investigação e validação técnica para trabalhar com contratos públicos, documentos oficiais e extração de informações.

Na prática, ele está organizado em duas frentes principais:

1. **PNCP**
   - consultar a API pública do Portal Nacional de Contratações Públicas;
   - reencontrar contratos que já aparecem em uma planilha manual;
   - comparar dados manuais com dados oficiais retornados pela API;
   - preparar o caminho para baixar ou referenciar documentos oficiais.

2. **OCR**
   - testar ferramentas de reconhecimento óptico de caracteres em documentos escaneados;
   - comparar ferramentas como `Tesseract`, `PaddleOCR` e `docTR`;
   - medir estabilidade, tempo de execução e quantidade de texto extraído;
   - avaliar se o texto extraído é útil para etapas futuras de classificação e extração de campos.

O projeto ainda tem caráter experimental. Ele não é, por enquanto, um pipeline final de produção. A prioridade atual é gerar evidências confiáveis para decidir quais caminhos técnicos seguir.

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

## Código Fonte

O código reutilizável fica em `src/sherlock_holmes`.

### `src/sherlock_holmes/pncp`

Contém o cliente mínimo para conversar com APIs públicas do PNCP.

Arquivo principal:

- `client.py`

Responsabilidades:

- montar URLs da API;
- normalizar CNPJ e textos;
- executar requisições HTTP;
- buscar contratos por data de publicação;
- buscar metadados de arquivos anexados a contratos;
- gerar URLs diretas para detalhes e downloads;
- filtrar contratos por termos no objeto contratual.

Esse módulo é usado principalmente pelo app Streamlit em `scripts/pncp_streamlit_app.py`.

### `src/sherlock_holmes/ocr`

Contém a camada de OCR.

Arquivos principais:

- `extractors.py`
- `manifest_runner.py`

O `extractors.py` define uma interface comum para três ferramentas:

- `tesseract`
- `paddleocr`
- `doctr`

Cada ferramenta retorna um objeto padronizado com:

- texto extraído;
- saída bruta;
- confiança média, quando disponível.

O `manifest_runner.py` executa OCR em lote a partir de um manifesto CSV. Ele aplica pré-processamento, roda a ferramenta escolhida, salva um JSON por documento e gera um `summary.csv` com métricas consolidadas.

### `src/sherlock_holmes/preprocessing`

Contém os presets de pré-processamento de imagem.

Arquivo principal:

- `presets.py`

Presets disponíveis:

- `none`: usa a imagem original;
- `basic`: converte para escala de cinza e aumenta contraste;
- `binarized`: converte para escala de cinza e aplica threshold de Otsu;
- `deskew_binarized`: tenta corrigir inclinação e depois binariza.

Esses presets permitem comparar se tratamentos simples melhoram ou pioram o OCR.

## Scripts

A pasta `scripts` contém comandos operacionais e utilitários.

### PNCP

- `generate_pncp_manual_manifest.py`
  - gera um manifesto intermediário a partir da planilha manual em `documentation/source`.

- `run_pncp_api_smoke.py`
  - executa consultas pequenas na API do PNCP;
  - salva respostas brutas em `data/raw/pncp`;
  - salva candidatos e resumos em `data/processed/pncp`.

- `pncp_streamlit_app.py`
  - abre uma interface Streamlit para explorar contratos do PNCP;
  - permite filtrar por órgão, ano, tema e palavras-chave;
  - lista contratos e arquivos associados.

### OCR

- `generate_ocr_sample_manifests.py`
  - cria amostras versionáveis para smoke test e benchmark.

- `run_ocr_smoke.py`
  - roda OCR em uma amostra pequena;
  - útil para validar instalação, compatibilidade e saída.

- `run_ocr_manifest.py`
  - roda OCR em qualquer manifesto CSV informado.

- `convert_pdf_to_ocr_images.py`
  - converte páginas de PDF em imagens para posterior OCR.

- `collect_ocr_text.py`
  - consolida textos extraídos por OCR.

## Documentação

A pasta `documentation` é parte central do projeto. Ela registra contexto, planejamento e decisões.

### `documentation/context`

Guarda análises de contexto técnico.

Exemplos:

- `tools-analysis.md`
  - levantamento de ferramentas de OCR, PDF, layout e extração.

- `pncp-api-consultas.md`
  - notas sobre a API de consultas do PNCP.

### `documentation/plans`

Guarda planos de execução e manifests pequenos versionáveis.

Exemplos importantes:

- `ocr-execution-plan-v1.md`
  - plano da rodada inicial de OCR.

- `pncp-api-execution-plan.md`
  - plano da validação inicial da API PNCP.

- `ocr-smoke-sample-v1.csv`
  - amostra reduzida para smoke test OCR.

- `ocr-benchmark-sample-v1.csv`
  - amostra maior para benchmark OCR.

- `pncp-api-smoke-sample.csv`
  - amostra pequena para validação da API PNCP.

### `documentation/reports`

Guarda relatórios de execução, ambiente e resultados.

Exemplos:

- `ocr-run-001-environment.md`
- `ocr-run-001-smoke-dev.md`
- `ocr-run-001-smoke-none.md`
- `pncp-streamlit-explorer.md`
- `ocr-pdf-conversion-setup.md`

Esses arquivos contam o histórico real do que já foi executado, quais problemas apareceram e quais decisões foram tomadas.

### `documentation/source`

Guarda fontes manuais ou documentos de referência.

Exemplos:

- PDFs da documentação do PNCP;
- planilhas de exemplo;
- arquivos usados como base para gerar manifests.

## Dados Locais

A pasta `data` é usada para dados de execução, mas está ignorada pelo Git.

Convenção geral:

```text
data/raw/
data/interim/
data/processed/
```

Uso esperado:

- `data/raw`: dados brutos baixados ou recebidos;
- `data/interim`: arquivos intermediários, como imagens pré-processadas;
- `data/processed`: resultados finais de uma execução local, como JSONs e CSVs consolidados.

Como esses arquivos podem ser grandes ou sensíveis, eles não devem ser versionados por padrão.

## Notebooks

A pasta `notebooks` contém apoio para inspeção manual.

Arquivo atual:

- `ocr-result-review.ipynb`

Ele serve para revisar visualmente:

- imagem original;
- imagem pré-processada;
- texto extraído;
- métricas de execução;
- comparação entre ferramentas.

Essa revisão é importante porque uma ferramenta pode gerar muito texto, mas ainda assim produzir uma saída pouco útil.

## Dependências

O projeto separa dependências por frente de trabalho.

### OCR

Arquivo:

```powershell
requirements-ocr.txt
```

Inclui bibliotecas como:

- `Pillow`
- `opencv-python`
- `pytesseract`
- `paddleocr`
- `paddlepaddle`
- `python-doctr`
- `torch`
- `torchvision`
- `pandas`
- `ipykernel`
- `pypdfium2`

### Streamlit

Arquivo:

```powershell
requirements-streamlit.txt
```

Inclui:

- `streamlit`
- `pandas`

## Comandos Úteis

Os comandos Python devem usar o ambiente virtual local:

```powershell
.venv\Scripts\python.exe
```

### Rodar smoke da API PNCP

```powershell
.venv\Scripts\python.exe scripts\run_pncp_api_smoke.py --limit 1 --run-id pncp-api-smoke-local
```

### Rodar OCR em smoke test

```powershell
.venv\Scripts\python.exe scripts\run_ocr_smoke.py --tool tesseract --preset none --run-id ocr-smoke-local
```

### Rodar OCR usando manifesto específico

```powershell
.venv\Scripts\python.exe scripts\run_ocr_manifest.py --tool tesseract --preset none --manifest documentation\plans\ocr-smoke-sample-v1.csv --run-id ocr-manifest-local
```

### Abrir o explorador PNCP em Streamlit

```powershell
.venv\Scripts\python.exe -m streamlit run scripts\pncp_streamlit_app.py
```

## Estado Atual do Projeto

### Frente OCR

O projeto já possui:

- ambiente OCR configurado;
- runners para smoke test e execução por manifesto;
- adapters para `Tesseract`, `PaddleOCR` e `docTR`;
- presets de pré-processamento;
- manifests de amostra;
- notebook de revisão;
- relatórios de ambiente e smoke test.

Resultados já registrados indicam que, com preset `none`, as três ferramentas executaram com sucesso no smoke completo de 30 imagens:

- `Tesseract + none`
- `docTR + none`
- `PaddleOCR + none`

O próximo passo recomendado nessa frente é revisar qualitativamente os resultados do preset `none` antes de expandir a matriz para os demais presets.

### Frente PNCP

O projeto já possui:

- plano de validação da API;
- amostra de smoke;
- script para consultar a API;
- cliente reutilizável em `src`;
- app Streamlit para exploração;
- primeiras validações com retorno real da API.

O aprendizado principal até agora é que buscar contratos no PNCP sem filtros fortes pode retornar volume alto demais. Quando o CNPJ do manifesto corresponde ao `cnpjOrgao`, a busca fica muito mais precisa.

O próximo passo recomendado nessa frente é investigar as demais linhas da amostra inicial, confirmando se o CNPJ disponível representa o órgão contratante ou outra entidade.

## Cuidados Importantes

- Não versionar dados grandes ou locais em `data/raw`, `data/interim`, `data/processed`, `.cache`, `.venv` ou `.local`.
- Registrar decisões relevantes em `documentation/reports`.
- Atualizar planos em `documentation/plans` quando o escopo ou status operacional mudar.
- Não aprovar uma ferramenta de OCR apenas por métrica automática; a revisão qualitativa continua necessária.
- Preservar a planilha e os PDFs originais em `documentation/source`.
- Não fazer commits automaticamente sem confirmação.

## Leitura Recomendada Para Novos Contribuidores

Para entender o projeto rapidamente, leia nesta ordem:

1. `AGENTS.md`
2. `documentation/plans/pncp-api-execution-plan.md`
3. `documentation/plans/ocr-execution-plan-v1.md`
4. `documentation/reports/ocr-run-001-environment.md`
5. `documentation/reports/ocr-run-001-smoke-none.md`
6. `src/sherlock_holmes/pncp/client.py`
7. `src/sherlock_holmes/ocr/extractors.py`
8. `src/sherlock_holmes/preprocessing/presets.py`

## Resumo em Uma Frase

O Sherlock Holmes é um laboratório técnico para descobrir, validar e documentar a melhor forma de localizar contratos públicos, acessar seus documentos oficiais e extrair texto útil deles com APIs, parsing e OCR.
