# Dados e artefatos

O projeto separa dados brutos, intermediários e processados.

```text
data/raw/         dados coletados ou baixados
data/interim/     artefatos intermediários
data/processed/   resultados prontos para auditoria ou consumo
```

Esses diretórios são ignorados pelo Git.

## Exemplos

Contratos PNCP coletados:

```text
data/raw/pncp/
```

Documentos baixados:

```text
data/raw/pncp/documents/
```

Texto extraído de documentos:

```text
data/processed/pncp/documents/
```

Comparações:

```text
data/processed/comparison/
```

Relatórios:

```text
data/processed/reports/
```

## Regra

Artefatos gerados localmente devem ser reproduzíveis por scripts ou pela UI. O Git deve versionar código, configuração, documentação e amostras pequenas, não saídas grandes de execução.
