# Arquitetura

## Direção

A arquitetura do Sherlock Holmes segue esta regra:

```text
Regra principal no centro.
Ferramentas nas bordas.
```

O objetivo da reestruturação é separar o que pertence ao domínio do que pertence a integrações externas, interfaces, scripts e detalhes de infraestrutura.

## Estrutura atual

Hoje o pacote está organizado principalmente por trilhas técnicas:

```text
src/sherlock_holmes/
|-- pncp/
|-- enrichment/
|-- validation/
|-- documents/
|-- reporting/
|-- webapp/
|-- ocr/
`-- investigation.py
```

Essa estrutura ajudou a evoluir rápido, mas agora começa a misturar responsabilidades. Por exemplo, `validation` concentra regra central, enquanto `pncp` e `enrichment` são integrações externas.

## Estrutura de transição

A Fase 1 já criou os pacotes da arquitetura alvo sem mover regra de negócio. Nesta etapa, os módulos antigos continuam funcionando e os novos diretórios servem como destino explícito para as próximas migrações:

```text
src/sherlock_holmes/
|-- domain/
|-- application/
|-- adapters/
|-- infrastructure/
`-- shared/
```

Essa convivência é temporária. As próximas fases movem conceitos centrais, casos de uso e integrações externas em ondas pequenas, preservando wrappers quando necessário.

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

Os módulos antigos em `sherlock_holmes.validation` e `sherlock_holmes.pncp.ids` continuam existindo como wrappers de compatibilidade durante a transição. O Streamlit também mantém wrappers internos enquanto a borda visual ainda não foi movida para `adapters/inbound/streamlit`.

A Fase 3 iniciou a migração de casos de uso. A investigação de uma linha manual contra candidatos PNCP foi movida para:

```text
src/sherlock_holmes/application/use_cases/investigate_manual_row.py
```

A geração de relatórios auditáveis foi movida para:

```text
src/sherlock_holmes/application/use_cases/build_audit_report.py
```

Os módulos antigos `sherlock_holmes.investigation` e `sherlock_holmes.reporting` continuam como wrappers de compatibilidade.

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
