# Instrucoes Para Agentes

## Idioma

- Conversas, planos, relatorios e documentacao do projeto devem ser escritos em portugues do Brasil.
- Codigo, nomes de arquivos, nomes de funcoes, classes, variaveis e comandos devem permanecer em ingles, salvo quando houver motivo claro para usar portugues.

## Ritual de Execucao

- Antes de executar uma nova parte do plano, ler o plano de execucao relevante e os relatorios existentes para entender o estado atual.
- Ao executar qualquer parte do plano de execucao, atualizar o arquivo de plano correspondente com:
  - o que foi feito
  - artefatos criados ou alterados
  - status atual da etapa
  - proximo passo operacional
- Quando houver uma mudanca relevante fora do plano, registrar tambem em `documentation/reports` quando fizer sentido.
- Apos modificacoes no repositorio, sugerir explicitamente um `git add` e um `git commit` com mensagem adequada.
- Nao fazer commit automaticamente sem confirmacao explicita do usuario.

## Validacao Local

- Usar sempre o Python do ambiente virtual local para comandos Python:

```powershell
.venv\Scripts\python.exe
```

- Antes de sugerir commit, rodar validacoes locais quando aplicavel.
- Quando configurados no projeto, preferir estes comandos de validacao rapida:

```powershell
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m ruff format --check .
```

- Se algum comando ainda nao estiver configurado no projeto, propor a configuracao antes de torna-lo obrigatorio.
- Smoke tests reais de OCR nao fazem parte da validacao rapida obrigatoria.
- Rodar smoke OCR quando a mudanca afetar OCR, preprocessamento, manifests, ambiente ou resultados documentados.
- Registrar resultados relevantes de OCR em `documentation/reports`.

## OCR

- Usar `documentation/plans/ocr-execution-plan-v1.md` como fonte principal do plano da rodada OCR atual.
- Manter os manifests versionaveis em `documentation/plans`.
- Manter resultados locais de execucao fora do Git quando estiverem em `data/interim`, `data/processed`, `.cache`, `.venv` ou `.local`.
- Usar `PaddleOCR` com `PP-OCRv4` nesta rodada, conforme registrado no relatorio de ambiente.
- Manter caches e downloads locais dentro do projeto quando possivel, especialmente em `.cache/` ou `.local/`.
- Para execucoes OCR automatizadas, preferir `scripts/run_ocr_smoke.py` e registrar `run_id` claro.

## Documentacao

- Atualizar `documentation/plans` quando o plano, o escopo ou o status operacional mudar.
- Atualizar `documentation/reports` quando houver resultado de execucao, decisao tecnica, problema de ambiente ou conclusao relevante.
- Evitar aprovar ferramenta OCR apenas por metricas automaticas; considerar tambem revisao qualitativa quando o plano exigir.
