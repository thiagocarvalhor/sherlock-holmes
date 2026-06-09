# Dados e artefatos

O projeto separa dados brutos, intermediarios e processados.

```text
data/raw/         dados coletados ou baixados
data/interim/     artefatos intermediarios
data/processed/   resultados prontos para auditoria ou consumo
```

Esses diretorios sao ignorados pelo Git.

## Exemplos

Contratos PNCP coletados:

```text
data/raw/pncp/
```

Documentos baixados:

```text
data/raw/pncp/documents/
```

Texto extraido de documentos:

```text
data/processed/pncp/documents/
```

Comparacoes:

```text
data/processed/comparison/
```

Relatorios:

```text
data/processed/reports/
```

## Regra

Artefatos gerados localmente devem ser reproduziveis por scripts ou pela UI. O Git deve versionar codigo, configuracao, documentacao e amostras pequenas, nao saidas grandes de execucao.
