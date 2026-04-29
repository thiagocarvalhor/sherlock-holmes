# Plano de Execução: Validação Inicial de OCR

## Objetivo

Validar, de forma controlada e comparável, quais ferramentas e estratégias de OCR apresentam melhor desempenho inicial para o projeto Sherlock Holmes usando o dataset de documentos escaneados disponível em `data/raw/dataset`.

## Referência de Contexto

O radar técnico de ferramentas está documentado em `documentation/context/tools-analysis.md`.

Este plano usa apenas um subconjunto desse levantamento para manter a fase inicial controlada. Ferramentas citadas no radar, mas não incluídas nesta rodada, devem ser tratadas como candidatas futuras e não como escopo automático da fase 1.

## Escopo da Fase 1

Esta primeira fase terá foco exclusivo na validação inicial de OCR sobre imagens escaneadas já disponíveis no dataset.

### Inclui

- uso do dataset em `data/raw/dataset`
- comparação entre ferramentas de OCR selecionadas
- testes com e sem pré-processamento de imagens
- análise por categorias de documento
- registro de métricas e resultados em artefatos comparáveis

### Não inclui

- classificação de documentos
- extração semântica de campos
- pipeline final de produção
- processamento de PDFs reais do projeto
- tuning avançado ou fine-tuning de modelos

## Critérios de Sucesso

Ao final desta fase, o projeto deve ter evidências suficientes para selecionar uma estratégia inicial de OCR para continuar os próximos experimentos.

Os critérios mínimos de sucesso são:

- pelo menos uma ferramenta principal recomendada para a próxima etapa
- pelo menos uma ferramenta alternativa ou fallback identificada
- resultados comparáveis entre ferramentas usando o mesmo conjunto de amostras
- métricas registradas de tempo, sucesso de execução e volume de texto extraído
- avaliação qualitativa inicial por categoria de documento
- documentação consolidada com conclusões e próximos passos

## Etapas de Execução

### 1. Preparar o dataset de teste

- confirmar a organização das categorias em `data/raw/dataset`
- definir uma amostra inicial equilibrada por categoria
- separar uma amostra pequena para smoke test e outra para benchmark inicial

#### Detalhamento da etapa 1

O dataset atual está organizado em 10 categorias:

- `ADVE`: 230 imagens
- `Email`: 599 imagens
- `Form`: 431 imagens
- `Letter`: 567 imagens
- `Memo`: 620 imagens
- `News`: 188 imagens
- `Note`: 201 imagens
- `Report`: 265 imagens
- `Resume`: 120 imagens
- `Scientific`: 261 imagens

Para esta fase, a estratégia de amostragem será estratificada por categoria, para evitar que categorias maiores distorçam o benchmark inicial.

##### 1.1. Smoke test

Objetivo:
- validar instalação, execução básica e compatibilidade das ferramentas
- detectar erros antes de rodar o benchmark principal

Proposta:
- selecionar `3 imagens por categoria`
- total estimado: `30 imagens`

Critério:
- a seleção deve cobrir as 10 categorias
- manter uma amostra pequena para reduzir custo de iteração

##### 1.2. Benchmark inicial

Objetivo:
- comparar ferramentas e presets em uma amostra pequena, mas já representativa

Proposta:
- selecionar `20 imagens por categoria`
- total estimado: `200 imagens`

Critério:
- usar exatamente a mesma amostra para todas as ferramentas e presets
- manter equilíbrio entre categorias
- respeitar o limite da menor classe disponível sem necessidade de ajuste adicional nesta rodada

##### 1.3. Critérios de seleção da amostra

- priorizar seleção reproduzível
- registrar os caminhos dos arquivos escolhidos
- considerar apenas arquivos `.jpg` nesta rodada
- ignorar arquivos auxiliares do sistema operacional, como `Thumbs.db`
- evitar troca manual de imagens entre rodadas
- manter um arquivo de referência com as amostras do `smoke test` e do `benchmark inicial`

##### 1.4. Artefatos esperados desta etapa

- lista versionável com os arquivos do `smoke test` em `documentation/plans`
- lista versionável com os arquivos do `benchmark inicial` em `documentation/plans`
- documentação curta explicando o critério de amostragem adotado

Arquivos sugeridos:

- `documentation/plans/ocr-smoke-sample-v1.csv`
- `documentation/plans/ocr-benchmark-sample-v1.csv`
- `documentation/plans/ocr-sampling-criteria-v1.md`
- `scripts/generate_ocr_sample_manifests.py`

Observação:

- os arquivos originais do dataset permanecem em `data/raw` e não devem ser versionados
- os manifests das amostras devem ser versionados, pois descrevem quais arquivos foram usados em cada rodada
- o script gerador também deve ser versionado para permitir recriar os manifests

Status atual:

- etapa executada
- dataset confirmado em `data/raw/dataset`
- arquivos `Thumbs.db` identificados e excluídos da amostragem
- manifests gerados:
  - `documentation/plans/ocr-smoke-sample-v1.csv`, com `30` imagens
  - `documentation/plans/ocr-benchmark-sample-v1.csv`, com `200` imagens
- critério de amostragem documentado em `documentation/plans/ocr-sampling-criteria-v1.md`

### 2. Definir as ferramentas da rodada 1

- selecionar as ferramentas de OCR que entrarão no primeiro benchmark
- definir uma ferramenta baseline clássica
- definir pelo menos uma alternativa baseada em deep learning

#### Detalhamento da etapa 2

Nesta primeira rodada, a seleção de ferramentas deve ser pequena o suficiente para viabilizar comparação rápida, mas diversa o suficiente para cobrir abordagens diferentes.

##### 2.1. Ferramentas propostas para a rodada 1

- `Tesseract`
- `PaddleOCR`
- `docTR`

##### 2.2. Papel de cada ferramenta

- `Tesseract`
  - baseline clássica
  - referência de mercado e de comunidade
  - importante para comparar o ganho real das alternativas mais modernas

- `PaddleOCR`
  - baseline moderna com deep learning
  - candidata forte para OCR de documentos escaneados
  - útil para comparar com a abordagem clássica

- `docTR`
  - alternativa moderna com saída mais estruturada
  - relevante para avaliar se há ganho em organização além do texto bruto
  - pode ser útil também em fases futuras do pipeline

##### 2.3. Critérios para entrada na rodada 1

- instalação viável no ambiente do projeto
- execução reproduzível em lote
- capacidade de processar imagens `.jpg`
- possibilidade de extrair texto utilizável para comparação

##### 2.4. Ferramentas que ficam fora desta rodada inicial

As ferramentas abaixo permanecem no radar técnico, mas ficam fora desta rodada para preservar comparabilidade, reduzir custo de setup e manter o foco em OCR local sobre imagens.

- alternativas locais de OCR
  - `EasyOCR`: candidata natural para uma rodada posterior se for necessário ampliar a comparação local
  - `Keras-OCR`: baixa prioridade para pipeline novo, mas pode servir como referência histórica/técnica
  - `Kraken` e `OCRopus`: relevantes apenas se surgirem documentos históricos, manuscritos ou tipografias incomuns

- ferramentas focadas em PDFs, layout ou conversão estruturada
  - `OCRmyPDF`: não entra nesta fase porque o dataset atual é composto por imagens, não PDFs
  - `Docling`, `SmolDocling`, `pymupdf4llm`, `marker-pdf`, `unstructured` e `MinerU`: relevantes para PDFs reais, Markdown estruturado, tabelas e ordem de leitura, mas fora do escopo inicial de OCR em imagens

- ferramentas cloud ou comerciais
  - `Amazon Textract`, `Azure AI Document Intelligence`, `Google Cloud Vision`, `ABBYY`, `Nanonets OCR` e `Rossum.AI`: ficam fora desta rodada para evitar custo, dependência externa, avaliação de privacidade e variação operacional

- modelos multimodais experimentais
  - `DeepSeek-OCR`, `Dots.OCR`, `OLMo-OCR 2`, `Qwen3-VL`, `Donut` e `TrOCR`: ficam fora desta rodada por exigirem validação específica de hardware, licença, maturidade e formato de saída

##### 2.5. Resultado esperado desta etapa

- lista fechada de ferramentas do benchmark inicial
- papel de cada ferramenta documentado
- justificativa registrada para inclusão e exclusão nesta rodada

##### 2.6. Registro de ambiente da rodada

Cada rodada deve registrar as informações mínimas do ambiente de execução:

- sistema operacional
- versão do Python
- versão das bibliotecas instaladas
- versão do Tesseract e idiomas disponíveis
- versão/modelo usado pelo PaddleOCR
- versão/modelo usado pelo docTR
- versão do Pillow e do OpenCV usados no pré-processamento
- uso de CPU ou GPU
- observações de instalação relevantes

Artefato sugerido:

- `documentation/reports/ocr-run-001-environment.md`

Status atual:

- ambiente virtual local criado em `.venv`, com prompt `sherlock-holmes`
- Python do ambiente: `3.10.0`
- dependências diretas registradas em `requirements-ocr.txt`
- `Pillow`, `OpenCV`, `pytesseract`, `PaddleOCR`, `paddlepaddle`, `docTR`, `torch` e `torchvision` instalados no `.venv`
- `docTR` validado em CPU com `torch==2.5.1` e `torchvision==0.20.1`
- `PaddleOCR` validado em CPU com `PP-OCRv4`
- `PaddleOCR` com configuração default `PP-OCRv5` falhou nesta máquina com erro nativo oneDNN/MKLDNN; por isso, a rodada inicial deve usar `PP-OCRv4`
- `Tesseract` instalado em `C:\Program Files\Tesseract-OCR\tesseract.exe`
- `Tesseract` validado em CPU com idioma `eng`
- idiomas Tesseract disponíveis nesta instalação: `eng`, `osd`
- detalhes registrados em `documentation/reports/ocr-run-001-environment.md`

### 3. Definir os presets de pré-processamento

- estabelecer um conjunto pequeno de presets para teste comparável
- incluir uma execução sem pré-processamento
- incluir apenas presets simples e reproduzíveis na rodada inicial

#### Detalhamento da etapa 3

Nesta fase, o objetivo não é encontrar o melhor pipeline de pré-processamento possível, mas verificar se transformações simples geram ganho real nas ferramentas avaliadas.

Ferramentas de suporte contempladas:

- `Pillow`
  - abertura, conversão e salvamento de imagens
  - conversão para grayscale
  - ajuste simples de contraste
  - suporte aos presets `basic`, `binarized` e `deskew_binarized`

- `OpenCV`
  - binarização com método `Otsu`
  - correção de inclinação (`deskew`)
  - operações futuras de denoising, bordas e contornos, se necessárias
  - suporte aos presets `binarized` e `deskew_binarized`

##### 3.1. Presets propostos para a rodada 1

- `none`
  - imagem original, sem alteração

- `basic`
  - conversão para grayscale com `Pillow`
  - ajuste simples de contraste com `Pillow` e fator inicial `1.5`

- `binarized`
  - grayscale com `Pillow`
  - threshold/binarização com `OpenCV` e método `Otsu`

- `deskew_binarized`
  - grayscale com `Pillow`
  - correção de inclinação com `OpenCV`
  - limite de correção de rotação entre `-15` e `15` graus
  - threshold/binarização com `OpenCV` e método `Otsu`

##### 3.2. Objetivo dos presets

- `none`
  - servir como referência base
  - medir o desempenho bruto de cada ferramenta

- `basic`
  - testar ganho leve sem agressividade no tratamento da imagem

- `binarized`
  - verificar se OCR melhora em documentos escaneados com texto mais apagado ou fundo irregular

- `deskew_binarized`
  - verificar ganho em casos com rotação ou desalinhamento visual

##### 3.3. Regras desta rodada

- aplicar os mesmos presets para todas as ferramentas sempre que tecnicamente viável
- evitar presets muito sofisticados nesta fase
- manter implementações reproduzíveis e fáceis de auditar
- registrar exatamente quais transformações compõem cada preset
- se a correção de inclinação não conseguir estimar o ângulo com segurança, manter a imagem sem rotação e registrar a observação

##### 3.4. Resultado esperado desta etapa

- conjunto pequeno e fechado de presets para a rodada 1
- descrição objetiva de cada preset
- base suficiente para observar se pré-processamento simples ajuda ou não

##### 3.5. Ordem de execução dos presets

A execução dos presets seguirá uma progressão do mais simples para o mais intrusivo:

1. `none`
2. `basic`
3. `binarized`
4. `deskew_binarized`

Aplicação prática:

- no `smoke test`, começar com `none` para validar OCR bruto
- depois validar os demais presets na mesma amostra reduzida
- no `benchmark inicial`, rodar a matriz completa de ferramentas e presets usando a mesma amostra

Objetivo desta ordem:

- detectar erros cedo com o menor número possível de variáveis
- evitar depurar OCR e pré-processamento ao mesmo tempo logo na primeira execução
- facilitar leitura comparativa do ganho incremental de cada preset

Status atual:

- presets implementados em `src/sherlock_holmes/preprocessing/presets.py`
- `none`, `basic`, `binarized` e `deskew_binarized` disponíveis no runner
- `basic` foi validado tecnicamente em smoke dev com `docTR` sem pesos pré-treinados
- os demais presets ainda não foram rodados no smoke completo

### 4. Padronizar a saída dos experimentos

- definir um formato único para armazenar os resultados de cada execução
- registrar texto extraído, tempo, status da execução e metadados do teste
- garantir comparabilidade entre ferramentas e configurações

#### Detalhamento da etapa 4

A saída dos experimentos deve ser padronizada desde a primeira rodada para permitir comparação entre ferramentas, presets e categorias sem retrabalho posterior.

##### 4.1. Princípios da saída

- uma execução deve gerar dados legíveis por humanos e por máquina
- o formato deve servir tanto para debug quanto para consolidação de métricas
- a estrutura precisa ser igual para todas as ferramentas, independentemente da implementação interna

##### 4.2. Estrutura mínima por execução

Cada execução por arquivo deve registrar, no mínimo:

- identificador da ferramenta
- identificador do preset de pré-processamento
- caminho do arquivo de entrada
- categoria do documento
- status da execução
- tempo de processamento
- texto extraído
- tamanho do texto extraído
- mensagem de erro, quando houver

Campos opcionais recomendados quando a ferramenta disponibilizar:

- número de palavras extraídas
- confiança média ou scores de confiança por trecho
- caminho para saída bruta da ferramenta
- caminho para saída estruturada, quando houver
- observações de pré-processamento ou fallback

##### 4.3. Formato recomendado

Para esta fase, a recomendação é usar `JSON` por documento e `CSV` de consolidação por rodada.

Uso sugerido:

- `JSON`
  - guardar o resultado bruto de cada documento processado
  - facilitar debug e auditoria

- `CSV`
  - consolidar métricas resumidas
  - facilitar comparação rápida e geração de relatórios

##### 4.4. Exemplo de campos no resultado por documento

```json
{
  "tool": "tesseract",
  "preset": "none",
  "category": "Form",
  "input_path": "data/raw/dataset/Form/img_001.jpg",
  "status": "success",
  "elapsed_seconds": 0.82,
  "text": "texto extraido do documento",
  "text_length": 1284,
  "word_count": 214,
  "confidence_avg": null,
  "raw_output_path": "data/processed/ocr/tesseract/none/Form/img_001.raw.json",
  "structured_output_path": null,
  "error": null
}
```

##### 4.5. Exemplo de campos para consolidação

O arquivo consolidado por rodada pode conter colunas como:

- `tool`
- `preset`
- `category`
- `total_documents`
- `success_count`
- `error_count`
- `avg_elapsed_seconds`
- `avg_text_length`

##### 4.6. Organização sugerida dos artefatos

Nesta fase, os resultados podem ser organizados em `data/processed` com uma convenção simples, por exemplo:

- `data/processed/ocr/<tool>/<preset>/...`
- `data/processed/benchmark/<run_id>/summary.csv`

Como `data/processed` está ignorado pelo Git, estes arquivos são considerados artefatos locais de execução.

Artefatos pequenos e importantes para auditoria devem ser salvos em `documentation/reports`, por exemplo:

- resumo consolidado da rodada
- decisão técnica
- configuração de ambiente
- referência aos manifests das amostras usadas

Artefatos de apoio para inspeção visual devem ser mantidos em `notebooks`, por exemplo:

- `notebooks/ocr-result-review.ipynb`

##### 4.7. Resultado esperado desta etapa

- formato de saída único definido
- campos mínimos obrigatórios registrados
- convenção inicial de armazenamento documentada

Status atual:

- runner criado em `scripts/run_ocr_smoke.py`
- adapters OCR criados em `src/sherlock_holmes/ocr/extractors.py`
- saída por documento salva como `JSON`
- resumo por execução salvo como `summary.csv`
- resultados locais salvos em `data/processed/ocr/<run_id>/<tool>/<preset>/...`
- imagens pré-processadas locais salvas em `data/interim/ocr/<run_id>/<preset>/...`
- `data/processed`, `data/interim`, `.venv` e `.cache` estão ignorados no Git
- `.local` também está ignorado no Git para armazenar downloads locais, como o instalador do Tesseract
- notebook de revisão visual criado em `notebooks/ocr-result-review.ipynb`
- `ipykernel` adicionado em `requirements-ocr.txt` para executar o notebook no ambiente `.venv`
- kernel Jupyter `sherlock-holmes` registrado apontando para `.venv/Scripts/python.exe`
- notebook ajustado para revisar por padrão apenas os runs canônicos do smoke dev, evitando misturar tentativas intermediárias de setup/cache com os resultados válidos

##### 4.8. Como avaliar o sucesso de cada run

A avaliação de cada execução deve considerar três níveis complementares:

1. Sucesso técnico
- a execução terminou sem erro
- houve saída estruturada no formato esperado
- o tempo de execução ficou em faixa aceitável

2. Sucesso de extração
- o texto retornado não está vazio ou quase vazio
- o conteúdo parece coerente com a imagem processada
- a ordem de leitura permanece minimamente compreensível

3. Sucesso para o projeto
- a saída parece utilizável para fases posteriores
- o texto preserva informação suficiente para classificação futura
- o texto preserva informação suficiente para extração posterior de campos

##### 4.9. Avaliação prática por documento

Além dos campos automáticos, uma amostra reduzida dos resultados deve passar por revisão qualitativa manual com notas de `1` a `5` para:

- `legibilidade`
- `completude`
- `ordem_de_leitura`
- `utilidade_para_proxima_fase`

Essa revisão manual não precisa ser feita em todos os documentos do benchmark, mas deve cobrir exemplos de todas as categorias.

Para a rodada 1, a proposta inicial é revisar manualmente:

- `5 documentos por categoria`
- total estimado: `50 documentos`
- priorizar os resultados das combinações finalistas após análise quantitativa inicial

As notas manuais devem ser registradas em artefato próprio, por exemplo:

- `documentation/reports/ocr-run-001-manual-review.csv`

##### 4.10. Notebook de revisão visual

Antes do smoke test completo e do benchmark inicial, os resultados já gerados devem ser inspecionados em notebook para validar a utilidade real do texto extraído.

O notebook deve permitir:

- visualizar a imagem original
- visualizar a imagem pré-processada quando houver preset diferente de `none`
- ler o texto extraído no campo `text` dos arquivos `JSON`
- comparar ferramentas diferentes no mesmo documento
- comparar métricas técnicas como `status`, `elapsed_seconds`, `text_length` e `word_count`
- registrar avaliação humana simples, por exemplo `good`, `partial`, `bad` ou `failed`

Artefato criado:

- `notebooks/ocr-result-review.ipynb`

Objetivo desta inclusão:

- evitar aprovar uma ferramenta apenas porque ela gerou texto
- verificar se o texto extraído parece útil para leitura humana e fases futuras do projeto
- transformar a validação do smoke test em uma avaliação técnica e qualitativa

### 5. Rodar o smoke test

- executar as ferramentas em uma amostra pequena
- identificar erros de instalação, compatibilidade ou performance
- ajustar o setup antes do benchmark principal

#### Detalhamento da etapa 5

O `smoke test` será a primeira validação operacional do ambiente e das ferramentas selecionadas.

##### 5.1. Objetivo

- confirmar que as ferramentas escolhidas executam corretamente no ambiente do projeto
- validar o fluxo básico de entrada, processamento e saída
- detectar falhas antes do benchmark inicial

##### 5.2. Escopo do smoke test

- usar a amostra reduzida definida na etapa 1
- processar `3 imagens por categoria`
- total estimado: `30 imagens`

##### 5.3. Ordem de execução

Primeira rodada:
- `Tesseract + none`
- `PaddleOCR + none`
- `docTR + none`

Segunda rodada:
- repetir a mesma amostra com os demais presets
- ordem: `basic`, `binarized`, `deskew_binarized`

##### 5.4. O que verificar no smoke test

- instalação e inicialização das ferramentas
- leitura correta dos arquivos `.jpg`
- geração dos arquivos de saída no formato padronizado
- tempo de execução em faixa razoável
- presença de texto extraído em quantidade minimamente útil
- inspeção visual no notebook para verificar se o texto parece útil
- ausência de falhas recorrentes por categoria

##### 5.5. Critérios para aprovação no smoke test

Uma combinação de ferramenta e preset é considerada apta para o benchmark inicial quando:

- executa sem falha sistemática
- gera saída estruturada para a maior parte da amostra
- produz texto minimamente utilizável
- tem resultados revisados no notebook antes de avançar para benchmark
- não apresenta tempo de execução inviável para a rodada seguinte

##### 5.6. Possíveis saídas desta etapa

- combinação aprovada sem ajuste
- combinação aprovada com observações
- combinação reprovada temporariamente por erro técnico
- combinação adiada para rodada posterior

##### 5.7. Artefatos esperados desta etapa

- resultados brutos do smoke test
- revisão visual dos resultados no notebook
- registro das combinações aprovadas e reprovadas
- notas curtas sobre problemas encontrados e ajustes necessários

Status atual:

- smoke completo de `30` imagens ainda não foi executado
- smoke dev de `1` imagem foi executado para validar instalação e fluxo
- `Tesseract + none` teve sucesso real em `1` imagem após instalação, com `text_length=1606`
- `docTR + none` teve sucesso real em `1` imagem, com `text_length=1502`
- `PaddleOCR + none` teve sucesso real em `1` imagem usando `PP-OCRv4`, com `text_length=1109`
- antes da instalação, `Tesseract + none` gerou erro esperado por ausência do executável `tesseract`
- `docTR` exige `DOCTR_MULTIPROCESSING_DISABLE=TRUE` neste ambiente para evitar erro de permissão no `ThreadPool`
- caches de modelos foram direcionados para `.cache/`
- relatório do smoke dev registrado em `documentation/reports/ocr-run-001-smoke-dev.md`
- notebook de visualização criado em `notebooks/ocr-result-review.ipynb` para inspecionar imagem, saída OCR e métricas lado a lado
- resultados canônicos do smoke dev revisados no notebook:
  - `Tesseract + none`: `success_rate=1.0`, `errors=0`, `elapsed_seconds=2.460369`, `text_length=1606`, `word_count=261`
  - `docTR + none`: `success_rate=1.0`, `errors=0`, `elapsed_seconds=20.469273`, `text_length=1502`, `word_count=239`
  - `PaddleOCR + none`: `success_rate=1.0`, `errors=0`, `elapsed_seconds=51.659296`, `text_length=1109`, `word_count=159`
- interpretação preliminar do smoke dev:
  - as três combinações estão tecnicamente aptas para avançar para o smoke completo com preset `none`
  - `Tesseract + none` apresentou melhor sinal quantitativo inicial, com menor tempo e maior volume de texto
  - `docTR + none` apresentou volume de texto próximo ao Tesseract, mas com tempo maior
  - `PaddleOCR + none` executou com sucesso usando `PP-OCRv4`, mas foi mais lento e extraiu menos texto nesta imagem
  - a revisão qualitativa inicial não reprova nenhuma das três combinações, mas ainda não substitui avaliação em amostra maior
- próximo passo operacional: rodar smoke completo de `30` imagens para `Tesseract + none`, `docTR + none` e `PaddleOCR + none`

### 6. Rodar o benchmark inicial

- executar todas as combinações escolhidas de ferramenta e preset
- usar a mesma amostra para todas as execuções
- salvar os resultados brutos em arquivos auditáveis
- salvar resumos e decisões em arquivos versionáveis dentro de `documentation/reports`

#### Detalhamento da etapa 6

O benchmark inicial será a primeira comparação estruturada entre as ferramentas e presets aprovados no `smoke test`.

##### 6.1. Objetivo

- comparar ferramentas em uma amostra maior e equilibrada
- observar impacto dos presets de pré-processamento
- gerar dados suficientes para uma primeira decisão técnica

##### 6.2. Escopo do benchmark inicial

- usar a amostra definida na etapa 1 para benchmark
- processar `20 imagens por categoria`
- total estimado: `200 imagens`

##### 6.3. Combinações a executar

Executar somente:

- ferramentas aprovadas no `smoke test`
- presets aprovados no `smoke test`

Princípio:

- nenhuma combinação deve entrar no benchmark inicial sem ter passado antes pela validação técnica mínima

##### 6.4. Regra de comparabilidade

- todas as ferramentas devem rodar sobre exatamente a mesma amostra
- todos os presets devem usar exatamente a mesma amostra
- os resultados devem ser salvos com identificação clara de ferramenta, preset e categoria

##### 6.5. Ordem sugerida de execução

1. rodar todas as ferramentas com `none`
2. rodar todas as ferramentas com `basic`
3. rodar todas as ferramentas com `binarized`
4. rodar todas as ferramentas com `deskew_binarized`

Objetivo da ordem:

- manter leitura incremental do impacto do pré-processamento
- facilitar depuração se surgir erro em algum preset específico

##### 6.6. O que registrar durante o benchmark

- status de cada execução
- tempo por documento
- texto extraído por documento
- tamanho do texto extraído
- erros por combinação
- observações relevantes de execução, quando necessário

##### 6.7. Resultado esperado desta etapa

- conjunto completo de resultados comparáveis da rodada 1
- base consolidada para análise quantitativa e qualitativa
- insumos suficientes para iniciar recomendação de ferramenta principal e fallback

##### 6.8. Critérios de parada durante o benchmark

Uma combinação de ferramenta e preset pode ser interrompida antes do fim do benchmark se apresentar sinais claros de inviabilidade.

Critérios sugeridos:

- falha técnica recorrente em mais de `30%` das primeiras execuções
- tempo médio muito acima das demais combinações sem ganho qualitativo aparente
- saída vazia ou quase vazia em grande parte da amostra inicial
- erro sistemático em uma categoria inteira

Quando isso ocorrer, a interrupção deve ser registrada no relatório da rodada com:

- ferramenta
- preset
- motivo da interrupção
- quantidade de documentos processados antes da parada

### 7. Avaliar os resultados

- comparar tempo de execução, taxa de sucesso e volume de texto extraído
- revisar qualitativamente uma amostra dos textos gerados
- observar diferenças por categoria de documento

#### Detalhamento da etapa 7

A avaliação dos resultados deve combinar leitura quantitativa e qualitativa. O objetivo não é identificar apenas qual ferramenta extrai mais texto, mas qual gera a melhor saída para os próximos passos do projeto.

##### 7.1. Avaliação quantitativa

Comparar, por ferramenta, preset e categoria:

- `success_count`
- `error_count`
- `success_rate`
- `avg_elapsed_seconds`
- `avg_text_length`

Objetivo:

- identificar combinações estáveis e rápidas
- detectar combinações com falhas recorrentes
- observar padrões de desempenho entre categorias

##### 7.2. Avaliação qualitativa

Selecionar uma amostra reduzida dos resultados para leitura manual e atribuição de notas de `1` a `5` em:

- `legibilidade`
- `completude`
- `ordem_de_leitura`
- `utilidade_para_proxima_fase`

Objetivo:

- verificar se o texto extraído faz sentido
- detectar ruído excessivo, truncamento ou desorganização
- observar se a saída é útil para classificação e extração futura

Escala sugerida:

- `1`: inutilizável
- `2`: muito ruim, com pouco conteúdo aproveitável
- `3`: parcialmente utilizável
- `4`: bom, com pequenos problemas
- `5`: muito bom para a próxima fase

##### 7.3. Análise por categoria

A leitura dos resultados deve considerar que categorias diferentes exigem comportamentos diferentes do OCR.

Exemplos:

- `Form`
  - observar preservação de campos e estrutura

- `Scientific`
  - observar blocos densos, títulos e possível ruído estrutural

- `Email`, `Letter`, `Memo`
  - observar fluxo de leitura em texto corrido

- `News` e `ADVE`
  - observar possíveis problemas com layout mais visual ou múltiplos blocos

##### 7.4. Interpretação dos resultados

Princípios para leitura:

- mais texto não significa automaticamente melhor OCR
- menor tempo não significa automaticamente melhor ferramenta
- uma ferramenta pode ser globalmente melhor ou melhor apenas para algumas categorias
- presets agressivos podem melhorar certas classes e piorar outras

##### 7.5. Resultado esperado desta etapa

- visão comparativa clara entre ferramentas e presets
- identificação de pontos fortes e fracos por categoria
- base suficiente para consolidar uma decisão técnica inicial

### 8. Consolidar a decisão

- recomendar uma ferramenta principal
- recomendar uma opção alternativa ou fallback
- registrar limitações, riscos e próximos testes necessários

#### Detalhamento da etapa 8

Ao final da rodada 1, os resultados devem ser convertidos em uma decisão prática para o projeto.

##### 8.1. Objetivo

- selecionar uma estratégia inicial de OCR para continuar o desenvolvimento
- registrar claramente o racional da decisão
- definir se a rodada 1 foi suficiente ou se será necessário ampliar o benchmark

##### 8.2. Decisões esperadas

- escolha de uma ferramenta principal
- escolha de uma ferramenta alternativa ou fallback
- indicação de qual preset parece mais promissor por padrão inicial

##### 8.3. Perguntas que a etapa deve responder

- qual ferramenta apresentou melhor equilíbrio entre estabilidade, qualidade e tempo
- qual ferramenta parece mais útil para as próximas fases do Sherlock Holmes
- qual preset trouxe ganho real sem aumentar complexidade excessiva
- há diferença importante de desempenho entre categorias

##### 8.4. Quando a rodada 1 pode ser considerada suficiente

- existe uma ferramenta claramente superior ou mais adequada
- existe pelo menos uma alternativa viável
- os resultados são consistentes o bastante para seguir para a próxima fase

##### 8.5. Quando abrir uma rodada 2

Uma nova rodada deve ser considerada se ocorrer um ou mais dos cenários abaixo:

- nenhuma ferramenta apresenta desempenho satisfatório
- os resultados ficam muito próximos e sem vencedor claro
- há falhas recorrentes em categorias importantes
- os melhores resultados ainda não parecem suficientes para classificação ou extração futura
- o custo operacional da melhor ferramenta é inviável

##### 8.6. Possíveis expansões da rodada 2

- incluir alternativas locais como `EasyOCR`
- revisar presets de pré-processamento
- ampliar a amostra
- iniciar testes com PDFs reais para aproximar o pipeline do cenário final
- avaliar ferramentas de PDF, layout e Markdown estruturado, como `OCRmyPDF`, `Docling`, `SmolDocling`, `pymupdf4llm`, `marker-pdf`, `unstructured` e `MinerU`
- avaliar ferramentas cloud ou comerciais, como `Amazon Textract`, `Azure AI Document Intelligence`, `Google Cloud Vision`, `ABBYY`, `Nanonets OCR` e `Rossum.AI`, se custo e privacidade forem aceitáveis
- abrir uma rodada experimental com modelos multimodais, como `DeepSeek-OCR`, `Dots.OCR`, `OLMo-OCR 2`, `Qwen3-VL`, `Donut` ou `TrOCR`, somente após validação de hardware, licença e formato de saída

##### 8.7. Artefato final desta etapa

- relatório de decisão em `documentation/reports`
- recomendação explícita de ferramenta principal, fallback e próximos passos

## Entregáveis

Ao final desta fase, os seguintes artefatos devem estar disponíveis:

- amostra de teste definida e documentada
- configuração das ferramentas da rodada 1 registrada
- definição dos presets de pré-processamento utilizada nos testes
- resultados brutos das execuções salvos em formato estruturado
- resumo comparativo das métricas por ferramenta e por categoria
- avaliação qualitativa inicial dos resultados
- recomendação da estratégia inicial de OCR para a próxima fase
- relatório final desta rodada em `documentation/reports`
