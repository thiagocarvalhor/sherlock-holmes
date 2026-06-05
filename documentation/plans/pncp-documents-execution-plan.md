# Plano de Execucao: Camada PNCP de Arquivos e Documentos

## Objetivo

Criar uma camada inicial para tratar arquivos/anexos oficiais retornados pelo PNCP como referencias auditaveis, preparando o caminho para download controlado, extracao textual direta e OCR apenas quando necessario.

Esta etapa fortalece a diretriz:

```text
Documentos depois.
OCR apenas quando necessario.
Evidencia sempre.
```

## Contexto

As entregas anteriores adicionaram:

- camada inicial de contratos;
- camada inicial de licitacoes/compras;
- listagem de arquivos vinculados a contratos;
- listagem de arquivos vinculados a compras/licitacoes.

Agora e necessario padronizar como esses arquivos sao representados dentro do Sherlock Holmes.

## Escopo

### Inclui

- criar modulo `arquivos.py`;
- criar estrutura para referencia de documento;
- normalizar registros de arquivos retornados pelo PNCP;
- identificar titulo, tipo, URL, sequencial e contexto;
- criar referencias de documentos a partir de arquivos de contrato;
- criar referencias de documentos a partir de arquivos de licitacao;
- preparar metadados para futura evidencia.

### Nao inclui

- baixar arquivos automaticamente;
- extrair texto de PDF;
- rodar OCR;
- detectar se PDF tem camada textual;
- armazenar documentos em `data/raw`;
- criar interface Streamlit para documentos;
- comparar campos extraidos de documentos.

## Arquivos a Criar ou Ajustar

```text
src/sherlock_holmes/pncp/arquivos.py
src/sherlock_holmes/pncp/__init__.py
```

## Funcoes Prioritarias

```text
document_reference_from_pncp_file
document_references_from_pncp_files
contract_file_references
procurement_file_references
```

## Estrutura Esperada

Cada referencia de documento deve conter, quando disponivel:

```text
source
resource_type
resource_id
title
document_type
sequence
url
uri
published_at
raw
```

## Criterios de Sucesso

- `arquivos.py` criado;
- funcoes importaveis via `sherlock_holmes.pncp`;
- uma lista de arquivos PNCP pode ser convertida em referencias padronizadas;
- arquivos de contrato podem ser referenciados via `contract_file_references`;
- arquivos de licitacao podem ser referenciados via `procurement_file_references`;
- nenhuma chamada de download e executada automaticamente.

## Validacao Local

Sem rede:

```powershell
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -c "from sherlock_holmes.pncp import document_references_from_pncp_files; print(document_references_from_pncp_files([{'sequencialDocumento': 1, 'titulo': 'Contrato', 'tipoDocumentoNome': 'Contrato', 'url': 'https://example.test/doc.pdf'}], resource_type='contract', resource_id='demo')[0])"
```

Com rede, usando recurso ja validado:

```powershell
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -c "from sherlock_holmes.pncp import procurement_file_references; refs=procurement_file_references(numero_controle_pncp='23274194000119-1-000191/2024'); print(len(refs)); print(refs[0] if refs else '')"
```

## Status

Concluida.

## Resultado da Entrega

Arquivo criado:

- `src/sherlock_holmes/pncp/arquivos.py`

Arquivo atualizado:

- `src/sherlock_holmes/pncp/__init__.py`

Validacoes executadas:

- compilacao com `compileall`;
- conversao local de metadado simulado em `PncpDocumentReference`;
- chamada real para `procurement_file_references(numero_controle_pncp='23274194000119-1-000191/2024')`, retornando `1` referencia de edital.

Relatorio:

- `documentation/reports/pncp-documents-001.md`

## Proximo Passo

Criar plano para download controlado e armazenamento local de documentos oficiais, sem acionar OCR automaticamente.
