# Ambiente da Rodada OCR 001

## Contexto

Registro inicial do ambiente local antes da instalação e execução das ferramentas da rodada 1.

Plano relacionado:

- `documentation/plans/ocr-execution-plan-v1.md`

## Sistema

- Sistema operacional: `Microsoft Windows NT 10.0.19045.0`
- Arquitetura: `64-bit`
- Processadores lógicos detectados: `8`
- Máquina: `DESKTOP-NP27SBK`

## Python Inicial Detectado

- Python: `3.10.0`
- pip: `21.2.3`
- Interpretador detectado: `C:\Users\thiag\AppData\Local\Programs\Python\Python310\python.exe`
- Ambiente virtual ativo neste shell: não detectado

## Ambiente Virtual do Projeto

- Diretório: `.venv`
- Prompt configurado: `sherlock-holmes`
- Python do venv: `3.10.0`
- pip inicial do venv: `21.2.3`
- pip atualizado no venv: `26.1`
- Interpretador do venv: `C:\Users\thiag\Documents\projetos\sherlock-holmes\.venv\Scripts\python.exe`
- Comando recomendado para execução automatizada: `.venv\Scripts\python.exe`

## Ferramentas OCR

- `Tesseract`: `5.5.0.20241111` instalado em `C:\Program Files\Tesseract-OCR\tesseract.exe`
- idiomas Tesseract disponíveis: `eng`, `osd`
- `pytesseract`: `0.3.13` instalado como wrapper Python
- `PaddleOCR`: `3.5.0` instalado e smoke real validado com `PP-OCRv4`
- `paddlepaddle`: `3.3.1` instalado, execução CPU validada com `paddle.utils.run_check()`
- `docTR`: `v1.0.1` instalado e import validado
- `torch`: `2.5.1+cpu` instalado e import validado
- `torchvision`: `0.20.1+cpu` instalado e import validado

## Pré-processamento

- `Pillow`: `12.2.0` instalado e import validado
- `OpenCV`: import `cv2` validado com versão efetiva `4.10.0`
- `opencv-python`: `4.13.0.92` instalado
- `opencv-contrib-python`: `4.10.0.84` instalado como dependência de `PaddleOCR`/`PaddleX`
- `numpy`: `2.2.6` instalado
- `pandas`: `2.3.3` instalado

## Dependências auxiliares verificadas

Pacotes principais instalados no ambiente `.venv`:

- `pytesseract`
- `paddleocr`
- `paddlepaddle`
- `python-doctr`
- `Pillow`
- `opencv-python`
- `opencv-contrib-python`
- `torch`
- `torchvision`

Validação de consistência:

- `pip check`: sem dependências Python quebradas

## Variáveis de Ambiente Para Execução

Para manter caches e modelos dentro do projeto, execuções com `PaddleOCR`, `PaddleX` ou `PaddlePaddle` devem configurar:

- `HOME`: raiz do projeto
- `USERPROFILE`: raiz do projeto
- `PADDLE_PDX_CACHE_HOME`: `.cache\paddlex`
- `PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT`: `False`
- `DOCTR_CACHE_DIR`: `.cache\doctr`
- `DOCTR_MULTIPROCESSING_DISABLE`: `TRUE`
- `TORCH_HOME`: `.cache\torch`
- `HF_HOME`: `.cache\huggingface`

Essas pastas ficam sob `.cache/`, que está ignorado no Git.

## Observações de Compatibilidade

- `PaddleOCR` deve ser importado de forma isolada, sem importar `paddle` manualmente antes no mesmo processo.
- `PaddleOCR` com `PP-OCRv5` falhou nesta máquina com erro oneDNN/MKLDNN; a configuração operacional inicial usa `PP-OCRv4`.
- `docTR` deve rodar com `torch==2.5.1` e `torchvision==0.20.1`; a tentativa inicial com `torch==2.11.0` falhou com erro nativo de DLL no Windows.
- `docTR` precisou de `DOCTR_MULTIPROCESSING_DISABLE=TRUE` para evitar erro de permissão em `ThreadPool`.
- Para o benchmark, a recomendação é executar cada engine OCR em subprocesso separado. Isso isola dependências nativas e evita conflitos entre `PaddlePaddle` e `Torch`.
- O `Tesseract` não depende mais do `PATH` para o runner, pois o adapter busca também o caminho padrão `C:\Program Files\Tesseract-OCR\tesseract.exe`.
- O idioma `por` não está instalado nesta rodada; o baseline inicial usa `eng`.

## Observações

- O shell PowerShell emitiu aviso de política de execução ao tentar carregar o perfil local: `Microsoft.PowerShell_profile.ps1`.
- Esse aviso não bloqueou os comandos executados nesta verificação.
- Este relatório começou a partir do ambiente disponível para os comandos executados pelo agente. Em seguida, foi criado um venv local exclusivo do projeto em `.venv`.
- A execução validada até aqui é CPU.
- A execução GPU não foi validada nesta rodada.
