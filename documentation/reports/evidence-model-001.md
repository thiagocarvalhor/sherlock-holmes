# Relatorio: Modelo Inicial de Evidencia e Confianca

## Objetivo

Registrar a primeira entrega do modelo de evidencia e confianca do Sherlock Holmes.

## Alteracoes Realizadas

Foram criados:

- `src/sherlock_holmes/validation/__init__.py`
- `src/sherlock_holmes/validation/evidence.py`

Plano criado:

- `documentation/plans/evidence-model-execution-plan.md`

## Estruturas Criadas

Dataclass:

- `EvidenceRecord`

Constantes:

- `SOURCE_TYPES`
- `CONFIDENCE_LEVELS`

Helpers:

- `evidence_from_official_api`
- `evidence_from_document_reference`
- `evidence_from_extracted_text`
- `write_evidence_records`

## Tipos de Origem

```text
official_api
official_document
manual_spreadsheet
ocr_extracted
llm_extracted
human_reviewed
unresolved
```

## Niveis de Confianca

```text
high
medium
low
reviewed
unknown
```

## Validacao Executada

Comando:

```powershell
.venv\Scripts\python.exe -m compileall src\sherlock_holmes\validation
```

Resultado:

- sucesso.

Tambem foi criado um smoke local com tres evidencias:

- evidencia de API oficial;
- evidencia de referencia documental;
- evidencia de texto extraido.

Arquivo local gerado:

```text
data/processed/pncp/evidence/evidence-model-smoke.json
```

Esse arquivo fica ignorado pelo Git.

## Exemplo de Registro

```text
EvidenceRecord(
  evidence_id='api-1',
  source_type='official_api',
  confidence_level='high',
  method='pncp_search',
  source_url='https://example.test/api',
  field_name='numeroControlePNCP',
  value='demo'
)
```

## Conclusao

O projeto agora possui uma estrutura inicial para representar evidencias auditaveis.

Essa camada sera usada para conectar:

```text
PNCP API
documento oficial
texto extraido
decisao de OCR
comparacao manual vs oficial
```

## Proximos Passos

1. Criar helpers para evidencias vindas de planilha manual.
2. Criar camada inicial de comparacao campo a campo.
3. Ligar `ocr_fallback` e qualidade textual aos metadados de evidencia.
