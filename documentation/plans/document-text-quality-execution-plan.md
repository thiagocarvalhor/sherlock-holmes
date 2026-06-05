# Plano de Execucao: Normalizacao e Qualidade do Texto Extraido

## Objetivo

Criar uma camada inicial para normalizar texto extraido diretamente de documentos e gerar sinais simples de qualidade.

Essa etapa prepara a decisao operacional:

```text
texto direto serve
ou
precisa de OCR / revisao
```

## Escopo

### Inclui

- normalizar quebras de linha e espacos;
- remover caracteres de controle;
- calcular metricas simples do texto;
- classificar qualidade inicial como `good`, `partial`, `poor` ou `empty`;
- indicar se OCR deve ser considerado;
- integrar a normalizacao ao script `process_document_text.py`.

### Nao inclui

- corrigir todos os problemas de encoding;
- LLM;
- OCR;
- parse semantico de campos;
- classificacao final de documento.

## Arquivos a Criar ou Ajustar

```text
src/sherlock_holmes/documents/text_quality.py
src/sherlock_holmes/documents/__init__.py
scripts/process_document_text.py
```

## Criterios de Sucesso

- texto extraido passa por normalizacao simples;
- JSON de saida inclui metricas de qualidade;
- textos vazios ou muito curtos indicam `should_consider_ocr=true`;
- texto extraido do PDF de smoke fica classificado como utilizavel.

## Status

Concluida.

## Resultado da Entrega

Arquivo criado:

- `src/sherlock_holmes/documents/text_quality.py`

Arquivos atualizados:

- `src/sherlock_holmes/documents/__init__.py`
- `src/sherlock_holmes/documents/inspection.py`

Validacoes executadas:

- compilacao com `compileall`;
- reprocessamento do ZIP PNCP com `scripts/process_document_text.py`;
- geracao de `normalized_text` e bloco `quality`;
- classificacao do PDF de smoke como `good`, sem necessidade de OCR.

Relatorio:

- `documentation/reports/document-text-quality-001.md`

## Proximo Passo

Definir criterios formais de fallback para OCR e integrar esse status ao futuro fluxo de evidencia.
