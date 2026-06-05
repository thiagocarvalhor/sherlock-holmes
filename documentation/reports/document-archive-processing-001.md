# Relatorio: Processamento Controlado de Arquivos ZIP

## Objetivo

Registrar a entrega inicial para listar e extrair arquivos internos de ZIPs baixados do PNCP, salvando resultados de extracao textual direta em JSON.

## Alteracoes Realizadas

Arquivos atualizados:

- `src/sherlock_holmes/documents/inspection.py`
- `src/sherlock_holmes/documents/__init__.py`

Plano criado:

- `documentation/plans/document-archive-processing-execution-plan.md`

## Funcoes Criadas

- `list_zip_members`
- `extract_zip_members`
- `write_text_extraction_result`

Dataclasses:

- `ZipMember`
- `ExtractedZipMember`

## Validacao Executada

Arquivo ZIP usado:

```text
data/raw/pncp/documents/pncp-download-smoke-pdf-ext/001_91084705902152024000.zip
```

Membros listados:

```text
PE 902152024.zip
RelacaoItens91084705902152024000.pdf
```

Extracao controlada:

```text
data/interim/pncp/documents/archive-smoke/RelacaoItens91084705902152024000.pdf
```

Extracao textual direta:

- status: `success`;
- texto extraido: `5514` caracteres nas duas primeiras paginas;
- resultado salvo em:

```text
data/processed/pncp/documents/archive-smoke/relacao-itens-text.json
```

## Cuidados Implementados

- ZIP nao e extraido automaticamente;
- membros com caminho absoluto ou `..` sao rejeitados;
- e possivel filtrar por extensao permitida;
- OCR nao e acionado;
- resultados locais ficam em `data/interim` e `data/processed`, ambos ignorados pelo Git.

## Conclusao

O projeto agora consegue lidar com o caso real observado no PNCP:

```text
arquivo oficial baixado
    |
    v
ZIP
    |
    v
PDF interno
    |
    v
texto direto extraido
    |
    v
JSON auditavel em data/processed
```

Isso confirma mais uma vez que OCR deve ser fallback, nao primeira opcao.

## Proximos Passos

1. Integrar esse fluxo em um script operacional.
2. Criar uma convencao de `run_id` para processamento documental.
3. Preparar criterios para quando acionar OCR.
