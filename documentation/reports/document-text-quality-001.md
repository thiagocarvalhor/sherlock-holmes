# Relatorio: Normalizacao e Qualidade do Texto Extraido

## Objetivo

Registrar a entrega da camada inicial de normalizacao e qualidade de texto extraido diretamente.

## Alteracoes Realizadas

Foi criado:

- `src/sherlock_holmes/documents/text_quality.py`

Foram atualizados:

- `src/sherlock_holmes/documents/__init__.py`
- `src/sherlock_holmes/documents/inspection.py`

Plano criado:

- `documentation/plans/document-text-quality-execution-plan.md`

## Funcoes Criadas

- `normalize_extracted_text`
- `assess_text_quality`

Dataclass:

- `TextQuality`

## Integracao

A funcao `write_text_extraction_result` agora salva tambem:

- `normalized_text`;
- bloco `quality`;
- `word_count`;
- `line_count`;
- `mojibake_marker_count`;
- `should_consider_ocr`;
- notas de qualidade.

## Validacao Executada

Comando:

```powershell
.venv\Scripts\python.exe scripts\process_document_text.py --input data\raw\pncp\documents\pncp-download-smoke-pdf-ext\001_91084705902152024000.zip --run-id document-quality-smoke --max-pages 2
```

Resultado:

```text
run_id=document-quality-smoke
file_type=zip
text_outputs=1
```

Qualidade registrada no JSON:

```text
quality=good
text_length=5412
word_count=719
line_count=104
mojibake_marker_count=4
should_consider_ocr=false
```

Interpretacao:

- o texto extraido diretamente e utilizavel;
- OCR nao deve ser acionado para este documento;
- os artefatos de encoding observados no terminal eram em parte efeito de exibicao do PowerShell, nao necessariamente do JSON salvo.

## Conclusao

O pipeline documental agora consegue:

```text
baixar documento controladamente
    |
    v
identificar ZIP/PDF
    |
    v
extrair PDF interno
    |
    v
extrair texto direto
    |
    v
normalizar texto
    |
    v
avaliar qualidade e decidir se OCR deve ser considerado
```

## Proximos Passos

1. Definir criterios formais de fallback para OCR.
2. Integrar esse status ao futuro fluxo de evidencia.
3. Criar relatorio consolidado por documento processado.
