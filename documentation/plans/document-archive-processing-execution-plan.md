# Plano de Execucao: Processamento Controlado de Arquivos ZIP

## Objetivo

Adicionar suporte controlado para extrair arquivos internos de ZIPs baixados do PNCP e persistir resultados de extracao textual direta em `data/processed`.

## Diretriz

```text
ZIP nao e texto final.
Extrair membros de forma controlada.
Tentar texto direto.
OCR somente se necessario.
```

## Escopo

### Inclui

- listar membros de ZIP;
- extrair membros de ZIP para diretorio informado;
- evitar path traversal;
- processar arquivos extraidos com `extract_text_direct`;
- salvar resultado de extracao textual em JSON;
- manter tudo acionado explicitamente.

### Nao inclui

- download automatico;
- OCR;
- extracao recursiva profunda de ZIP dentro de ZIP;
- parse semantico de campos;
- interface Streamlit.

## Arquivos a Ajustar

```text
src/sherlock_holmes/documents/inspection.py
src/sherlock_holmes/documents/__init__.py
```

## Funcoes Prioritarias

```text
list_zip_members
extract_zip_members
write_text_extraction_result
```

## Convencoes

Arquivos extraidos:

```text
data/interim/pncp/documents/<run_id>/
```

Resultados de texto:

```text
data/processed/pncp/documents/<run_id>/
```

## Validacao Local

Usar o ZIP ja baixado em:

```text
data/raw/pncp/documents/pncp-download-smoke-pdf-ext/001_91084705902152024000.zip
```

Esperado:

- listar `PE 902152024.zip`;
- listar `RelacaoItens91084705902152024000.pdf`;
- extrair membros para `data/interim`;
- extrair texto direto do PDF;
- salvar JSON em `data/processed`.

## Status

Concluida.

## Resultado da Entrega

Arquivos atualizados:

- `src/sherlock_holmes/documents/inspection.py`
- `src/sherlock_holmes/documents/__init__.py`

Validacoes executadas:

- compilacao com `compileall`;
- listagem de membros do ZIP PNCP;
- extracao controlada do PDF interno;
- extracao textual direta do PDF;
- persistencia do resultado em JSON.

Relatorio:

- `documentation/reports/document-archive-processing-001.md`

## Proximo Passo

Integrar esse fluxo em um script operacional com `run_id`, entrada de documento e saidas padronizadas.
