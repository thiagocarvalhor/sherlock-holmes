# Relatorio: Comparacao Campo a Campo Inicial

## Objetivo

Registrar a primeira entrega da camada de comparacao campo a campo entre fonte manual e fonte oficial.

## Alteracoes Realizadas

Foram criados:

- `src/sherlock_holmes/validation/comparison.py`
- `documentation/plans/field-comparison-execution-plan.md`

Foram atualizados:

- `src/sherlock_holmes/validation/evidence.py`
- `src/sherlock_holmes/validation/__init__.py`

## Funcoes Criadas

- `evidence_from_manual_spreadsheet`
- `compare_field_values`

Dataclass:

- `FieldComparison`

## Status de Comparacao

```text
match
partial_match
divergent
missing_in_manual
missing_in_official
unresolved
```

## Validacao Executada

Comando:

```powershell
.venv\Scripts\python.exe -m compileall src\sherlock_holmes\validation
```

Resultado:

- sucesso.

Casos testados:

### Valor

Manual:

```text
52801942.27
```

Oficial:

```text
52801942.27
```

Resultado:

```text
status=match
similarity_score=1.0
```

### CNPJ

Manual:

```text
39.485.438/0001-42
```

Oficial:

```text
39485438000142
```

Resultado:

```text
status=match
similarity_score=1.0
```

## Conclusao

O Sherlock Holmes agora possui uma primeira camada para comparar valores manuais e oficiais com vinculo a evidencias dos dois lados.

Essa camada ainda e simples, mas ja estabelece a base para:

- comparacao campo a campo;
- relatorios de divergencia;
- matching mais explicavel;
- auditoria de cada valor comparado.

## Proximos Passos

1. Criar comparacao de registros completos.
2. Aplicar a comparacao sobre a linha `67` e o candidato PNCP top.
3. Gerar relatorio CSV/JSON de comparacao.
