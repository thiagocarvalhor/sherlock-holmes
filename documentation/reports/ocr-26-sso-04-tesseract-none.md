# OCR do contrato 26/SSO/04 com Tesseract

## Contexto

Execucao de OCR sobre o contrato escaneado:

```text
data/raw/dataset/26-SSO-04 - Contrato de Concessao - Agrupamento Sudeste.pdf
```

O contrato foi convertido previamente em 63 imagens PNG:

```text
data/interim/ocr/pncp-contract-26-sso-04/pages/page-001.png
...
data/interim/ocr/pncp-contract-26-sso-04/pages/page-063.png
```

O manifesto usado na execucao foi:

```text
documentation/plans/ocr-26-sso-04-pages.csv
```

## Comando OCR

```powershell
.venv\Scripts\python.exe scripts\run_ocr_manifest.py --tool tesseract --preset none --manifest documentation\plans\ocr-26-sso-04-pages.csv --run-id ocr-26-sso-04-tesseract-none
```

## Resultado

- ferramenta: `tesseract`
- preset: `none`
- paginas processadas: `63`
- paginas com sucesso: `63`
- paginas vazias: `0`
- tempo total registrado no summary: `96.825s`
- media de caracteres por pagina: `2081.2`
- menor pagina em volume de texto: `page-063.png`, com `922` caracteres
- maior pagina em volume de texto: `page-054.png`, com `2729` caracteres

Artefatos gerados:

```text
data/processed/ocr/ocr-26-sso-04-tesseract-none/tesseract/none/summary.csv
data/processed/ocr/ocr-26-sso-04-tesseract-none/tesseract/none/Contract/page-001.json
...
data/processed/ocr/ocr-26-sso-04-tesseract-none/tesseract/none/Contract/page-063.json
```

## Texto consolidado

Os JSONs por pagina foram consolidados em um unico TXT com separadores de pagina:

```powershell
.venv\Scripts\python.exe scripts\collect_ocr_text.py --input-dir data\processed\ocr\ocr-26-sso-04-tesseract-none\tesseract\none\Contract --output data\processed\ocr-text\ocr-26-sso-04-tesseract-none.txt --title "Contrato 26/SSO/04 - OCR Tesseract" --page-separators
```

Saida:

```text
data/processed/ocr-text/ocr-26-sso-04-tesseract-none.txt
```

Tamanho do arquivo consolidado: `138174` bytes.

## Campos identificados inicialmente

Na primeira pagina do OCR aparecem os seguintes campos:

- contrato: `26/SSO/04`
- processo administrativo: `0262004-0.235.349-4`
- licitacao: `Concorrencia n. 019/SSO/03`
- objeto: execucao dos servicos divisiveis de limpeza urbana, Agrupamento Sudeste
- contratante: Prefeitura do Municipio de Sao Paulo / AMLURB / Secretaria de Servicos e Obras
- CNPJ encontrado para a contratante: `46.392.163/0001-68`
- contratada: `ECOURBIS AMBIENTAL S/A`
- origem societaria indicada no contrato: `Consorcio Bandeirantes II`

Tambem foram localizados no texto consolidado:

- clausula 4: valor do contrato
- valor OCR lido: `R$ 5.039.480.640,00`
- clausula 5: prazo do contrato e condicoes de prorrogacao
- prazo OCR lido: `240` meses
- inicio da execucao OCR lido: `13 de outubro de 2004`, a partir das `06:00`
- fim estimado do prazo original: `13/10/2024`
- a clausula 5 permite prorrogacao por igual ou menor periodo

## Relacao com exemplo_1.xlsx

A linha correspondente em `documentation/source/exemplo_1.xlsx`, aba `CONSOLIDADO`,
associa:

- municipio: `Sao Paulo`
- empresa: `Ecourbis Ambiental S.A.`
- revisao empresas: `Vital Engenharia Ambiental / Marquise Ambiental / SA Paulista`
- CNPJ: `07.037.123/0001-46`
- contrato: `026/SSO/2004`

No OCR do contrato, os nomes `Vital Engenharia Ambiental` e `Marquise Ambiental`
nao apareceram literalmente na busca inicial. O texto do contrato associa a Ecourbis
ao `Consorcio Bandeirantes II`, indicando que a coluna `REVISÃO EMPRESAS` da
planilha provavelmente e um enriquecimento/manual de normalizacao, nao um campo
literal do contrato.

## Leitura sobre vigencia e prorrogacao

A clausula 5 informa que o prazo original do contrato e de `240` meses, contados
do inicio da execucao dos servicos, previsto para `13 de outubro de 2004` as
`06:00`.

Assim, o ciclo original estimado e:

```text
13/10/2004 + 240 meses = 13/10/2024
```

A mesma clausula preve que a prorrogacao pode ser efetuada por igual ou menor
periodo, desde que cumpridas condicoes como manifestacao de interesse,
justificativa de interesse publico, estudo de viabilidade economico-financeira,
pagamento de renovacao de outorga e novos condicionamentos/metas.

Essa regra ajuda a explicar a vigencia registrada no `exemplo_1.xlsx`:

```text
inicio: 12/10/2024
fim: 12/10/2044
```

Interpretacao atual:

- o PDF OCR analisado e o contrato-base de 2004
- o contrato-base ja previa possibilidade de prorrogacao por ate novo periodo de
  240 meses
- a planilha parece registrar o ciclo prorrogado/consolidado, nao apenas a
  vigencia original do contrato-base
- o termo aditivo/subrogacao deve ser analisado para confirmar formalmente a
  prorrogacao 2024-2044

## Proximo passo

- extrair campos estruturados do TXT consolidado
- comparar campos extraidos com a linha do `exemplo_1.xlsx`
- identificar quais campos podem vir da API PNCP e quais dependem do documento OCR
- executar OCR no termo aditivo/subrogacao da Ecourbis e comparar com a clausula 5
