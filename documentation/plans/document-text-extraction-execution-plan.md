# Plano de Execucao: Identificacao de Tipo e Extracao Textual Direta

## Objetivo

Criar uma camada inicial para identificar o tipo real de documentos baixados e tentar extrair texto diretamente antes de acionar OCR.

## Diretriz

```text
Download controlado.
Identificacao de tipo real.
Extracao textual direta quando possivel.
OCR apenas como fallback.
```

## Escopo

### Inclui

- criar pacote `sherlock_holmes.documents`;
- detectar tipo por assinatura de arquivo;
- reconhecer PDF, ZIP, texto e binario desconhecido;
- extrair texto de PDF com `pypdfium2`, quando houver camada textual;
- extrair texto de arquivos `.txt`;
- gerar inventario textual de arquivos ZIP;
- retornar metadados de extracao.

### Nao inclui

- OCR;
- extrair PDFs dentro de ZIP automaticamente;
- baixar documentos;
- parse semantico de campos;
- comparar texto extraido com planilha;
- interface Streamlit.

## Arquivos a Criar

```text
src/sherlock_holmes/documents/__init__.py
src/sherlock_holmes/documents/inspection.py
```

## Funcoes Prioritarias

```text
detect_document_type
extract_text_direct
```

## Criterios de Sucesso

- identificar corretamente o ZIP baixado do PNCP;
- gerar inventario dos arquivos internos do ZIP;
- identificar PDF por assinatura;
- extrair texto direto de PDF quando houver camada textual;
- nao acionar OCR automaticamente.

## Status

Concluida.

## Resultado da Entrega

Arquivos criados:

- `src/sherlock_holmes/documents/__init__.py`
- `src/sherlock_holmes/documents/inspection.py`

Validacoes executadas:

- compilacao com `compileall`;
- deteccao do ZIP baixado do PNCP;
- inventario textual do ZIP;
- extracao local do PDF interno para smoke;
- extracao textual direta do PDF com `pypdfium2`.

Relatorio:

- `documentation/reports/document-text-extraction-001.md`

## Proximo Passo

Criar suporte controlado para extrair arquivos internos de ZIP e salvar resultados textuais em `data/processed`.
