# Relatorio: Criterios de Fallback Para OCR

## Objetivo

Registrar a entrega inicial dos criterios formais para decidir quando OCR deve ser considerado.

## Alteracoes Realizadas

Foi criado:

- `src/sherlock_holmes/documents/ocr_fallback.py`

Foram atualizados:

- `src/sherlock_holmes/documents/__init__.py`
- `src/sherlock_holmes/documents/inspection.py`

Plano criado:

- `documentation/plans/ocr-fallback-criteria-execution-plan.md`

## Funcoes Criadas

- `decide_ocr_fallback`

Dataclass:

- `OcrFallbackDecision`

## Status Operacionais

Foram definidos os status:

- `direct_text_ok`
- `consider_ocr`
- `manual_review`
- `unsupported`

## Regras Iniciais

- `success` + qualidade `good`: `direct_text_ok`
- `success` + qualidade `partial`: `manual_review`
- `no_text`: `consider_ocr`
- `empty` ou `poor`: `consider_ocr`
- `unsupported_container`: `manual_review`
- `unsupported`: `manual_review`

## Integracao

O JSON gerado por `write_text_extraction_result` agora inclui:

```text
ocr_fallback.status
ocr_fallback.should_run_ocr
ocr_fallback.reason
ocr_fallback.extraction_status
ocr_fallback.text_quality
```

## Validacoes Executadas

### Casos Sinteticos

Texto bom:

```text
status=direct_text_ok
should_run_ocr=false
```

PDF sem texto:

```text
status=consider_ocr
should_run_ocr=true
```

### Documento Real de Smoke

Comando:

```powershell
.venv\Scripts\python.exe scripts\process_document_text.py --input data\raw\pncp\documents\pncp-download-smoke-pdf-ext\001_91084705902152024000.zip --run-id document-ocr-fallback-smoke --max-pages 2
```

Resultado:

```text
quality=good
should_consider_ocr=false
ocr_fallback.status=direct_text_ok
ocr_fallback.should_run_ocr=false
```

## Conclusao

O projeto agora possui uma decisao operacional explicita para OCR.

No documento real testado, o texto direto foi considerado suficiente. OCR nao deve ser acionado.

## Proximos Passos

1. Integrar `ocr_fallback` ao futuro modelo de evidencia.
2. Criar camada de matching/comparacao usando texto direto quando disponivel.
3. Acionar runners OCR apenas para casos com `consider_ocr`.
