# Smoke Completo OCR 001 - Preset none

## Objetivo

Executar o smoke test completo de 30 imagens com o preset `none`, usando as tres ferramentas aprovadas no smoke dev:

- `tesseract`
- `doctr`
- `paddleocr`

Manifest usado:

- `documentation/plans/ocr-smoke-sample-v1.csv`

## Runs Executados

| Ferramenta | Preset | Run ID | Documentos | Status |
| --- | --- | --- | ---: | --- |
| `tesseract` | `none` | `ocr-smoke-001-tesseract-none` | 30 | sucesso tecnico |
| `doctr` | `none` | `ocr-smoke-001-doctr-none` | 30 | sucesso tecnico |
| `paddleocr` | `none` | `ocr-smoke-001-paddleocr-none` | 30 | sucesso tecnico |

## Resultado Quantitativo

| Ferramenta | Preset | Documentos | Sucessos | Erros | Textos vazios | Tempo medio (s) | Tempo total (s) | Texto medio |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `tesseract` | `none` | 30 | 30 | 0 | 1 | 1.303 | 39.099 | 1303.7 |
| `doctr` | `none` | 30 | 30 | 0 | 0 | 6.350 | 190.500 | 1345.5 |
| `paddleocr` | `none` | 30 | 30 | 0 | 0 | 32.133 | 963.997 | 1166.2 |

## Observacoes

- Todas as ferramentas concluiram as 30 imagens sem erro tecnico.
- `tesseract` foi a ferramenta mais rapida nesta rodada.
- `doctr` teve o maior `avg_text_length`, com tempo medio maior que o Tesseract.
- `paddleocr` executou com sucesso usando `PP-OCRv4`, mas teve o maior tempo medio.
- `tesseract` gerou texto vazio em `data/raw/dataset/ADVE/2050834062.jpg`; a mesma imagem gerou texto com `doctr` e `paddleocr`.
- A execucao de `doctr` emitiu um `FutureWarning` do `torch.load`; nao bloqueou a rodada.
- A execucao de `paddleocr` emitiu aviso sobre ausencia de `ccache`; nao bloqueou a rodada.
- O PowerShell continuou emitindo aviso de politica de execucao ao tentar carregar o perfil local; esse aviso nao bloqueou os comandos.
- A execucao gerou arquivos `__pycache__`; o `.gitignore` foi atualizado para ignorar `__pycache__/` e `*.py[cod]`.

## Artefatos Locais

Os resultados brutos foram salvos em:

- `data/processed/ocr/ocr-smoke-001-tesseract-none/tesseract/none/`
- `data/processed/ocr/ocr-smoke-001-doctr-none/doctr/none/`
- `data/processed/ocr/ocr-smoke-001-paddleocr-none/paddleocr/none/`

Cada run contem `summary.csv` e arquivos JSON por documento.

## Interpretacao Inicial

As tres combinacoes estao tecnicamente aptas para seguir para a revisao qualitativa no notebook.

Leitura preliminar:

- `tesseract + none` e a melhor combinacao inicial em velocidade.
- `doctr + none` e uma alternativa forte para qualidade/volume de texto, com custo maior de tempo.
- `paddleocr + none` permanece viavel tecnicamente, mas seu tempo de execucao precisa ser considerado antes do benchmark de 200 imagens.

## Proximo Passo

Revisar qualitativamente os resultados no notebook `notebooks/ocr-result-review.ipynb`, com atencao especial para:

- o caso vazio de `tesseract` em `ADVE/2050834062.jpg`
- comparacao de ordem de leitura entre `tesseract`, `doctr` e `paddleocr`
- decisao sobre repetir o smoke completo com os presets `basic`, `binarized` e `deskew_binarized`
