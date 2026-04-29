# Critério de Amostragem: OCR Fase 1

## Objetivo

Definir amostras pequenas, reproduzíveis e equilibradas por categoria para a validação inicial de OCR do projeto Sherlock Holmes.

## Dataset de origem

As amostras são geradas a partir de `data/raw/dataset`.

Categorias contempladas:

- `ADVE`
- `Email`
- `Form`
- `Letter`
- `Memo`
- `News`
- `Note`
- `Report`
- `Resume`
- `Scientific`

## Arquivos elegíveis

Nesta rodada, apenas arquivos `.jpg` são elegíveis.

Arquivos auxiliares do sistema operacional, como `Thumbs.db`, devem ser ignorados.

## Estratégia de seleção

A seleção é estratificada por categoria.

Para cada categoria:

- o `smoke test` usa `3` imagens
- o `benchmark inicial` usa `20` imagens

A seleção é reproduzível e não manual. Os arquivos são ordenados por um hash `SHA-256` calculado a partir de:

- seed fixa: `sherlock-holmes-ocr-v1`
- caminho relativo do arquivo

Com isso, a amostra não depende da ordem retornada pelo sistema de arquivos.

## Relação entre amostras

A amostra de `smoke test` é um subconjunto da amostra de `benchmark inicial`.

Isso permite validar instalação e execução básica usando parte dos mesmos documentos que depois entrarão no benchmark completo.

## Artefatos gerados

- `documentation/plans/ocr-smoke-sample-v1.csv`
- `documentation/plans/ocr-benchmark-sample-v1.csv`

## Script gerador

Os manifests são gerados por:

```bash
python scripts/generate_ocr_sample_manifests.py
```
