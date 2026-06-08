# Relatorio: Documentos Oficiais em Relatorios Auditaveis - Entrega 001

## Objetivo

Registrar a inclusao de referencias de documentos oficiais PNCP nos relatorios auditaveis.

## Artefatos Criados

- `documentation/plans/audit-report-documents-execution-plan.md`

## Artefatos Atualizados

- `src/sherlock_holmes/reporting/audit.py`
- `src/sherlock_holmes/reporting/__init__.py`
- `scripts/generate_audit_report.py`
- `scripts/generate_audit_batch_report.py`
- `tests/test_audit_report.py`
- `documentation/projetos-similares/plano-execucao-roadmap-sherlock-holmes.md`

## Funcionalidades

- `load_document_references` carrega referencias documentais de JSON;
- `build_audit_report` aceita `official_documents`;
- o resumo unitario registra `official_documents_count`;
- o Markdown unitario inclui a secao `Documentos Oficiais Vinculados`;
- o relatorio consolidado soma `total_official_documents`;
- `scripts/generate_audit_report.py` aceita `--documents`;
- `scripts/generate_audit_batch_report.py` aceita `--documents-dir`.

## Formatos de Entrada

O carregador aceita:

- uma lista JSON de documentos;
- um objeto com `documents`;
- um objeto com `official_documents`;
- um objeto com `document_references`;
- um objeto unico com campos de documento.

Os campos normalizados no relatorio sao:

- `source`;
- `resource_type`;
- `resource_id`;
- `numero_controle_pncp`;
- `title`;
- `document_type`;
- `sequence`;
- `url`;
- `uri`;
- `published_at`;
- `local_path`.

## Validacoes Automatizadas

- `ruff check .` - passou.
- `pytest` - 60 testes passaram.

## Observacoes

Esta entrega nao faz chamada de rede. A busca PNCP, download e processamento documental continuam em camadas separadas; o relatorio apenas recebe referencias ja coletadas e as torna auditaveis.
