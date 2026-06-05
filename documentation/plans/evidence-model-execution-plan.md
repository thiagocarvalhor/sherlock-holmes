# Plano de Execucao: Modelo Inicial de Evidencia e Confianca

## Objetivo

Criar um modelo inicial para registrar evidencias usadas pelo Sherlock Holmes.

O objetivo e permitir que cada informacao relevante consiga responder:

```text
de onde veio?
como foi obtida?
qual e a confianca?
qual URL ou arquivo sustenta isso?
quando foi coletada?
```

## Contexto

O projeto ja possui:

- consultas PNCP;
- referencias de documentos oficiais;
- download controlado;
- extracao textual direta;
- avaliacao de qualidade;
- decisao de fallback OCR.

Agora falta uma estrutura comum para registrar essas fontes como evidencias auditaveis.

## Escopo

### Inclui

- criar pacote `sherlock_holmes.validation`;
- criar dataclass `EvidenceRecord`;
- definir tipos de origem;
- definir niveis de confianca;
- criar helpers para evidencias vindas de:
  - API oficial;
  - referencia documental;
  - texto extraido;
- salvar evidencias em JSON.

### Nao inclui

- matching completo;
- comparacao campo a campo;
- banco de dados;
- interface Streamlit;
- LLM;
- OCR real.

## Arquivos a Criar

```text
src/sherlock_holmes/validation/__init__.py
src/sherlock_holmes/validation/evidence.py
```

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

## Criterios de Sucesso

- criar evidencia de resposta PNCP;
- criar evidencia de referencia documental;
- criar evidencia de texto extraido;
- salvar lista de evidencias em JSON;
- manter metadados suficientes para auditoria futura.

## Status

Concluida.

## Resultado da Entrega

Arquivos criados:

- `src/sherlock_holmes/validation/__init__.py`
- `src/sherlock_holmes/validation/evidence.py`

Validacoes executadas:

- compilacao com `compileall`;
- smoke local com evidencia de API, documento e texto extraido;
- escrita de JSON em `data/processed/pncp/evidence/evidence-model-smoke.json`.

Relatorio:

- `documentation/reports/evidence-model-001.md`

## Proximo Passo

Criar helpers para evidencias vindas de planilha manual e iniciar comparacao campo a campo.
