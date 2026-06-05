# Relatorio: Download Controlado de Documentos PNCP

## Objetivo

Registrar a entrega inicial de download controlado de documentos PNCP, conforme `documentation/plans/pncp-document-download-execution-plan.md`.

## Alteracoes Realizadas

Foi atualizado:

- `src/sherlock_holmes/pncp/arquivos.py`
- `src/sherlock_holmes/pncp/__init__.py`

## Funcoes Criadas

- `safe_document_filename`
- `download_document_reference`

Tambem foi criada a dataclass:

- `PncpDownloadedDocument`

## Comportamento Implementado

O download:

- acontece apenas quando `download_document_reference` e chamada explicitamente;
- usa uma `PncpDocumentReference`;
- grava o arquivo no diretorio informado pelo chamador;
- retorna metadados com caminho local, URL, content type, bytes gravados e timestamp;
- nao aciona extracao textual;
- nao aciona OCR.

## Validacoes Executadas

### Compilacao

Comando:

```powershell
.venv\Scripts\python.exe -m compileall src\sherlock_holmes\pncp
```

Resultado:

- sucesso.

### Nome Seguro

Comando:

```powershell
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -c "from sherlock_holmes.pncp import safe_document_filename; print(safe_document_filename('Edital 01/2025', sequence=1, default_extension='.pdf'))"
```

Resultado:

```text
001_Edital_01_2025.pdf
```

### Download Real Controlado

Recurso usado:

```text
23274194000119-1-000191/2024
```

Fluxo:

```text
procurement_file_references
download_document_reference
```

Resultado final:

- caminho local: `data/raw/pncp/documents/pncp-download-smoke-pdf-ext/001_91084705902152024000.zip`
- bytes gravados: `1040085`
- content type informado pelo PNCP: `application/octet-stream`
- extensao inferida por assinatura do conteudo: `.zip`

Observacao:

- o PNCP retornou `application/octet-stream`;
- a inferencia por assinatura identificou o arquivo como ZIP;
- esse comportamento reforca a necessidade de detectar tipo real antes de decidir entre extracao textual e OCR.

## Conclusao

A camada de download controlado foi implementada.

O projeto agora consegue partir de uma referencia oficial do PNCP e materializar o documento localmente em `data/raw`, preservando metadados da operacao.

## Proximos Passos

1. Criar camada de identificacao de tipo de arquivo.
2. Implementar extracao textual direta para PDFs ou arquivos suportados.
3. Acionar OCR apenas quando o documento nao tiver texto extraivel ou for imagem/escaneado.
