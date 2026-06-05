# Plano de Execucao: Script Operacional de Processamento Documental

## Objetivo

Criar um script operacional para processar documentos locais ja baixados, identificar tipo real, extrair texto direto quando possivel e salvar resultados padronizados.

## Diretriz

```text
Entrada local.
Sem download.
Sem OCR automatico.
Saida auditavel em JSON.
```

## Escopo

### Inclui

- receber caminho de arquivo local;
- receber `run_id`;
- identificar tipo real do arquivo;
- processar PDF, texto simples e ZIP;
- extrair membros permitidos de ZIP para `data/interim`;
- extrair texto direto dos membros extraidos;
- salvar resultados em `data/processed`;
- imprimir resumo operacional no terminal.

### Nao inclui

- download de arquivos PNCP;
- OCR;
- parse semantico de campos;
- comparacao com planilha;
- interface Streamlit.

## Arquivo a Criar

```text
scripts/process_document_text.py
```

## Saidas Padronizadas

Inspecao:

```text
data/processed/pncp/documents/<run_id>/inspection.json
```

Resultado de texto:

```text
data/processed/pncp/documents/<run_id>/text/<nome>.json
```

Arquivos extraidos de ZIP:

```text
data/interim/pncp/documents/<run_id>/
```

## Validacao Local

Usar o ZIP ja baixado:

```powershell
.venv\Scripts\python.exe scripts\process_document_text.py --input data\raw\pncp\documents\pncp-download-smoke-pdf-ext\001_91084705902152024000.zip --run-id document-processing-smoke --max-pages 2
```

Resultado esperado:

- detectar ZIP;
- extrair PDF interno;
- extrair texto direto do PDF;
- salvar JSON em `data/processed`.

## Status

Concluida.

## Resultado da Entrega

Arquivo criado:

- `scripts/process_document_text.py`

Validacoes executadas:

- compilacao com `compileall`;
- processamento local do ZIP baixado do PNCP;
- extracao controlada de PDF interno;
- extracao textual direta do PDF;
- persistencia de artefatos em `data/processed`.

Relatorio:

- `documentation/reports/document-processing-script-001.md`

## Proximo Passo

Criar normalizacao/limpeza inicial do texto extraido e definir criterios para acionar OCR.
