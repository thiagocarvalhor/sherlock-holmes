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

## Organização dos testes

```text
tests/unit/domain/                 regras puras de domínio
tests/unit/application/            casos de uso e ports com fakes
tests/integration/adapters/        adapters inbound/outbound com mocks
tests/integration/streamlit/       renderização e helpers da UI
```

Novos testes devem entrar na camada mais próxima do comportamento testado. Testes unitários não devem chamar rede nem depender de arquivos grandes.

## CI

O CI roda:

- `ruff check .`;
- `pytest`.

O workflow de documentação roda:

- `mkdocs build --strict`;
- deploy para GitHub Pages em `main`.
