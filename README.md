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
  pncp/                 # cliente e helpers da API PNCP
  validation/           # evidencia e comparacao
  documents/            # inspecao e extracao de texto
  ocr/                  # OCR como fallback
  webapp/               # helpers das paginas Streamlit
scripts/                # ferramentas operacionais e app Streamlit
tests/                  # testes automatizados (pytest)
documentation/          # planos, relatorios e roadmap
```

## Instalacao

Usando o ambiente virtual do projeto (`.venv`, Python 3.10):

```bash
.venv/Scripts/python.exe -m pip install -e ".[dev,webapp]"
```

Extras disponiveis: `webapp` (Streamlit), `ocr` (pipeline de OCR), `dev`
(pytest, ruff).

## Rodar o app

```bash
.venv/Scripts/python.exe -m streamlit run scripts/pncp_streamlit_app.py
```

## Testes e lint

```bash
.venv/Scripts/python.exe -m pytest
.venv/Scripts/python.exe -m ruff check .
```

## Documentacao

O estado do projeto e mantido em
`documentation/projetos-similares/plano-execucao-roadmap-sherlock-holmes.md`.
Cada entrega tem um plano em `documentation/plans/` e um relatorio em
`documentation/reports/`.
