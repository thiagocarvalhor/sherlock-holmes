# Smoke Dev OCR 001

## Objetivo

Validar o caminho operacional mínimo antes do smoke test completo de 30 imagens.

## Comandos Validados

- `python scripts/run_ocr_smoke.py --tool tesseract --preset none --limit 1`
- `python scripts/run_ocr_smoke.py --tool doctr --preset basic --limit 1 --no-doctr-pretrained`
- `python scripts/run_ocr_smoke.py --tool doctr --preset none --limit 1`
- `python scripts/run_ocr_smoke.py --tool paddleocr --preset none --limit 1`

## Resultados

| Ferramenta | Preset | Escopo | Status | Observação |
| --- | --- | ---: | --- | --- |
| `tesseract` | `none` | 1 imagem | erro esperado | executável `tesseract` não encontrado no `PATH` |
| `tesseract` | `none` | 1 imagem | sucesso real | após instalação do Tesseract; `text_length=1606` |
| `docTR` | `basic` | 1 imagem | sucesso técnico | modo sem pesos, usado apenas para validar pipeline e cache |
| `docTR` | `none` | 1 imagem | sucesso real | pesos baixados para `.cache/doctr`; `text_length=1502` |
| `PaddleOCR` | `none` | 1 imagem | erro com default | `PP-OCRv5` falhou com erro oneDNN/MKLDNN no Windows |
| `PaddleOCR` | `none` | 1 imagem | sucesso real | usando `PP-OCRv4`; modelos em `.cache/paddlex`; `text_length=1109` |

## Ajustes Aplicados

- caches de modelos apontados para `.cache/`
- `.cache/` ignorado no Git
- `DOCTR_MULTIPROCESSING_DISABLE=TRUE` para evitar erro de permissão em `ThreadPool` no Windows
- `PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT=False` para reduzir risco de erro nativo no Paddle
- `PaddleOCR` configurado com `ocr_version="PP-OCRv4"` por estabilidade nesta máquina
- `docTR` configurado para desligar `pretrained_backbone` quando o modo `--no-doctr-pretrained` for usado
- `Tesseract` configurado no adapter para buscar `C:\Program Files\Tesseract-OCR\tesseract.exe` quando não estiver no `PATH`

## Pendências

- instalar idioma `por` no Tesseract apenas se a rodada exigir português
- rodar o smoke test completo com 30 imagens para `Tesseract + none`
- rodar o smoke test completo com 30 imagens para `docTR + none`
- rodar o smoke test completo com 30 imagens para `PaddleOCR + none`
- depois repetir os presets `basic`, `binarized` e `deskew_binarized` nas ferramentas aprovadas
