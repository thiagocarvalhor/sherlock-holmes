# Relatorio: Comparacao de Registros Completos — Entrega 001

## Objetivo

Implementar a comparacao de registros completos entre um registro manual e um
candidato PNCP, gerando artefatos auditaveis (JSON e CSV).

## Artefatos Criados

- `src/sherlock_holmes/validation/comparison.py` — adicionados `RecordComparison`,
  `compare_records`, `RECORD_COMPARISON_STATUSES`, `_FIELD_MAPPING`, `_CRITICAL_FIELDS`
  e helper `_nested_get`
- `src/sherlock_holmes/validation/__init__.py` — exportados novos simbolos
- `scripts/compare_row67.py` — script operacional

## Artefatos Gerados na Validacao

- `data/processed/comparison/row67/record_comparison.json`
- `data/processed/comparison/row67/record_comparison.csv`

## Mapeamento de Campos

| Campo manual    | Campo PNCP                  | Tipo   |
|-----------------|-----------------------------|--------|
| cnpj            | orgaoEntidade.cnpj          | cnpj   |
| municipio       | unidadeOrgao.municipioNome  | text   |
| uf              | unidadeOrgao.ufSigla        | text   |
| objeto_contrato | objetoContrato              | text   |
| numero_contrato | numeroContratoEmpenho       | text   |
| valor_contrato  | valorGlobal                 | number |
| vigencia_inicio | dataVigenciaInicio          | date   |
| vigencia_fim    | dataVigenciaFim             | date   |

Campos criticos (acionam status `divergent`): `valor_contrato`, `numero_contrato`.

## Resultado da Validacao — Linha 67

Municipio: Belford Roxo / RJ  
CNPJ orgao: 39485438000142  
Manual: contrato 02/SEMSEP/2025/2025 — Limpeza Urbana — R$ 52.801.942,27

### Candidatos avaliados (pagina 1 — 10 de 22)

| numeroControlePNCP                 | score  | status    |
|------------------------------------|--------|-----------|
| 39485438000142-2-000012/2025       | 0.5000 | divergent |
| 39485438000142-2-000003/2025       | 0.3750 | divergent |
| 39485438000142-2-000004/2025       | 0.3750 | divergent |
| 39485438000142-2-000005/2025       | 0.3750 | divergent |
| 39485438000142-2-000006/2025       | 0.3750 | divergent |
| 39485438000142-2-000007/2025       | 0.3750 | divergent |
| 39485438000142-2-000008/2025       | 0.3750 | divergent |
| 39485438000142-2-000009/2025       | 0.3750 | divergent |
| 39485438000142-2-000010/2025       | 0.3750 | divergent |
| 39485438000142-2-000011/2025       | 0.3750 | divergent |

### Melhor candidato: 39485438000142-2-000012/2025 (score 0.50)

| campo           | status          | score | manual                          | oficial                                      |
|-----------------|-----------------|-------|---------------------------------|----------------------------------------------|
| cnpj            | match           | 1.00  | 39485438000142                  | 39485438000142                               |
| municipio       | match           | 1.00  | Belford Roxo                    | Belford Roxo                                 |
| uf              | match           | 1.00  | RJ                              | RJ                                           |
| vigencia_inicio | match           | 1.00  | 2025-11-04                      | 2025-11-04                                   |
| objeto_contrato | divergent       | 0.00  | LIMPEZA URBANA E MANEJO...      | AQUISICAO DE MATERIAL ESCOLAR...             |
| numero_contrato | divergent       | 0.00  | 02/SEMSEP/2025/2025             | 40/SEMED                                     |
| valor_contrato  | divergent       | 0.00  | 52801942.27                     | 1522778.0                                    |
| vigencia_fim    | divergent       | 0.00  | 2026-11-03                      | 2026-11-04                                   |

### Interpretacao

Todos os 10 candidatos retornam `divergent`. Isso e esperado: a API retornou
22 contratos em 3 paginas e apenas a pagina 1 foi consultada. O contrato de
limpeza urbana (02/SEMSEP/2025/2025, R$ 52M) nao esta entre os 10 primeiros
resultados da janela de datas usada na busca.

O sistema identificou corretamente que nenhum candidato da pagina 1 corresponde
ao registro manual, e os campos de orgao (CNPJ, municipio, UF) batem porque
todos os contratos retornados pertencem ao mesmo orgao.

### Proximos passos sugeridos

- Paginar a busca PNCP para cobrir as paginas 2 e 3.
- Ampliar a janela de datas se necessario.
- Se o contrato nao for encontrado nas paginas restantes, registrar como
  `missing_in_pncp` e acionar revisao documental.

## Validacoes Executadas

- compilacao com `compileall` sem erros;
- execucao do script sobre dado real salvo em `data/raw`;
- geracao de JSON e CSV em `data/processed/comparison/row67/`;
- score e status coerentes com os dados.
