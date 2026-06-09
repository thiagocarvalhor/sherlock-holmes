# Começar

## Requisitos

- Python 3.10 ou superior;
- ambiente virtual local em `.venv`;
- Git;
- acesso à internet para chamadas reais ao PNCP, BrasilAPI e instalação de dependências.

## Instalar dependências

No Windows/PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev,webapp,docs]"
```

Para OCR completo, instale também o extra `ocr`:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev,webapp,docs,ocr]"
```

## Rodar validações

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

## Rodar Streamlit

```powershell
.\.venv\Scripts\python.exe -m streamlit run scripts\pncp_streamlit_app.py
```

Depois abra:

```text
http://localhost:8501
```

## Servir documentação local

```powershell
.\.venv\Scripts\python.exe -m mkdocs serve
```

Depois abra:

```text
http://localhost:8000
```
