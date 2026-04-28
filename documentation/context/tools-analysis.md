# Análise de Ferramentas para Extração de Texto

## Ferramentas Consideradas

### 1. Dedoc
- **Tipo**: Sistema universal de conversão de documentos
- **Licença**: Apache-2.0 (open source, gratuito)
- **Versão**: 2.6.1 (ativa e mantida)

#### O que Dedoc faz
Dedoc extrai de documentos:
- Conteúdo (texto)
- Estrutura lógica (headings, seções, listas)
- Tabelas (dados estruturados)
- Metadados
- Formatação (fontes, tamanhos, negrito, itálico, indentação)

#### Formatos suportados
- Office: DOCX, XLSX, PPTX, ODT
- Web: HTML, EML, MHTML
- Simples: TXT, CSV, JSON
- PDF: PDFs com texto (layer copiável)
- Scaneados: Imagens (PNG, JPG) + PDF sem texto
- Compactados: ZIP, RAR

#### Pipeline interno do Dedoc
```
Documento (qualquer formato)
↓
Dedoc detecta tipo
├─ PDF com texto? → pdfminer-six (similar ao PyMuPDF)
└─ Imagem/PDF scaneado? → Tesseract OCR
↓
Saída unificada (estrutura + texto + tabelas)
```

#### Capacidades especiais
- Detecção automática de orientação de páginas scaneadas
- OCR inteligente com Tesseract
- Análise avançada de tabelas com contour analysis
- Machine Learning para detectar bold, colunas, estrutura
- Suporte a documentos aninhados (documentos dentro de documentos)

### 2. PyMuPDF + PaddleOCR
- **PyMuPDF**: Extração de texto de PDFs com layer de texto
- **PaddleOCR**: OCR de alta precisão para documentos scaneados/imagens
- **Licença**: Ambas open source, gratuitas

#### Fluxo esperado (com fallback)
```
Documento
↓
Detectar se PDF tem texto
├─ Sim → PyMuPDF
└─ Não → PaddleOCR
↓
Texto extraído
```

#### Vantagens
- PaddleOCR é mais preciso que Tesseract
- Controle total sobre qual ferramenta usar e quando
- Implementação modular do pipeline

#### Desvantagens
- Requer lógica adicional de detecção e fallback
- Mais código para gerenciar
- Precisa tratar erros e validações manualmente

### 3. Markitdown
- **Desenvolvedor**: Microsoft
- **Tipo**: Biblioteca Python para extração de dados de múltiplos formatos
- **Licença**: Open source
- **Instalação**: `pip install markitdown`

#### O que faz
Extrai informações de diferentes fontes e converte para Markdown.

#### Formatos suportados
- PDF
- DOCX
- XLSX
- PowerPoint
- HTML
- E outros

#### Características
- Simples de usar
- Focado em conversão para Markdown
- Bom para extrair tabelas de Excel

#### Limitações observadas (segundo artigo)
- PDF com imagens e tabelas: não conseguiu extrair conteúdo das tabelas
- Saída para PDF: sem output

### 4. Docling
- **Desenvolvedor**: IBM
- **Tipo**: Biblioteca Python para extração e conversão de documentos
- **Licença**: Open source
- **Instalação**: `pip install docling`

#### O que faz
Extrai informações de documentos e converte para múltiplos formatos (Markdown, JSON, HTML).

#### Formatos suportados
- PDF
- DOCX
- XLSX
- HTML
- E outros

#### Características
- Múltiplos formatos de saída (Markdown, JSON, HTML)
- Detecta estrutura (imagens, tabelas, texto)
- Melhor em extração de Excel com fórmulas
- Preserva formulas em tabelas

#### Exemplo de uso
```python
from docling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"  # local path ou URL
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())  # saída em Markdown
```

#### Limitações observadas (segundo artigo)
- PDF com tabelas: detecta tabelas mas não extrai conteúdo
- Necessita exploração mais aprofundada

---

## Ferramentas OCR Específicas

### 5. Tesseract OCR
- **Desenvolvedor**: Google
- **Tipo**: OCR clássico (Machine Learning tradicional)
- **Licença**: Open source (Apache 2.0)
- **Interface Python**: Pytesseract

#### O que faz
Extrai texto de imagens e documentos scaneados.

#### Características
- Referência de precisão em OCR
- Suporta 100+ idiomas
- Rápido em processamento
- Sem suporte a GPU
- Saída estruturada básica (bounding boxes, confiança)

#### Interface Python - Pytesseract
```python
import pytesseract
from pytesseract import Output

# Extrair com dados estruturados
results = pytesseract.image_to_data(img, output_type=Output.DICT)

# Retorna: text, left, top, width, height, conf (confiança 0-100)

# Converter imagem para string
txt = pytesseract.image_to_string(img)
```

#### Vantagens
- Simples de usar
- Muito maduro e testado
- Baixo consumo de recursos

#### Desvantagens
- Menos preciso que deep learning
- Sem GPU support
- Instalação complexa (dependências do sistema)

### 6. EasyOCR
- **Desenvolvedor**: Comunidade open source
- **Tipo**: Deep Learning (CRAFT + CRNN)
- **Licença**: Apache 2.0
- **Instalação**: `pip install easyocr`

#### O que faz
OCR moderna usando redes neurais, otimizada para múltiplos idiomas.

#### Características
- Suporta 80+ idiomas
- GPU support
- Precisa de download de modelos (primeira execução)
- Melhor precisão que Tesseract em casos complexos
- Interface Python simples

#### Exemplo
```python
import easyocr

reader = easyocr.Reader(['en', 'pt'])
result = reader.readtext('imagem.png')

# result contém: [([x1,y1,x2,y2,x3,y3,x4,y4], texto, confiança), ...]
```

#### Vantagens
- Alta precisão
- Suporte a GPU
- Comunidade ativa
- Múltiplos idiomas

#### Desvantagens
- Primeiro uso baixa modelos (lento)
- Consumo de memória maior
- Comunidade menor que Tesseract

---

## Ferramentas de Extração de PDF (Alternativas)

### 14. pypdfium2
- **Tipo**: Extração de PDF rápida
- **Licença**: Apache 2.0
- **Instalação**: `pip install pypdfium2`
- **Performance**: 0.003s por página (MAIS RÁPIDO)

#### O que faz
Extração básica de texto de PDFs com máxima velocidade.

#### Características
- Velocidade extrema (0.003s/página)
- Sem formatação, apenas texto puro
- Sem dependências complexas
- C++ binding otimizado

#### Exemplo
```python
import pypdfium2 as pdfium

text = "\n".join(
    p.get_textpage().get_text_range() 
    for p in pdfium.PdfDocument("doc.pdf")
)
```

#### Vantagens
- Blazingly fast
- Simples de usar
- Sem overhead

#### Desvantagens
- Sem preservação de formatação
- Sem suporte a tabelas
- Apenas texto puro

### 15. pypdf
- **Tipo**: Extração PDF Pythonic
- **Licença**: BSD
- **Instalação**: `pip install pypdf`
- **Performance**: 0.024s por página

#### O que faz
Extração confiável de texto de PDFs, sem dependências C.

#### Características
- Funciona em Lambda functions
- Sem C dependencies (containerizable)
- Extração básica, ocasionais problemas de espaçamento
- Muito testado e consolidado

#### Exemplo
```python
from pypdf import PdfReader

reader = PdfReader("doc.pdf")
text = "\n".join(p.extract_text() for p in reader.pages)
```

#### Vantagens
- Extremamente confiável
- Sem dependências do sistema
- Ótimo para ambientes containerizados
- Comunidade grande

#### Desvantagens
- Ocasionais problemas de espaçamento
- Sem estrutura ou formatação
- Sem suporte a tabelas nativo

### 16. pdfplumber
- **Tipo**: Extração de dados estruturados de PDF
- **Licença**: MIT
- **Instalação**: `pip install pdfplumber`
- **Performance**: 0.10s por página

#### O que faz
Extração avançada de dados tabulares e texto com análise de layout.

#### Características
- Extração de tabelas excelente
- Análise de coordenadas
- Controle fino de layout
- Bounding box support

#### Exemplo
```python
import pdfplumber

with pdfplumber.open("doc.pdf") as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    tables = page.extract_tables()
```

#### Vantagens
- Excelente para tabelas
- Análise de layout fino
- Coordenadas precisas
- Muitas opções configuráveis

#### Desvantagens
- Requer configuração para texto simples
- Necessita de sintonia para bons resultados
- Overhead de análise

### 17. pymupdf4llm
- **Tipo**: Extrator PDF → Markdown
- **Licença**: AGPL
- **Instalação**: `pip install pymupdf4llm`
- **Performance**: 0.12s por página

#### O que faz
Converte PDFs em Markdown estruturado, preservando hierarquia.

#### Características
- Saída Markdown limpa
- Preserva headings e estrutura
- Suporte a tabelas
- Formatação bem estruturada

#### Exemplo
```python
import pymupdf4llm

markdown = pymupdf4llm.to_markdown("doc.pdf")
print(markdown)
```

#### Vantagens
- Markdown estruturado
- Bom para RAG/LLMs
- Velocidade razoável
- Preserva hierarquia

#### Desvantagens
- AGPL license (cuidado em projetos comerciais)
- Menos preciso em layouts complexos

### 18. unstructured
- **Tipo**: Particionamento semântico de documentos
- **Licença**: Apache 2.0
- **Instalação**: `pip install "unstructured[all-docs]"`
- **Performance**: 1.29s por página

#### O que faz
Particiona documentos em chunks semânticos (Title, NarrativeText, etc).

#### Características
- Detecção semântica de elementos
- Categorização automática
- Perfeito para RAG
- Suporte a múltiplos formatos

#### Exemplo
```python
from unstructured.partition.auto import partition

blocks = partition(filename="doc.pdf")
for block in blocks:
    print(f"{block.category}: {block.text}")
    # Categorias: Title, NarrativeText, Table, etc.
```

#### Vantagens
- Chunks semânticos (perfeito para RAG)
- Detecção automática de tipo
- Integração com embeddings
- Múltiplos formatos

#### Desvantagens
- Mais lento (1.29s/página)
- Dependências pesadas
- Overhead computacional

### 19. marker-pdf
- **Tipo**: Conversion PDF → Markdown com Vision Model
- **Licença**: GPL-3.0
- **Instalação**: `pip install marker-pdf`
- **Performance**: 11.3s por página (primeira vez baixa 1GB modelo)

#### O que faz
Conversão de alta fidelidade de PDFs para Markdown usando modelos vision.

#### Características
- Layout perfeito preservado
- Reconhecimento de imagens
- Markdown estruturado
- Vision model (1GB)

#### Exemplo
```python
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

text, _, _ = text_from_rendered(
    PdfConverter(create_model_dict())("doc.pdf")
)
```

#### Vantagens
- Layout impecável
- Melhor qualidade geral
- Imagens preservadas
- Markdown estruturado

#### Desvantagens
- Muito lento (11.3s/página)
- 1GB modelo (primeira execução)
- Alto consumo de recursos
- GPL-3.0 (verificar licença para seu caso)

### 20. textract
- **Tipo**: Extrator universal com OCR fallback
- **Licença**: MIT
- **Instalação**: `pip install textract` (requer Tesseract do sistema)
- **Performance**: 0.05s por página

#### O que faz
Extração de texto de múltiplos formatos com fallback automático para OCR.

#### Características
- Suporta PDF, DOCX, DOC, HTML, XLS, etc.
- OCR automático se necessário
- Trata múltiplos formatos uniformemente
- Simples de usar

#### Exemplo
```python
import textract

text = textract.process("doc.pdf").decode()
```

#### Vantagens
- Formato agnóstico
- OCR fallback automático
- Interface uniforme
- Rápido

#### Desvantagens
- Dependência de Tesseract do sistema
- Menos controle fino
- Menor precisão em documentos complexos

### 7. Keras-OCR
- **Desenvolvedor**: Comunidade open source
- **Tipo**: Deep Learning
- **Licença**: MIT
- **Instalação**: `pip install keras-ocr`

#### Características
- Baseado em Keras/TensorFlow
- Bom para casos específicos
- Comunidade pequena

#### Limitações
- Desenvolvimento parou
- Comunidade pequena
- Menos recomendado para novos projetos

### 8. PaddleOCR
- **Desenvolvedor**: Baidu
- **Tipo**: Deep Learning (PaddlePaddle framework)
- **Licença**: Apache 2.0
- **Instalação**: `pip install paddleocr`

#### O que faz
OCR de alta precisão otimizado para velocidade.

#### Características
- Suporta 80+ idiomas
- GPU support
- Excelente relação precisão/velocidade
- Modelos pré-treinados
- Muito rápido

#### Exemplo
```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='pt')
result = ocr.ocr('imagem.png', cls=True)

# result: [[(bbox, (texto, confiança)), ...], ...]
```

#### Vantagens
- Excelente qualidade
- Muito rápido
- GPU optimizado
- Múltiplos idiomas

#### Desvantagens
- Menos comunidade que Tesseract
- Documentação em chinês

---

## Ferramentas OCR em Cloud

### 9. Azure Form Recognizer (Microsoft)
- **Tipo**: OCR + ML avançado em cloud
- **Modelo**: Especializado em formulários e documentos estruturados
- **Preço**: Por uso (pago)

#### O que faz
Extrai texto, key-value pairs, tabelas e estrutura de documentos.

#### Especialização
- Formulários
- Invoices/Faturas
- Recibos
- Cartões de identidade
- Documentos estruturados

#### Vantagens
- Excelente para documentos estruturados como licitações
- Reconhecimento de tabelas perfeito
- Muito preciso
- Suporte Microsoft

#### Desvantagens
- Pago
- Limite de requisições
- Dependência de cloud

### 10. Amazon Textract
- **Tipo**: OCR + ML avançado em cloud
- **Desenvolvedor**: Amazon AWS
- **Preço**: Por uso (pago)

#### O que faz
Extrai texto, tabelas e formulários de documentos.

#### Características
- Reconhecimento de tabelas excelente
- Análise de formulários
- OCR de alta precisão

#### Vantagens
- Integrável com AWS
- Muito preciso
- Bom suporte

#### Desvantagens
- Pago
- Limite de requisições
- Dependência de cloud

### 11. Google Cloud Vision
- **Tipo**: OCR + Computer Vision em cloud
- **Desenvolvedor**: Google
- **Preço**: Por uso (pago)

#### O que faz
OCR geral + detecção de objetos, faces, logos.

#### Características
- Geral (não especializado)
- Muito preciso para texto
- Integração com Google Cloud

#### Vantagens
- Tecnologia Google
- Muito preciso

#### Desvantagens
- Pago
- Menos especializado que Form Recognizer/Textract
- Limite de requisições

---

## Ferramentas de Extração com LLM

### 12. LangExtract
- **Desenvolvedor**: Google
- **Tipo**: Biblioteca Python para extração AI-powered com LLMs
- **Licença**: Open source
- **Instalação**: `pip install langextract`
- **Modelos suportados**: OpenAI GPT, Google Gemini, Anthropic Claude, modelos locais (Ollama)

#### O que faz
Transforma texto não-estruturado em dados estruturados usando Large Language Models (LLMs).

#### Como funciona
Define um schema (estrutura de dados desejada) e o LLM extrai campos semanticamente relevantes do texto.

#### Exemplo básico
```python
from langextract import Extractor, Schema, Field

# Definir schema
schema = Schema(
    products=Field(
        type="list",
        fields={
            "name": Field(type="string"),
            "price": Field(type="float")
        }
    )
)

# Criar extrator
extractor = Extractor(schema=schema, model="gpt-4-turbo")

# Texto desorganizado
text = """
Our latest launch includes:
- iPhone 15 Pro priced at $1199
- MacBook Air M3 priced at $1399
"""

# Extrair
result = extractor.extract(text)
# Retorna: {"products": [{"name": "iPhone 15 Pro", "price": 1199.0}, ...]}
```

#### Características principais
- Define schemas para estruturar output
- Suporta múltiplos modelos LLM
- Chunking automático para textos longos
- Processamento paralelo de batches
- Context-aware extraction (entende o significado)
- Retorna JSON, CSV ou DataFrames
- Integração com pandas, ETL pipelines

#### Casos de uso
- Extração de resumes (nome, skills, experiência)
- Parsing de invoices (vendor, data, total)
- Categorização de support tickets
- Estruturação de emails
- Análise de relatórios financeiros
- Licitações (valor, data, objeto, órgão)

#### Saída
```python
import pandas as pd

# Converter para DataFrame
df = pd.DataFrame(result["products"])

# Salvar como CSV
df.to_csv("products.csv")

# Visualizar
df.plot(x="name", y="price", kind="bar")
```

#### Vantagens
- Entende contexto semântico (não é regex)
- Define estrutura facilmente com schemas
- Cuida de variações no texto ("USD 1199", "$1,199", "1.199 dólares")
- Suporta documentos longos com chunking
- Integração com múltiplos LLMs
- Transformação em múltiplos formatos (JSON, CSV, DataFrame)
- Perfeito para dados despadronizados

#### Desvantagens
- Requer API key (OpenAI, Gemini, etc.)
- Custo por chamada de API
- Latência de rede (cloud models)
- Depende da qualidade do modelo LLM escolhido
- Precisa de schemas bem definidos

#### Instalação e setup
```bash
# 1. Criar virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 2. Instalar
pip install langextract

# 3. Configurar API key (OpenAI exemplo)
export OPENAI_API_KEY="sua_chave_aqui"

# 4. Verificar
python -m langextract --version
```

#### Dicas de otimização
- Manter campos específicos ("price" melhor que "data")
- Usar modelos menores (gpt-3.5-turbo) para volume alto e economizar custo
- Cachear respostas localmente para datasets grandes
- Integrar em pipelines Airflow ou dbt para processamento agendado
- Usar modelos locais (Ollama) para casos sensíveis a privacidade

#### Integração com Sherlock Holmes
LangExtract seria perfeito para a **Fase 5 (Extração de campos estruturados)**:

```python
# Exemplo para licitação
schema = Schema(
    valor_estimado=Field(type="float"),
    data_abertura=Field(type="string"),
    objeto_licitacao=Field(type="string"),
    orgao_responsavel=Field(type="string"),
    modalidade=Field(type="string"),
    edital_link=Field(type="string")
)

# Após extrair texto (Fase 3), passar para LangExtract
extractor = Extractor(schema=schema, model="gpt-4-turbo")
campos_estruturados = extractor.extract(texto_da_licitacao)

# Resultado: JSON estruturado pronto para armazenar/analisar
```

### 13. SmolDocling
- **Desenvolvedor**: HuggingFace + IBM (colaboração)
- **Tipo**: Modelo vision ultra-compacto para document conversion
- **Tamanho**: 256M parâmetros (5-10x menor que concorrentes)
- **Performance**: Compara com modelos 27x maiores
- **Licença**: Open source
- **Instalação**: `pip install docling-core mlx-vlm pillow`
- **Framework**: MLX (Apple Silicon) ou PyTorch

#### O que faz
Converte imagens de documentos em formato DocTags (XML-like) preservando estrutura, layout e conteúdo.

#### DocTags Format
Formato XML-like que define:
- Element type: texto, imagem, tabela, código, título, rodapé
- Position on page: bounding box (x1, y1, x2, y2)
- Content: informação textual ou estrutural

```xml
<document>
  <section>
    <heading>Título</heading>
    <paragraph>Parágrafo de texto</paragraph>
    <table>
      <table_row>
        <table_cell>Dado</table_cell>
      </table_row>
    </table>
  </section>
</document>
```

#### Características principais
- End-to-end document conversion
- Preserva reading order (ordem de leitura)
- Mantém layout original (posição de elementos)
- Reconhecimento de tabelas com estrutura
- OCR integrado
- Extração de equações matemáticas
- Code list recognition
- Nested structures support
- Position-aware (bounding boxes)
- Tamanho ultra-compacto

#### Casos de uso
- Document classification (classificação)
- OCR (reconhecimento de texto)
- Layout analysis (análise de estrutura)
- Table recognition (reconhecimento de tabelas)
- Key-value extraction (extração de pares chave-valor)
- Graph understanding (compreensão de gráficos)
- Equation recognition (reconhecimento de equações)
- Code extraction

#### Exemplo de uso
```python
from io import BytesIO
from pathlib import Path
from PIL import Image
from docling_core.types.doc import ImageRefMode
from docling_core.types.doc.document import DocTagsDocument, DoclingDocument
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config, stream_generate

# Carregar modelo
model_path = "ds4sd/SmolDocling-256M-preview-mlx-bf16"
model, processor = load(model_path)
config = load_config(model_path)

# Preparar entrada
prompt = "Convert this page to docling."
image = "documento.png"

# Carregar imagem
pil_image = Image.open(image)

# Aplicar template
formatted_prompt = apply_chat_template(processor, config, prompt, num_images=1)

# Gerar DocTags
output = ""
for token in stream_generate(
    model, processor, formatted_prompt, [image], max_tokens=4096
):
    output += token.text
    if "</doctag>" in token.text:
        break

# Criar documento
doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([output], [pil_image])
doc = DoclingDocument(name="Documento")
doc.load_from_doctags(doctags_doc)

# Exportar
print(doc.export_to_markdown())  # Markdown
doc.save_as_html(Path("output.html"))  # HTML
```

#### Vantagens
- Ultra-compacto (256M params) - roda localmente
- Performance competitiva com modelos 27x maiores
- End-to-end (sem pipeline complexo)
- Preserva estrutura e layout
- Excelente em tabelas, equações, code lists
- Open source
- Sem dependência de API cloud
- Suporta Apple Silicon (MLX)
- Formato DocTags bem definido

#### Desvantagens
- Requer mais poder computacional que Tesseract
- Ainda requer download de modelo (256M)
- Comunidade menor que alternativas (novo)
- MLX limitado a Apple Silicon (PyTorch necessário para outros)

#### Performance (vs. outros modelos)
Segundo benchmark DocLayNet:
- Edit Distance: 0.48 (mais baixo = melhor)
- F1-Score: 0.80 (mais alto = melhor)
- Code lists: 0.11 Edit Distance, 0.92 F1-Score
- Equações: 0.11 Edit Distance, 0.95 F1-Score

Comparação: Supera Qwen2.5-VL (7B params) em várias métricas.

#### Integração com Sherlock Holmes
SmolDocling seria excelente para **Fase 3 (Extração de estrutura)**:

```python
# Após OCR/extração básica, usar SmolDocling
# para preservar estrutura e layout

# Vantagem: Extrai tabelas estruturadas
# Vantagem: Sem dependência de cloud (local)
# Vantagem: Compacto o suficiente para serverless/edge
```

---

## Conceito: Gerenciamento de Fallback

Fallback = plano B quando algo falha.

### Sem gerenciamento (não robusto)
```python
texto = extrair_com_pymupdf(documento)  # Tenta uma vez
# Se falhar, tudo quebra
```

### Com gerenciamento (robusto)
```python
try:
    texto = extrair_com_pymupdf(documento)
    if texto está vazio:
        raise Exception("PDF sem texto detectável")
except:
    logger.info("PyMuPDF falhou, tentando PaddleOCR...")
    try:
        texto = extrair_com_paddleocr(documento)
        if texto está vazio:
            raise Exception("PaddleOCR também falhou")
    except Exception as e:
        logger.error(f"Todas as ferramentas falharam: {e}")
        raise

return texto
```

### O que gerenciar
1. Detectar quando usar cada ferramenta
2. Capturar erros em cada etapa
3. Validar resultado (não vazio, qualidade mínima)
4. Logging detalhado (qual ferramenta foi usada, erros)

---

## Comparação Completa: Todas as Ferramentas

### Categoria 1: Parsers Gerais (Multi-formato)

| Aspecto | Dedoc | Markitdown | Docling | SmolDocling |
|---------|-------|------------|---------|-------------|
| Desenvolvedor | ISPRAS (Rusia) | Microsoft | IBM | HuggingFace + IBM |
| Gerenciamento de fallback | Automático | Não | Não | Não |
| OCR integrado | Tesseract | Não | Não | Sim (vision-based) |
| Extração de estrutura | Sim (headings, listas, tabelas) | Sim (básica) | Sim (estrutura + fórmulas) | Sim (end-to-end com DocTags) |
| Formatos de entrada | PDF/DOCX/XLSX/HTML/imagens/ZIP | PDF/DOCX/XLSX/PPT/HTML | PDF/DOCX/XLSX/HTML | Imagens/PDF (vision) |
| Formatos de saída | JSON/estrutura nativa | Markdown | Markdown/JSON/HTML | DocTags/Markdown/HTML |
| Tabelas PDF | Detecta estrutura | Falha em PDFs | Detecta mas não extrai | Excelente |
| Imagens em PDF | Detecta | Não | Detecta | Sim (vision-based) |
| Equações matemáticas | Não | Não | Não | Sim |
| Scaneados/Imagens | Sim (OCR) | Não | Não | Sim (vision-based) |
| Layout/Positioning | Básico | Não | Básico | Excelente (bounding boxes) |
| Instalação | Docker ou pip | pip | pip | pip (MLX ou PyTorch) |
| Complexidade | Simples | Simples | Simples | Simples |
| Tamanho modelo | Médio | Médio | Médio | 256M (ultra-compacto) |

### Categoria 2: Ferramentas OCR Específicas (Open Source)

| Aspecto | Tesseract | EasyOCR | Keras-OCR | PaddleOCR |
|---------|-----------|---------|-----------|-----------|
| Desenvolvedor | Google | Comunidade | Comunidade | Baidu |
| Tipo | OCR clássico | Deep Learning | Deep Learning | Deep Learning |
| Qualidade | Boa (referência) | Muito boa | Boa | Excelente |
| Idiomas | 100+ | 80+ | Limitado | 80+ |
| Velocidade | Rápido | Médio | Lento | Rápido |
| Precisão | Média | Alta | Alta | Muito Alta |
| Interface Python | Pytesseract | Nativa | Nativa | Nativa |
| GPU support | Não | Sim | Sim | Sim |
| Formatos entrada | Imagens | Imagens | Imagens | Imagens |
| Saída estruturada | Pouca | Pouca | Pouca | Pouca |
| Instalação | Complexa (dependências) | pip | pip | pip |
| Comunidade | Grande | Crescente | Pequena | Crescente |

### Categoria 3: Ferramentas OCR em Cloud (Pagas)

| Aspecto | Azure Form Recognizer | Amazon Textract | Google Cloud Vision |
|---------|----------------------|-----------------|---------------------|
| Desenvolvedor | Microsoft | Amazon | Google |
| Tipo | ML avançado (cloud) | ML avançado (cloud) | ML avançado (cloud) |
| Qualidade | Excelente | Excelente | Excelente |
| Especialização | Formulários/documentos estruturados | Documentos estruturados | Geral |
| Preço | Pago | Pago | Pago |
| OCR | Sim | Sim | Sim |
| Extração de dados | Sim (key-value, tabelas, estrutura) | Sim (tabelas, texto, formulários) | Sim (texto, objetos) |
| Reconhecimento de tabelas | Excelente | Excelente | Bom |
| Reconhecimento de formulários | Excelente | Excelente | Bom |
| Limite de requisições | Sim | Sim | Sim |
| Documentação | Excelente | Excelente | Excelente |
| Integração | Fácil via SDK | Fácil via SDK | Fácil via SDK |

### Categoria 4: Combinação Clássica

| Aspecto | PyMuPDF + PaddleOCR |
|---------|---------------------|
| Para PDFs com texto | PyMuPDF |
| Para PDFs scaneados | PaddleOCR |
| Gerenciamento de fallback | Manual (seu código) |
| Controle | Total |
| Complexidade | Complexa |
| Custo | Gratuito |

### Categoria 5: PDF Extraction Specific (Benchmark do Artigo 2025)

| Ferramenta | Velocidade | Qualidade Texto | Tabelas | Estrutura | Recomendado Para |
|-----------|-----------|-----------------|---------|-----------|------------------|
| **pypdfium2** | 0.003s (FASTEST) | Básica | Não | Não | Alto volume, indexação simples |
| **pypdf** | 0.024s | Confiável | Não | Não | Lambda, containers |
| **pdfplumber** | 0.10s | Boa | Excelente | Média | Extração de dados tabulares |
| **pymupdf4llm** | 0.12s | Excelente | Sim | Sim (Markdown) | Markdown, RAG systems |
| **textract** | 0.05s | Boa | Média | Não | Multi-formato com OCR |
| **unstructured** | 1.29s | Estruturada | Média | Excelente (semântica) | RAG, chunks semânticos |
| **marker-pdf** | 11.3s | Perfeita | Excelente | Perfeita (vision) | Alta fidelidade, imagens |

**Nota importante:** Tempos baseados em teste com 1 página. marker-pdf baixa 1GB modelo na primeira execução.

**Trade-offs observados:**
- Speed vs Quality: pypdfium2 é 3000x mais rápido que marker-pdf
- Structure vs Simplicity: unstructured/marker-pdf têm estrutura mas são lentos
- Reliability: pypdf é o mais confiável (sem C dependencies)

### Categoria 5.5: Extração com LLM (IA-powered)

| Aspecto | LangExtract | LangChain (custom) | Modelos LLM puros |
|---------|-------------|-------------------|-------------------|
| Desenvolvedor | Google | Comunidade | OpenAI/Anthropic/Google |
| Tipo | Extração com schema | Framework customizável | Chamadas diretas |
| Modelos | GPT, Gemini, Claude, locais | Qualquer LLM | Qualquer LLM |
| Instalação | pip install | pip install | API keys |
| Schemas/estrutura | Sim (Field-based) | Customizável | Manual via prompts |
| Context-aware | Sim (entende semântica) | Sim | Sim |
| Tratamento de variações | Automático | Manual | Manual |
| Saída estruturada | JSON/CSV/DataFrame | Customizável | JSON (com parsing) |
| Chunking automático | Sim | Parcial | Não |
| Processamento paralelo | Sim | Sim | Não |
| Documentação | Boa | Excelente | Excelente |
| Custo | API key (pago) | API key (pago) | API key (pago) |
| Latência | Médio-Alto | Médio-Alto | Médio-Alto |
| Privacidade | Envia para cloud | Envia para cloud | Envia para cloud |
| Modelos locais | Sim (Ollama) | Sim (LLaMA, etc) | Sim (Ollama) |

### Categoria 5: Extração com LLM (IA-powered)

| Aspecto | LangExtract | LangChain (custom) | Modelos LLM puros |
|---------|-------------|-------------------|-------------------|
| Desenvolvedor | Google | Comunidade | OpenAI/Anthropic/Google |
| Tipo | Extração com schema | Framework customizável | Chamadas diretas |
| Modelos | GPT, Gemini, Claude, locais | Qualquer LLM | Qualquer LLM |
| Instalação | pip install | pip install | API keys |
| Schemas/estrutura | Sim (Field-based) | Customizável | Manual via prompts |
| Context-aware | Sim (entende semântica) | Sim | Sim |
| Tratamento de variações | Automático | Manual | Manual |
| Saída estruturada | JSON/CSV/DataFrame | Customizável | JSON (com parsing) |
| Chunking automático | Sim | Parcial | Não |
| Processamento paralelo | Sim | Sim | Não |
| Documentação | Boa | Excelente | Excelente |
| Custo | API key (pago) | API key (pago) | API key (pago) |
| Latência | Médio-Alto | Médio-Alto | Médio-Alto |
| Privacidade | Envia para cloud | Envia para cloud | Envia para cloud |
| Modelos locais | Sim (Ollama) | Sim (LLaMA, etc) | Sim (Ollama) |

---

## Limitações de cada ferramenta

### Dedoc
- Não faz extração de campos específicos
- Não faz classificação de documento
- Não tem compreensão semântica de contexto

### PyMuPDF + PaddleOCR
- Não extrai estrutura lógica automaticamente
- Não tem reconhecimento automático de tabelas
- Não normaliza formatos diferentes

### Markitdown
- Sem OCR (não funciona com imagens/PDF scaneados)
- Não extraiu tabelas de PDF no teste
- Não funciona bem com PDFs complexos

### Docling
- Sem OCR (não funciona com imagens/PDF scaneados)
- Detecta tabelas mas não extrai conteúdo em PDF
- Requer mais exploração e testes

---

## Insights do Artigo: Markitdown vs Docling

### Teste com PDF
Resultado: Ambas tiveram dificuldade
- Markitdown: Sem output
- Docling: Detectou tabelas e imagens, mas não extraiu conteúdo

### Teste com Excel
Resultado: Docling superior para casos específicos

**Markitdown**: Extrai valores das células em Markdown, mas saída com muitos "NaN" (células vazias)

**Docling**: 
- Extrai valores em formato limpo
- Preserva fórmulas do Excel
- Saída mais estruturada e legível

### Conclusão do artigo
Ambas ferramentas complementam-se bem. Para extrair tanto fórmulas quanto valores, usar ambas em conjunto é eficaz.

---

## Observação Importante

Nenhuma das ferramentas até agora resolveu perfeitamente:
- Extração de dados de tabelas em PDF
- OCR de alta qualidade integrado
- Compreensão semântica para campos específicos

Isso reforça que o pipeline do Sherlock Holmes precisará de múltiplas camadas (estrutura + classificação + extração semântica).

---

## Artigo: OCR - Extracting Value from Unstructured Data

### Contexto Geral (Gavita Regunath, 2023)

**Problema:**
- 80-90% de dados globais são não-estruturados
- Crescimento de 55-65% ao ano
- Difícil de analisar e usar para decisões
- Referido como "dark data" (dados sem valor aparente)

**Conceitos:**
- Dados estruturados: organizados, máquina-legível (Excel, bancos de dados)
- Dados não-estruturados: documentos scaneados, imagens, áudio, vídeo, posts

### Por que OCR importa

OCR converte "dark data" em dados estruturados e utilizáveis.

Exemplos de aplicação por setor:

1. Healthcare: Digitalizar e organizar prontuários médicos
2. Finance/Banking: Extrair dados de faturas, recibos, extratos bancários
3. Legal: Converter contratos e briefs em texto pesquisável
4. Retail: Extrair dados de recibos para automação de contas a pagar
5. Government: Automatizar extração de formulários, declarações fiscais
6. Manufacturing: Extrair dados de relatórios de inspeção e testes
7. Education: Digitalizar livros e materiais de estudo

### Ferramentas disponíveis

Opções livres/open source:
- Tesseract (Google, muito preciso)
- EasyOCR
- Keras-OCR

Opções pagas (cloud):
- Azure Form Recognizer
- Amazon Textract
- Google Cloud Vision

### Exemplo Prático: Pytesseract

Caso de uso: Extrair informações de uma fatura em francês.

Código básico:
```python
import pytesseract
from pytesseract import Output
import cv2

# Extrair dados estruturados
results = pytesseract.image_to_data(img, output_type=Output.DICT)

# Dados retornados:
# - text: palavras detectadas
# - left: distância do canto esquerdo (pixels)
# - top: distância do topo (pixels)
# - width/height: dimensões do bounding box
# - conf: confiança da predição (0-100)
```

Filtrando por confiança:
```python
confidence_value = 70

for i in range(len(results["text"])):
    conf = int(results["conf"][i])
    
    if conf > confidence_value:
        # Desenhar retângulo ao redor do texto
        # Adicionar texto na imagem
        # Procurar apenas predictions com alta confiança
```

Convertendo imagem para string:
```python
txt = pytesseract.image_to_string(file_name)
```

### Após extrair o texto

O artigo sugere:
- Tradução automática (usando Google Translate)
- Análise de conteúdo
- Integração com outros sistemas
- Para escala: usar Azure Form Recognizer (cloud, mais robusto)

### Insights para o Sherlock Holmes

1. OCR não é binário - há níveis de confiança
2. Pode-se filtrar resultados por confiança
3. Bounding boxes ajudam a localizar dados
4. Tesseract é referência de precisão
5. Para invoices/formulários: Form Recognizer é melhor (cloud, ML avançado)
6. Pós-extração pode incluir tradução, análise, integração


---

## Pipeline Completo: Integrando Todas as Ferramentas

### Fluxo recomendado para Sherlock Holmes

```
Fase 1: Buscar licitações (PNCP, portais)
↓
Fase 2: Baixar documentos
↓
Fase 3: Extrair texto e estrutura
├─ Opção A: Dedoc (completo, consolidado)
├─ Opção B: SmolDocling (ultra-compacto, excelente tabelas)
├─ Opção C: PyMuPDF + PaddleOCR (maximal control)
├─ Opção D: Docling (alternativa, bom em Excel)
└─ Opção E: Tesseract + Markitdown (simplista)
↓
Fase 4: Classificar documento
├─ Detectar: "É licitação? Qual tipo?"
└─ Ferramentas: ML model ou LLM
↓
Fase 5: Extrair campos estruturados
├─ Opção A: LangExtract (recomendado, semântico)
├─ Opção B: LLM custom (GPT, Claude direto)
├─ Opção C: Azure Form Recognizer (cloud, otimizado)
└─ Opção D: Regex + regras (básico)
↓
JSON estruturado final
```

### Sugestão de Stack para MVP

**Fase 3 (Extração de texto):** SmolDocling OU Dedoc
- SmolDocling: ultra-compacto, excelente em tabelas, DocTags nativo
- Dedoc: mais consolidado, fallback automático, mais comunidade

**Fase 4 (Classificação):** LLM leve (GPT-3.5 small) ou modelo classificação simples
- Detecta tipo de licitação
- Rápido

**Fase 5 (Extração de campos):** LangExtract
- Schema-based
- Semântico
- Fácil iterar schemas

---

## Plano de Benchmark: Sprint de Testes (Open Source)

### O que testar - Fase 3 (Extração)

**Stack clássica (baseline):**
1. Tesseract (sozinho)
2. PyMuPDF (apenas PDFs com texto)
3. PyMuPDF + Tesseract (fallback clássico)
4. PyMuPDF + PaddleOCR (fallback moderno)

**Alternativas rápidas:**
5. pypdfium2 (ultra-rápido)
6. pdfplumber (tabelas)

**Novos players:**
7. Dedoc (completo)
8. SmolDocling (vision model compacto)
9. pymupdf4llm (markdown estruturado)
10. unstructured (chunks semânticos)
11. marker-pdf (high fidelity, mas lento)

**Total: 11 opções para testar**

---

### Cronograma Realista

| Ferramenta | Setup | Teste 30 docs | Total |
|-----------|-------|---------------|-------|
| Tesseract | 30min | 15min | 45min |
| PyMuPDF | 5min | 5min | 10min |
| PyMuPDF+Tes | 5min | 20min | 25min |
| PyMuPDF+PO | 15min | 10min | 25min |
| pypdfium2 | 5min | 1min | 6min |
| pdfplumber | 5min | 10min | 15min |
| Dedoc | 10min | 10min | 20min |
| SmolDocling | 15min | 20min | 35min |
| pymupdf4llm | 5min | 10min | 15min |
| unstructured | 10min | 30min | 40min |
| marker-pdf | 20min* | 15min | 35min |
| **TOTAL** | **2.5h** | **2h** | **~4.5h** |

*marker-pdf: primeira vez baixa 1GB modelo

---

### Métricas a Medir

Para cada ferramenta, em cada documento:

```
VELOCIDADE
- Tempo por documento (segundos)
- Throughput (docs/segundo)
- Consumo memória RAM

QUALIDADE
- Caracteres extraídos vs. esperado
- OCR accuracy (se houver ground truth)
- Preservação de estrutura (tabelas, headings)
- Taxa de sucesso (sem erros)

ROBUSTEZ
- Falhas por tipo de erro
- Tipos de PDF que falham
- Edge cases detectados

RECURSOS
- Dependências do sistema
- Tamanho do modelo
- Complexidade de setup
```

---

### Script de Teste (Skeleton)

```python
import time
import json
from pathlib import Path

# Importar extractores
from extractors import (
    TesseractExtractor,
    PyMuPFExtractor,
    PyMuPDFTesseractExtractor,
    PyMuPDFPaddleExtractor,
    pypdfium2Extractor,
    pdfplumberExtractor,
    DedocExtractor,
    SmolDoclingExtractor,
    pymupdf4llmExtractor,
    UnstructuredExtractor,
    MarkerPDFExtractor,
)

# Configurar teste
test_docs = list(Path("test_data/").glob("*.pdf"))[:30]
extractors = [
    ("Tesseract", TesseractExtractor()),
    ("PyMuPF", PyMuPFExtractor()),
    ("PyMuPDF+Tes", PyMuPDFTesseractExtractor()),
    ("PyMuPDF+PaddleOCR", PyMuPDFPaddleExtractor()),
    ("pypdfium2", pypdfium2Extractor()),
    ("pdfplumber", pdfplumberExtractor()),
    ("Dedoc", DedocExtractor()),
    ("SmolDocling", SmolDoclingExtractor()),
    ("pymupdf4llm", pymupdf4llmExtractor()),
    ("unstructured", UnstructuredExtractor()),
    ("marker-pdf", MarkerPDFExtractor()),
]

results = {}

# Executar testes
for name, extractor in extractors:
    print(f"\nTestando {name}...")
    results[name] = {
        "total_time": 0,
        "success_count": 0,
        "error_count": 0,
        "documents": []
    }
    
    for doc in test_docs:
        start = time.time()
        try:
            text = extractor.extract(doc)
            elapsed = time.time() - start
            
            results[name]["documents"].append({
                "file": doc.name,
                "time": elapsed,
                "status": "success",
                "text_length": len(text),
            })
            results[name]["success_count"] += 1
            results[name]["total_time"] += elapsed
            
        except Exception as e:
            results[name]["documents"].append({
                "file": doc.name,
                "status": "error",
                "error": str(e),
            })
            results[name]["error_count"] += 1

# Salvar resultados
with open("benchmark_results.json", "w") as f:
    json.dump(results, f, indent=2)

# Gerar summary
print("\n" + "="*60)
print("BENCHMARK SUMMARY")
print("="*60)

for name, data in results.items():
    avg_time = data["total_time"] / data["success_count"] if data["success_count"] > 0 else float('inf')
    success_rate = data["success_count"] / len(test_docs) * 100
    
    print(f"\n{name}:")
    print(f"  - Avg time: {avg_time:.3f}s/doc")
    print(f"  - Success rate: {success_rate:.1f}% ({data['success_count']}/{len(test_docs)})")
    print(f"  - Total time: {data['total_time']:.1f}s")
```

---

### Próximas Etapas do MVP

1. **Coletar dataset de teste**
   - 20-30 licitações reais variadas
   - Mix de: PDFs com texto, scaneados, com tabelas

2. **Implementar extractores wrapper**
   - Interface uniforme para cada ferramenta
   - Try/except consistent

3. **Rodar benchmark (4-5 horas)**
   - Coletar todos os dados
   - Gerar relatório

4. **Analisar resultados**
   - Tabular: tempo, sucesso, qualidade
   - Decidir: Top 2 ferramentas por fase

5. **Implementar Fase 3 com ferramenta vencedora**
   - Integrar no pipeline
   - Testes com Fase 4 e 5

Nenhuma ferramenta resolve tudo. O sucesso do Sherlock Holmes depende de:

1. **Extração de texto e estrutura robusta** (Fase 3)
   - Diferentes formatos de entrada
   - OCR de qualidade
   - Preservação de estrutura
   - Reconhecimento de tabelas

2. **Classificação inteligente** (Fase 4)
   - Identifica tipo de documento
   - Permite regras diferentes por tipo
   - Melhora precisão da Fase 5

3. **Extração semântica** (Fase 5)
   - Entende contexto ("valor" pode ser em reais, dólares, euros)
   - Lida com variações ("25 de dezembro" vs "25/12" vs "25-12-2025")
   - Extrai relações entre campos

Combinar ferramentas é a chave!

---

## Próximas Etapas

1. Confirmar escolha: Dedoc ou PyMuPDF + PaddleOCR
2. Estruturar o projeto com a ferramenta escolhida
3. Implementar Fase 3 (extração de texto)
4. Passar para Fase 4 (classificação)
5. Passar para Fase 5 (extração de campos)
