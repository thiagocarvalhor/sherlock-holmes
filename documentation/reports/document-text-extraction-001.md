# Relatorio: Identificacao de Tipo e Extracao Textual Direta

## Objetivo

Registrar a entrega inicial da camada de identificacao de tipo de arquivo e extracao textual direta, conforme `documentation/plans/document-text-extraction-execution-plan.md`.

## Alteracoes Realizadas

Foram criados:

- `src/sherlock_holmes/documents/__init__.py`
- `src/sherlock_holmes/documents/inspection.py`

## Funcoes Criadas

- `detect_document_type`
- `extract_text_direct`

Dataclasses:

- `DocumentInspection`
- `DirectTextExtraction`

## Comportamento Implementado

A camada consegue:

- detectar PDF por assinatura `%PDF`;
- detectar ZIP por assinatura `PK`;
- identificar texto simples;
- gerar inventario textual de ZIP;
- extrair texto direto de PDF com `pypdfium2`;
- retornar `no_text` quando PDF nao tiver camada textual;
- retornar `unsupported` ou `unsupported_container` sem acionar OCR.

## Validacoes Executadas

### Compilacao

Comando:

```powershell
.venv\Scripts\python.exe -m compileall src\sherlock_holmes\documents
```

Resultado:

- sucesso.

### Identificacao de ZIP PNCP

Arquivo:

```text
data/raw/pncp/documents/pncp-download-smoke-pdf-ext/001_91084705902152024000.zip
```

Resultado:

```text
DocumentInspection(... file_type='zip', extension='.zip', size_bytes=1040085, detection_method='signature')
```

Extracao direta:

```text
status=unsupported_container
```

Inventario gerado:

```text
ZIP entries:
- PE 902152024.zip (977643 bytes)
- RelacaoItens91084705902152024000.pdf (65456 bytes)
```

### Extracao Textual Direta de PDF

PDF extraido localmente para smoke:

```text
data/interim/pncp/text-extraction-smoke/RelacaoItens91084705902152024000.pdf
```

Resultado:

- tipo detectado: `pdf`;
- metodo: `signature`;
- status: `success`;
- paginas: `5`;
- texto extraido nas duas primeiras paginas: `5514` caracteres.

Trecho inicial extraido:

```text
91081 - FURNAS-CENTRAIS ELETRICAS S.A.
910847 - ELETRONUCLEAR S.A
RELACAO DE ITENS - PREGAO ELETRONICO...
```

## Conclusao

A camada inicial de identificacao e extracao textual direta foi implementada com sucesso.

O teste confirmou que um documento oficial baixado do PNCP pode ser:

```text
ZIP
    |
    v
PDF interno
    |
    v
texto extraido diretamente
```

Isso valida a diretriz de nao acionar OCR antes de tentar extracao textual direta.

## Proximos Passos

1. Criar suporte controlado para extrair arquivos internos de ZIP.
2. Criar convencao para resultados de texto extraido em `data/processed`.
3. Integrar essa camada ao fluxo de documentos PNCP.
4. Acionar OCR apenas quando `extract_text_direct` retornar `no_text` ou tipo de imagem/escaneado.
