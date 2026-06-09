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
