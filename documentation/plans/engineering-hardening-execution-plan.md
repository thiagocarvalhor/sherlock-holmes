# Plano de Execucao: Endurecimento de Base de Engenharia

## Objetivo

Tornar o projeto um pacote Python instalavel, eliminar os hacks de `sys.path`,
introduzir testes automatizados, linting e CI, sem alterar comportamento.

## Contexto

Auditoria identificou:

- pasta `tests/` existe mas vazia (zero testes);
- nenhum `pyproject.toml` / pacote instalavel;
- `sys.path.insert` em 9 arquivos;
- nenhum lint/format/CI configurado.

Ambiente alvo: `.venv` na raiz (Python 3.10.0, ja com streamlit, pandas,
pypdfium2, torch, paddle). Remote: GitHub `thiagocarvalhor/sherlock-holmes`.

Cadeia de imports confirmada: nucleo (`pncp`, `validation`, `documents`) usa
apenas stdlib; `pypdfium2` e importado de forma lazy; dependencias pesadas
(torch, paddle, doctr, cv2) vivem apenas em `ocr/` e `preprocessing/`.

## Escopo

### Inclui

1. **Empacotamento** — criar `pyproject.toml` com layout `src/`, deps base
   minimas e extras (`webapp`, `ocr`, `dev`), config de ruff e pytest.
2. **Instalacao editavel** — `pip install -e ".[dev,webapp]"` no `.venv`.
3. **Mover helpers da UI** — `scripts/app/*` para `src/sherlock_holmes/webapp/*`
   (modulo instalavel), eliminando o pacote local `app`.
4. **Parser puro** — mover `parse_numero_controle_pncp` para `pncp/ids.py`
   (stdlib puro, testavel sem pandas/streamlit); webapp re-exporta.
5. **Remover sys.path hacks** — nos 9 arquivos, apos instalacao editavel.
6. **Testes** — suite pytest cobrindo nucleo de logica.
7. **Linting** — config ruff e correcao de violacoes.
8. **CI** — workflow GitHub Actions (ruff + pytest, Python 3.10).

### Nao inclui

- mudanca de comportamento de qualquer funcao;
- BrasilAPI (Fase 4);
- reescrita de OCR.

## Estrutura de Dependencias (pyproject)

```text
[project]
requires-python = ">=3.10"
dependencies = ["pypdfium2==5.7.1"]   # nucleo: stdlib + extracao PDF lazy

[project.optional-dependencies]
webapp = ["streamlit==1.45.1", "pandas==2.2.3"]
ocr    = [Pillow, opencv-python, opencv-contrib-python, pytesseract,
          numpy, paddleocr, paddlepaddle, python-doctr, torch, torchvision]
dev    = ["pytest>=8", "ruff>=0.6"]
```

## Movimentacao de Arquivos

```text
scripts/app/__init__.py     -> src/sherlock_holmes/webapp/__init__.py
scripts/app/pncp.py         -> src/sherlock_holmes/webapp/pncp.py
scripts/app/comparison.py   -> src/sherlock_holmes/webapp/comparison.py
scripts/app/ui.py           -> src/sherlock_holmes/webapp/ui.py
```

Paginas Streamlit passam a importar de `sherlock_holmes.webapp.*`.

`parse_numero_controle_pncp` e `candidate_detail_url` (parte pura) -> `pncp/ids.py`.

## Arquivos sys.path a Limpar

```text
scripts/app/comparison.py        (movido)
scripts/app/pncp.py              (movido)
scripts/compare_row67.py
scripts/pages/comparacao_manual_pncp.py
scripts/pncp_streamlit_app.py
scripts/process_document_text.py
scripts/run_ocr_manifest.py
scripts/run_ocr_smoke.py
scripts/run_pncp_api_smoke.py
```

## Testes Planejados

```text
tests/__init__.py
tests/test_comparison.py   - _similarity (cnpj/number/date/text),
                             compare_field_values (missing/match),
                             compare_records (caso linha 67 sintetico)
tests/test_evidence.py     - helpers de evidencia, ValueError em tipo invalido,
                             roundtrip write/read em tmp_path
tests/test_pncp_ids.py     - parse_numero_controle_pncp (validos e invalido),
                             helpers existentes de ids/dates se puros
```

## CI

`.github/workflows/ci.yml` — em push e pull_request:
- setup Python 3.10;
- `pip install -e ".[dev]"`;
- `ruff check .`;
- `pytest`.

CI instala apenas `[dev]` (pytest, ruff) + base (pypdfium2). Testes nao
importam modulos pesados, mantendo o CI rapido.

## Status

Concluida.

## Resultado da Entrega

Pacote instalavel (`pyproject.toml` + `README.md`), helpers da UI movidos para
`sherlock_holmes.webapp`, 9 hacks de `sys.path` removidos, 33 testes pytest
verdes, `ruff check` limpo e workflow de CI no GitHub Actions.

Detalhes em `documentation/reports/engineering-hardening-001.md`.

Nota: o parser `parse_numero_controle_pncp` ja existia em `pncp/ids.py`; o
webapp passou a reusa-lo em vez de duplicar (ajuste em relacao ao plano).

## Criterio de Conclusao

- `import sherlock_holmes` funciona no `.venv` sem hack de sys.path;
- nenhum `sys.path.insert` restante em `scripts/`;
- app Streamlit sobe normalmente importando de `sherlock_holmes.webapp`;
- `pytest` passa com todos os testes verdes;
- `ruff check .` sem erros;
- workflow de CI presente e valido;
- comportamento das funcoes inalterado (testes confirmam a logica anterior).
```
