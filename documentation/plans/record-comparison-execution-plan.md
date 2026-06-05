# Plano de Execucao: Comparacao de Registros Completos

## Objetivo

Comparar um registro manual completo contra um candidato PNCP completo, agregando
as comparacoes campo a campo em um resultado unico com score global e gerando
artefatos auditaveis (JSON e CSV).

## Contexto

A camada `compare_field_values` ja compara um campo por vez com vinculo de
evidencia. O que falta e a funcao que itera sobre os campos relevantes de um par
(manual, PNCP), produz a lista de `FieldComparison` e retorna um `RecordComparison`
com score agregado e status geral.

A validacao desta entrega sera aplicada sobre a linha `67` da planilha manual
(municipio Belford Roxo, CNPJ 39485438000142) contra os 10 candidatos retornados
pela API PNCP em `data/raw/pncp/pncp-refactor-live-row67/contracts/source_row_67.json`.

## Mapeamento de Campos

| Campo manual       | Campo PNCP                     | Tipo       |
|--------------------|-------------------------------|------------|
| cnpj               | orgaoEntidade.cnpj            | cnpj       |
| municipio          | unidadeOrgao.municipioNome    | text       |
| uf                 | unidadeOrgao.ufSigla          | text       |
| objeto_contrato    | objetoContrato                | text       |
| numero_contrato    | numeroContratoEmpenho         | text       |
| valor_contrato     | valorGlobal                   | number     |
| vigencia_inicio    | dataVigenciaInicio            | date       |
| vigencia_fim       | dataVigenciaFim               | date       |

## Escopo

### Inclui

- dataclass `RecordComparison` com lista de `FieldComparison`, score medio e status geral;
- funcao `compare_records` em `comparison.py`;
- mapeamento fixo dos campos acima;
- script `scripts/compare_row67.py` que carrega dado real e executa a comparacao;
- saida em JSON e CSV em `data/processed/comparison/row67/`;
- atualizacao de `__init__.py` para exportar os novos simbolos.

### Nao inclui

- pesos diferenciados por campo;
- paginacao PNCP adicional (usa apenas os 10 candidatos ja salvos);
- interface Streamlit;
- LLM;
- revisao humana.

## Status Geral de RecordComparison

```text
match          - todos os campos comparaveis retornaram match
partial_match  - maioria dos campos com match ou partial_match, sem divergencias criticas
divergent      - um ou mais campos criticos (valor, numero_contrato) sao divergent
inconclusive   - muitos campos faltando nos dois lados
```

Campos criticos para determinar `divergent`: `valor_contrato` e `numero_contrato`.

## Arquivos a Criar ou Ajustar

```text
src/sherlock_holmes/validation/comparison.py   (adicionar RecordComparison e compare_records)
src/sherlock_holmes/validation/__init__.py     (exportar novos simbolos)
scripts/compare_row67.py                       (script operacional)
```

## Status

Concluida.

## Resultado da Entrega

Arquivos criados:

- `src/sherlock_holmes/validation/comparison.py` — adicionados `RecordComparison` e `compare_records`
- `scripts/compare_row67.py`

Arquivos atualizados:

- `src/sherlock_holmes/validation/__init__.py`

Validacoes executadas:

- compilacao com `compileall`;
- execucao sobre linha 67 (10 candidatos PNCP reais);
- geracao de `data/processed/comparison/row67/record_comparison.json` e `.csv`.

Relatorio:

- `documentation/reports/record-comparison-001.md`

## Proximo Passo

Paginar a busca PNCP para cobrir as paginas 2 e 3 da linha 67 e localizar
o contrato de limpeza urbana (02/SEMSEP/2025/2025).

## Criterio de Conclusao

- `compare_records` compilar sem erros;
- script executar sobre linha 67 sem excecao;
- gerar `data/processed/comparison/row67/record_comparison.json`;
- gerar `data/processed/comparison/row67/record_comparison.csv`;
- JSON conter lista de comparacoes campo a campo com evidencias vinculadas;
- CSV conter uma linha por campo com colunas: `field_name`, `manual_value`,
  `official_value`, `status`, `similarity_score`, `notes`;
- relatorio registrado em `documentation/reports/record-comparison-001.md`.
