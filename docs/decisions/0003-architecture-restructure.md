# Decisão 0003: Reestruturação Arquitetural

## Contexto

O repositório cresceu rapidamente e acumulou módulos por trilha técnica.

## Decisão

Migrar gradualmente para uma arquitetura em camadas:

```text
domain
application
adapters
infrastructure
```

## Consequências

- domínio deve ficar livre de Streamlit, rede e filesystem;
- PNCP e BrasilAPI viram adapters externos;
- scripts e Streamlit viram adapters de entrada;
- casos de uso ficam em `application`;
- `docs/` passa a ser a documentação publicada;
- `documentation/` continua como histórico de planos e relatórios.

## Plano

O plano detalhado está em:

```text
documentation/plans/repository-architecture-restructure-execution-plan.md
```
