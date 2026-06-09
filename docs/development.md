# Desenvolvimento

## Validacoes locais

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

## Instalar em modo editavel

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev,webapp,docs]"
```

## Regras praticas

- manter mudancas pequenas;
- registrar entregas em `documentation/plans/` e `documentation/reports/`;
- atualizar `docs/` quando a arquitetura ou o uso mudarem;
- nao chamar PNCP ou BrasilAPI em testes unitarios;
- preferir funcoes puras para comparacao, evidencia e relatorio;
- deixar Streamlit e scripts como bordas.

## CI

O CI roda:

- `ruff check .`;
- `pytest`.

O workflow de documentacao roda:

- `mkdocs build --strict`;
- deploy para GitHub Pages em `main`.
