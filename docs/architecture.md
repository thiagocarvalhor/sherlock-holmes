# Arquitetura

## Direção

A arquitetura do Sherlock Holmes segue esta regra:

```text
Regra principal no centro.
Ferramentas nas bordas.
```

O objetivo da reestruturação é separar o que pertence ao domínio do que pertence a integrações externas, interfaces, scripts e detalhes de infraestrutura.

## Estrutura atual

Hoje o pacote está organizado por camadas:

```text
src/sherlock_holmes/
|-- domain/
|-- application/
|-- adapters/
|-- infrastructure/
`-- shared/
```

Os módulos legados por trilha técnica foram removidos na Fase 8. O código central fica em `domain` e `application`; integrações e entradas ficam em `adapters`.

## Estrutura consolidada

A migração criou e consolidou os pacotes da arquitetura alvo:

```text
src/sherlock_holmes/
|-- domain/
|-- application/
|-- adapters/
|-- infrastructure/
`-- shared/
```

Os comandos em `scripts/` continuam como wrappers operacionais finos para preservar a forma de execução local.

A Fase 2 já iniciou a migração do domínio central. A primeira fatia moveu os modelos e regras de comparação/evidência para:

```text
src/sherlock_holmes/domain/entities/comparison.py
src/sherlock_holmes/domain/entities/evidence.py
```

A segunda fatia moveu normalização de CNPJ e identificadores PNCP para:

```text
src/sherlock_holmes/domain/value_objects/cnpj.py
src/sherlock_holmes/domain/value_objects/pncp_id.py
```

A terceira fatia moveu a decisão de revisão operacional e indicação de OCR para:

```text
src/sherlock_holmes/domain/services/review.py
```

Os módulos antigos de validação foram removidos na Fase 8. O domínio passa a ser importado diretamente por `sherlock_holmes.domain`.

A Fase 3 iniciou a migração de casos de uso. A investigação de uma linha manual contra candidatos PNCP foi movida para:

```text
src/sherlock_holmes/application/use_cases/investigate_manual_row.py
```

A geração de relatórios auditáveis foi movida para:

```text
src/sherlock_holmes/application/use_cases/build_audit_report.py
```

A comparação direta de uma linha manual com um contrato oficial foi movida para:

```text
src/sherlock_holmes/application/use_cases/compare_manual_record.py
```

A preparação de revisão operacional foi movida para:

```text
src/sherlock_holmes/application/use_cases/prepare_review.py
```

Os wrappers antigos `sherlock_holmes.investigation` e `sherlock_holmes.reporting` foram removidos na Fase 8. Os fluxos devem importar casos de uso diretamente de `sherlock_holmes.application.use_cases`.

A Fase 4 iniciou a criação de ports da aplicação para dependências externas:

```text
src/sherlock_holmes/application/ports/pncp_contract_gateway.py
src/sherlock_holmes/application/ports/cnpj_enrichment_gateway.py
src/sherlock_holmes/application/ports/document_gateway.py
src/sherlock_holmes/application/ports/report_writer.py
src/sherlock_holmes/application/ports/review_status_store.py
```

Esses ports agora isolam os casos de uso das implementações concretas. PNCP, BrasilAPI, documentos, OCR e relatórios ficam em adapters outbound.

O enriquecimento CNPJ já passa pelo caso de uso:

```text
src/sherlock_holmes/application/use_cases/enrich_cnpj.py
```

Esse caso de uso depende do port `CnpjEnrichmentGateway`; a implementação concreta da BrasilAPI fica no adapter:

```text
src/sherlock_holmes/adapters/outbound/brasilapi/cnpj_gateway.py
```

O módulo antigo `sherlock_holmes.enrichment` foi removido na Fase 8. A integração BrasilAPI fica em `sherlock_holmes.adapters.outbound.brasilapi`.

A escrita de relatórios já pode usar o port `ReportWriter`, com adapter concreto em:

```text
src/sherlock_holmes/adapters/outbound/filesystem/report_writer.py
```

Os scripts de relatório usam esse adapter para gravar JSON e Markdown no filesystem.

A listagem de documentos oficiais de contratos já passa pelo port `DocumentGateway`, com adapter concreto em:

```text
src/sherlock_holmes/adapters/outbound/pncp/document_gateway.py
```

O helper Streamlit de PNCP chama `application.use_cases.list_contract_documents` para buscar arquivos oficiais.

A busca de contratos PNCP também passa pelo port `PncpContractGateway`, com caso de uso e adapter concreto em:

```text
src/sherlock_holmes/application/use_cases/search_pncp_contracts.py
src/sherlock_holmes/adapters/outbound/pncp/contract_gateway.py
```

O Streamlit usa esse caminho tanto na busca anual de contratos quanto na investigação automática de uma linha manual.

Na Fase 5, os clientes PNCP legados foram movidos para `adapters/outbound/pncp`:

```text
src/sherlock_holmes/adapters/outbound/pncp/client.py
src/sherlock_holmes/adapters/outbound/pncp/dates.py
src/sherlock_holmes/adapters/outbound/pncp/contratos.py
src/sherlock_holmes/adapters/outbound/pncp/licitacoes.py
src/sherlock_holmes/adapters/outbound/pncp/arquivos.py
```

Os módulos antigos em `sherlock_holmes.pncp` foram removidos na Fase 8. Clientes PNCP devem ser importados de `sherlock_holmes.adapters.outbound.pncp`; identificadores PNCP e CNPJ devem ser importados de `sherlock_holmes.domain.value_objects`.

Também na Fase 5, a inspeção/extração direta de documentos locais foi posicionada no adapter de filesystem:

```text
src/sherlock_holmes/adapters/outbound/filesystem/documents/
```

O OCR técnico usado em experimentos e manifestos foi posicionado em:

```text
src/sherlock_holmes/adapters/outbound/ocr/
```

Os pacotes antigos `sherlock_holmes.documents` e `sherlock_holmes.ocr` foram removidos na Fase 8.

Na Fase 6, as entradas do sistema foram posicionadas em `adapters/inbound`:

```text
src/sherlock_holmes/adapters/inbound/streamlit/
src/sherlock_holmes/adapters/inbound/cli/
```

O pacote antigo `sherlock_holmes.webapp` foi removido na Fase 8. Os arquivos em `scripts/` permanecem como wrappers finos para preservar comandos operacionais.

Na Fase 7, os testes passaram a acompanhar a arquitetura:

```text
tests/unit/domain/
tests/unit/application/
tests/integration/adapters/
tests/integration/streamlit/
```

## Arquitetura alvo

Estrutura planejada:

```text
src/sherlock_holmes/
|-- domain/
|   |-- entities/
|   |-- value_objects/
|   |-- services/
|   `-- exceptions/
|
|-- application/
|   |-- use_cases/
|   `-- ports/
|
|-- adapters/
|   |-- inbound/
|   |   |-- streamlit/
|   |   `-- cli/
|   |
|   `-- outbound/
|       |-- pncp/
|       |-- brasilapi/
|       |-- filesystem/
|       `-- ocr/
|
|-- infrastructure/
|   |-- config/
|   |-- logging/
|   `-- paths/
|
`-- shared/
```

## Papel das camadas

### Domain

Conceitos centrais:

- contrato;
- documento oficial;
- evidência;
- comparação;
- campo comparado;
- status de revisão;
- CNPJ;
- identificador PNCP.

### Application

Casos de uso:

- investigar linha manual;
- comparar linha manual com contrato oficial;
- gerar relatório auditável;
- preparar revisão operacional;
- consolidar relatórios.

### Adapters

Bordas do sistema:

- Streamlit;
- scripts CLI;
- PNCP;
- BrasilAPI;
- filesystem;
- OCR.

### Infrastructure

Detalhes técnicos compartilhados:

- configuração;
- logging;
- paths;
- bootstrap de execução.

## Plano de migração

A migração deve ser incremental. O plano detalhado está em:

```text
documentation/plans/repository-architecture-restructure-execution-plan.md
```

As fases principais são:

1. criar documentação automática;
2. criar esqueleto arquitetural;
3. mover domínio central;
4. mover casos de uso;
5. introduzir ports;
6. mover adapters externos;
7. organizar Streamlit e CLI;
8. reorganizar testes;
9. remover pontes antigas.
