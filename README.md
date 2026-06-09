# Sherlock Holmes

Pipeline investigativo e auditavel para contratos publicos.

```text
PNCP primeiro.
Documentos depois.
OCR apenas quando necessario.
Evidencia sempre.
```

O projeto compara registros de uma planilha manual contra dados oficiais do
PNCP (Portal Nacional de Contratacoes Publicas), preservando evidencia e nivel
de confianca por campo. Documentos e OCR entram como fallback quando o dado
estruturado nao basta.

## Estrutura

```text
src/sherlock_holmes/    # biblioteca instalavel
  domain/               # regras centrais, entidades e value objects
  application/          # casos de uso e ports
  adapters/             # entradas Streamlit/CLI e saidas PNCP/BrasilAPI/filesystem/OCR
  infrastructure/       # configuracao e detalhes tecnicos compartilhados
scripts/                # wrappers operacionais e app Streamlit
tests/                  # testes por camada (unit e integration)
docs/                   # documentacao navegavel MkDocs
documentation/          # planos, relatorios e roadmap
```

## Instalacao

Usando o ambiente virtual do projeto (`.venv`, Python 3.10):

```bash
.venv/Scripts/python.exe -m pip install -e ".[dev,webapp,docs]"
```

Extras disponiveis: `webapp` (Streamlit), `ocr` (pipeline de OCR), `dev`
(pytest, ruff) e `docs` (MkDocs).

## Rodar o app

```bash
.venv/Scripts/python.exe -m streamlit run scripts/pncp_streamlit_app.py
```

## Testes e lint

```bash
.venv/Scripts/python.exe -m pytest
.venv/Scripts/python.exe -m ruff check .
.venv/Scripts/python.exe -m mkdocs build --strict
```

## Documentacao

A documentacao navegavel fica em `docs/` e e gerada com MkDocs:

```bash
.venv/Scripts/python.exe -m mkdocs serve
```

O historico de execucao continua em `documentation/`: planos em
`documentation/plans/`, relatorios em `documentation/reports/` e roadmap em
`documentation/projetos-similares/plano-execucao-roadmap-sherlock-holmes.md`.
