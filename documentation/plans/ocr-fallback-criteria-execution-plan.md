# Plano de Execucao: Criterios de Fallback Para OCR

## Objetivo

Definir criterios formais para decidir quando OCR deve ser considerado no pipeline documental do Sherlock Holmes.

Essa etapa transforma a regra estrategica em comportamento operacional:

```text
OCR apenas quando necessario.
```

## Contexto

O projeto ja possui:

- download controlado de documentos PNCP;
- identificacao de tipo real de arquivo;
- extracao textual direta;
- processamento controlado de ZIP;
- normalizacao e metricas de qualidade do texto extraido.

Agora falta padronizar a decisao:

```text
texto direto suficiente
ou
considerar OCR
ou
revisao humana antes de decidir
```

## Escopo

### Inclui

- criar funcao de decisao de fallback OCR;
- usar `DirectTextExtraction` e `TextQuality`;
- retornar status operacional;
- explicar o motivo da decisao;
- nao executar OCR automaticamente.

### Nao inclui

- rodar OCR;
- escolher ferramenta OCR;
- converter PDF em imagem;
- integrar com Streamlit;
- matching/comparacao.

## Arquivos a Criar ou Ajustar

```text
src/sherlock_holmes/documents/ocr_fallback.py
src/sherlock_holmes/documents/__init__.py
```

## Status Esperados

```text
direct_text_ok
consider_ocr
manual_review
unsupported
```

## Regras Iniciais

- `success` + qualidade `good`: `direct_text_ok`
- `success` + qualidade `partial`: `manual_review`
- `no_text`: `consider_ocr`
- `empty` ou `poor`: `consider_ocr`
- `unsupported_container`: `manual_review`
- `unsupported`: `manual_review`

## Validacao Local

Usar o JSON/texto ja gerado pelo smoke documental e confirmar que o PDF de exemplo fica como:

```text
direct_text_ok
```

## Status

Concluida.

## Resultado da Entrega

Arquivo criado:

- `src/sherlock_holmes/documents/ocr_fallback.py`

Arquivos atualizados:

- `src/sherlock_holmes/documents/__init__.py`
- `src/sherlock_holmes/documents/inspection.py`

Validacoes executadas:

- compilacao com `compileall`;
- casos sinteticos para `direct_text_ok` e `consider_ocr`;
- reprocessamento do ZIP PNCP com `scripts/process_document_text.py`;
- geracao do bloco `ocr_fallback` no JSON de texto.

Relatorio:

- `documentation/reports/ocr-fallback-criteria-001.md`

## Proximo Passo

Integrar `ocr_fallback` ao futuro modelo de evidencia e ao fluxo de matching/comparacao.
