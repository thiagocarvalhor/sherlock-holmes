# Plano de Execucao: Comparacao Campo a Campo Inicial

## Objetivo

Criar uma camada inicial para comparar valores manuais com valores oficiais, preservando evidencias dos dois lados.

## Escopo

### Inclui

- criar evidencia de planilha manual;
- comparar valores simples;
- normalizar texto, CNPJ, datas e numeros;
- gerar status de comparacao;
- vincular evidencias manual e oficial.

### Nao inclui

- matching completo de candidatos;
- pesos complexos;
- interface;
- LLM;
- revisao humana.

## Arquivos a Criar ou Ajustar

```text
src/sherlock_holmes/validation/evidence.py
src/sherlock_holmes/validation/comparison.py
src/sherlock_holmes/validation/__init__.py
```

## Status Esperados

```text
match
partial_match
divergent
missing_in_manual
missing_in_official
unresolved
```

## Status

Concluida.

## Resultado da Entrega

Arquivos criados:

- `src/sherlock_holmes/validation/comparison.py`
- `documentation/reports/field-comparison-001.md`

Arquivos atualizados:

- `src/sherlock_holmes/validation/evidence.py`
- `src/sherlock_holmes/validation/__init__.py`

Validacoes executadas:

- compilacao com `compileall`;
- comparacao de valor;
- comparacao de CNPJ com e sem mascara.

Relatorio:

- `documentation/reports/field-comparison-001.md`

## Proximo Passo

Criar comparacao de registros completos e aplicar sobre a linha `67`.
