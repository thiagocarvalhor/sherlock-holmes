# Arquitetura

## Direcao

A arquitetura do Sherlock Holmes segue esta regra:

```text
Regra principal no centro.
Ferramentas nas bordas.
```

O objetivo da reestruturacao e separar o que pertence ao dominio do que pertence a integracoes externas, interfaces, scripts e detalhes de infraestrutura.

## Estrutura atual

Hoje o pacote esta organizado principalmente por trilhas tecnicas:

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

Essa estrutura ajudou a evoluir rapido, mas agora comeca a misturar responsabilidades. Por exemplo, `validation` concentra regra central, enquanto `pncp` e `enrichment` sao integracoes externas.

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
- evidencia;
- comparacao;
- campo comparado;
- status de revisao;
- CNPJ;
- identificador PNCP.

### Application

Casos de uso:

- investigar linha manual;
- comparar linha manual com contrato oficial;
- gerar relatorio auditavel;
- preparar revisao operacional;
- consolidar relatorios.

### Adapters

Bordas do sistema:

- Streamlit;
- scripts CLI;
- PNCP;
- BrasilAPI;
- filesystem;
- OCR.

### Infrastructure

Detalhes tecnicos compartilhados:

- configuracao;
- logging;
- paths;
- bootstrap de execucao.

## Plano de migracao

A migracao deve ser incremental. O plano detalhado esta em:

```text
documentation/plans/repository-architecture-restructure-execution-plan.md
```

As fases principais sao:

1. criar documentacao automatica;
2. criar esqueleto arquitetural;
3. mover dominio central;
4. mover casos de uso;
5. introduzir ports;
6. mover adapters externos;
7. organizar Streamlit e CLI;
8. reorganizar testes;
9. remover pontes antigas.
