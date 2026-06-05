# Relatorio: Endurecimento de Base de Engenharia — Entrega 001

## Objetivo

Tornar o projeto um pacote Python instalavel, eliminar hacks de `sys.path`,
introduzir testes automatizados, linting e CI, sem alterar comportamento.

## Artefatos Criados

- `pyproject.toml` — pacote instalavel (layout src/), deps base + extras
  (`webapp`, `ocr`, `dev`), config de ruff e pytest
- `README.md` — visao geral, instalacao, como rodar app e testes
- `src/sherlock_holmes/webapp/__init__.py`
- `src/sherlock_holmes/webapp/pncp.py` (movido de `scripts/app/pncp.py`)
- `src/sherlock_holmes/webapp/comparison.py` (movido de `scripts/app/comparison.py`)
- `src/sherlock_holmes/webapp/ui.py` (movido de `scripts/app/ui.py`)
- `tests/__init__.py`
- `tests/test_pncp_ids.py`
- `tests/test_pncp_dates.py`
- `tests/test_comparison.py`
- `tests/test_evidence.py`
- `.github/workflows/ci.yml`

## Artefatos Atualizados

- `scripts/pncp_streamlit_app.py` — importa de `sherlock_holmes.webapp`, sem hack
- `scripts/pages/comparacao_manual_pncp.py` — idem
- `scripts/compare_row67.py` — removido `sys.path.insert`
- `scripts/process_document_text.py` — removido `sys.path.insert`
- `scripts/run_ocr_manifest.py` — removido `sys.path.insert`
- `scripts/run_ocr_smoke.py` — removido `sys.path.insert`
- `scripts/run_pncp_api_smoke.py` — removido `sys.path.insert`

## Artefatos Removidos

- `scripts/app/` (pacote local substituido por `sherlock_holmes.webapp`)

## Decisoes Tecnicas

1. **Parser duplicado eliminado**: `webapp/comparison.py` reusa
   `sherlock_holmes.pncp.ids.parse_numero_controle_pncp` (que ja existia no
   nucleo) em vez de manter um regex proprio.

2. **Dependencias em camadas**: nucleo depende apenas de `pypdfium2` (lazy);
   `webapp` (streamlit, pandas) e `ocr` (torch, paddle, etc.) sao extras.
   Isso mantem o CI leve — instala apenas `[dev]` + base.

3. **Ruff**: line-length 120, regras E/F/I/W/B/UP. Notebooks excluidos do lint
   (artefatos exploratorios).

4. **Comportamento inalterado**: nenhuma funcao de logica foi modificada. Os
   testes reproduzem o caso validado da linha 67 (score 0.85, partial_match).

## Validacoes Executadas

- `pip install -e ".[dev]"` no `.venv` (Python 3.10) — pacote instalado editavel;
- `import sherlock_holmes` funciona de fora do projeto, sem `sys.path`;
- `grep sys.path.insert` em `*.py` — zero ocorrencias;
- `pytest` — **33 testes verdes** (0.11s);
- `ruff check .` — **All checks passed**;
- app Streamlit responde HTTP 200; modulos `webapp.*` importam em runtime;
- `candidate_detail_url` gera URL identica ao app anterior.

## Cobertura de Testes

| Arquivo               | Cobre                                                        |
|-----------------------|-------------------------------------------------------------|
| test_pncp_ids.py      | compact_digits, normalize_cnpj, parse/resolve control number |
| test_pncp_dates.py    | format/parse/validate/default date range                    |
| test_comparison.py    | _similarity (cnpj/number/date/text), compare_field_values,  |
|                       | compare_records (caso linha 67, divergent critico, match)   |
| test_evidence.py      | helpers de evidencia, roundtrip JSON, frozen dataclass      |

## Pendencias (dividas menores nao bloqueantes)

- `RecordComparison` permanece mutavel (tem lista de campos) — aceitavel;
- diretorios `benchmarking/` e `utils/` vazios — remover quando confirmado;
- pin de pandas em `ocr` alinhado a 2.2.3 (requirements-ocr.txt antigo tinha 2.3.3).
