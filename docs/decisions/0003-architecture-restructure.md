# Decisao 0003: Reestruturacao Arquitetural

## Contexto

O repositorio cresceu rapidamente e acumulou modulos por trilha tecnica.

## Decisao

Migrar gradualmente para uma arquitetura em camadas:

```text
domain
application
adapters
infrastructure
```

## Consequencias

- dominio deve ficar livre de Streamlit, rede e filesystem;
- PNCP e BrasilAPI viram adapters externos;
- scripts e Streamlit viram adapters de entrada;
- casos de uso ficam em `application`;
- `docs/` passa a ser a documentacao publicada;
- `documentation/` continua como historico de planos e relatorios.

## Plano

O plano detalhado esta em:

```text
documentation/plans/repository-architecture-restructure-execution-plan.md
```
