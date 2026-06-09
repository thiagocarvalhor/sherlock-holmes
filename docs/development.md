# Desenvolvimento

## Validações locais

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

## Instalar em modo editável

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev,webapp,docs]"
```

## Regras práticas

- manter mudanças pequenas;
- registrar entregas em `documentation/plans/` e `documentation/reports/`;
- atualizar `docs/` quando a arquitetura ou o uso mudarem;
- não chamar PNCP ou BrasilAPI em testes unitários;
- preferir funções puras para comparação, evidência e relatório;
- deixar Streamlit e scripts como bordas.

## CI

O CI roda:

- `ruff check .`;
- `pytest`.

O workflow de documentação roda:

- `mkdocs build --strict`;
- deploy para GitHub Pages em `main`.
