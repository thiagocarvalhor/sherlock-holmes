# Plano de Execucao: Download Controlado de Documentos PNCP

## Objetivo

Adicionar suporte inicial para baixar documentos oficiais referenciados pelo PNCP de forma explicita, auditavel e sem acionar OCR automaticamente.

Esta etapa parte da camada de referencias criada em `src/sherlock_holmes/pncp/arquivos.py`.

## Diretriz

```text
Referencia primeiro.
Download apenas quando solicitado.
Extracao textual antes de OCR.
OCR apenas quando necessario.
```

## Escopo

### Inclui

- criar funcao de download para `PncpDocumentReference`;
- salvar arquivo em diretorio informado pelo chamador;
- gerar nome de arquivo seguro;
- preservar URL, caminho local, content type, tamanho e timestamp;
- retornar metadados do download;
- manter download fora do fluxo automatico de busca.

### Nao inclui

- OCR;
- extracao textual de PDF;
- deteccao de PDF escaneado;
- banco de dados;
- download em lote;
- retry avancado;
- alteracao de Streamlit.

## Arquivos a Ajustar

```text
src/sherlock_holmes/pncp/arquivos.py
src/sherlock_holmes/pncp/__init__.py
```

## Funcoes Prioritarias

```text
safe_document_filename
download_document_reference
```

## Estrutura Esperada do Resultado

```text
source
resource_type
resource_id
url
local_path
content_type
bytes_written
downloaded_at
reference
```

## Convencao de Armazenamento

O chamador deve informar o diretorio raiz. Para execucoes reais, usar preferencialmente:

```text
data/raw/pncp/documents/<run_id>/
```

Esses arquivos ficam ignorados pelo Git.

## Validacao Local

Sem rede:

```powershell
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -c "from sherlock_holmes.pncp import safe_document_filename; print(safe_document_filename('Edital 01/2025', sequence=1, default_extension='.pdf'))"
```

Com rede, usando referencia real ja validada:

```powershell
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -c "from pathlib import Path; from sherlock_holmes.pncp import procurement_file_references, download_document_reference; ref=procurement_file_references(numero_controle_pncp='23274194000119-1-000191/2024')[0]; result=download_document_reference(ref, output_dir=Path('data/raw/pncp/documents/pncp-download-smoke')); print(result.local_path); print(result.bytes_written); print(result.content_type)"
```

## Status

Concluida.

## Resultado da Entrega

Arquivos atualizados:

- `src/sherlock_holmes/pncp/arquivos.py`
- `src/sherlock_holmes/pncp/__init__.py`

Validacoes executadas:

- compilacao com `compileall`;
- geracao de nome seguro;
- download real controlado de documento PNCP;
- inferencia de extensao por assinatura do conteudo.

Relatorio:

- `documentation/reports/pncp-document-download-001.md`

## Proximo Passo

Criar camada de identificacao de tipo de arquivo e extracao textual direta antes de OCR.
