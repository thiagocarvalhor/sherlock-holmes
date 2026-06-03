# Conversao de PDFs para imagens OCR

## Contexto

Foi adicionado um script reutilizavel para preparar PDFs escaneados antes da
execucao do fluxo de OCR existente.

O objetivo e manter a execucao de OCR orientada por manifesto. A nova etapa
converte PDFs em imagens e gera um manifesto compativel com o runner oficial
`scripts/run_ocr_manifest.py`.

## Script

- `scripts/convert_pdf_to_ocr_images.py`
- `scripts/run_ocr_manifest.py`
- `scripts/collect_ocr_text.py`
- `src/sherlock_holmes/ocr/manifest_runner.py`

## Dependencia direta registrada

- `pypdfium2==5.7.1`

## Comando para o contrato 26-SSO-04

```powershell
.venv\Scripts\python.exe scripts\convert_pdf_to_ocr_images.py --slug 26-sso-04
```

Esse comando usa como PDF padrao:

```text
data/raw/dataset/26-SSO-04 - Contrato de Concessao - Agrupamento Sudeste.pdf
```

Saidas esperadas:

```text
data/interim/ocr/pdf-pages/26-sso-04/page-001.jpg
data/interim/ocr/pdf-pages/26-sso-04/page-002.jpg
...
documentation/plans/ocr-26-sso-04-pages.csv
```

## Proximo passo OCR

Depois da conversao, executar o runner oficial de manifesto:

```powershell
.venv\Scripts\python.exe scripts\run_ocr_manifest.py --tool tesseract --preset none --manifest documentation\plans\ocr-26-sso-04-pages.csv --run-id ocr-26-sso-04-tesseract-none
```

Depois da execucao do OCR, consolidar os JSONs por pagina em um arquivo texto:

```powershell
.venv\Scripts\python.exe scripts\collect_ocr_text.py --input-dir data\processed\ocr\ocr-26-sso-04-tesseract-none\tesseract\none\Contract --output data\processed\ocr-text\ocr-26-sso-04-tesseract-none.txt --title "Contrato 26/SSO/04 - OCR Tesseract" --page-separators
```

## Validacao executada

- `scripts/convert_pdf_to_ocr_images.py` validado com `py_compile`
- `scripts/run_ocr_manifest.py` validado com `py_compile`
- `scripts/collect_ocr_text.py` validado com `py_compile`
- conversao de teste executada para a pagina 1 do contrato `26-SSO-04`
- imagem de teste gerada em `data/interim/ocr/pdf-pages/26-sso-04-validation/page-001.jpg`
- manifesto de teste gerado em `data/interim/ocr/26-sso-04-validation-manifest.csv`
- consolidacao de texto executada para o run `ocr-26-sso-04-tesseract-none`
- texto consolidado gerado em `data/processed/ocr-text/ocr-26-sso-04-tesseract-none.txt`
