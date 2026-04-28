# Análise de Ferramentas para Extração de Texto

## Objetivo

Este documento é um levantamento técnico das ferramentas que podem ser úteis para extração de texto, OCR, parsing de documentos, análise de layout e extração semântica no projeto Sherlock Holmes.

Ele não define plano de execução, ordem de testes, amostras, métricas de benchmark ou decisões de rodada. Esses pontos pertencem ao documento de plano em `documentation/plans/ocr-execution-plan-v1.md`.

O papel deste arquivo é responder:

- quais ferramentas existem no radar
- em que categoria cada ferramenta se encaixa
- quais problemas cada uma resolve melhor
- quais limitações e riscos precisam ser considerados
- quais ferramentas parecem mais aderentes ao contexto do projeto

## Critérios de Comparação

As ferramentas são avaliadas de forma qualitativa pelos critérios abaixo.

### Cobertura de entrada

- imagens escaneadas
- PDFs com camada de texto
- PDFs escaneados
- documentos Office
- HTML, e-mail e arquivos simples
- imagens isoladas, screenshots e páginas digitalizadas

### Tipo de extração

- texto puro
- texto com bounding boxes
- blocos, linhas e palavras
- tabelas
- layout e ordem de leitura
- Markdown estruturado
- JSON estruturado
- campos semânticos

### Robustez operacional

- facilidade de instalação
- dependências de sistema
- suporte a CPU/GPU
- consumo de memória
- maturidade do projeto
- manutenção e comunidade
- clareza de licença

### Adequação ao Sherlock Holmes

- documentos administrativos e licitatórios
- documentos em português
- necessidade de preservar ordem de leitura
- presença de tabelas, formulários e anexos
- uso local versus cloud
- custo operacional
- privacidade dos documentos

## Mapa Geral de Categorias

| Categoria | Ferramentas | Papel principal |
|---|---|---|
| OCR local clássico | `Tesseract`, `pytesseract`, `OCRmyPDF` | OCR maduro, baseline e PDFs pesquisáveis |
| OCR local deep learning | `PaddleOCR`, `docTR`, `EasyOCR`, `Keras-OCR` | OCR em imagens com detecção + reconhecimento |
| OCR histórico/especializado | `Kraken`, `OCRopus` | documentos históricos, manuscritos ou tipografia irregular |
| OCR híbrido/transformer | `TrOCR` | reconhecimento de texto em regiões já detectadas |
| Modelos multimodais emergentes | `DeepSeek-OCR`, `Dots.OCR`, `OLMo-OCR 2`, `Qwen3-VL`, `Donut`, `SmolDocling` | OCR + layout + document understanding |
| Parsers e conversores de documentos | `Dedoc`, `Docling`, `Markitdown`, `MinerU`, `unstructured`, `marker-pdf`, `pymupdf4llm`, `textract` | conversão para texto, Markdown ou estrutura |
| Extração PDF com texto | `PyMuPDF`, `pypdfium2`, `pypdf`, `pdfplumber`, `pdfminer.six`, `PyPDF2` | extrair texto de PDFs que já têm camada textual |
| Pré-processamento e suporte | `Pillow`, `OpenCV`, `pdf2image`, `LibreOffice` | preparar imagens, converter formatos e melhorar entrada |
| Cloud/comercial | `Amazon Textract`, `Azure AI Document Intelligence`, `Google Cloud Vision`, `ABBYY`, `Nanonets`, `Rossum.AI` | OCR gerenciado, formulários, tabelas e IDP |
| Extração semântica com LLM | `LangExtract`, `LangChain`, chamadas diretas a LLMs | transformar texto extraído em campos estruturados |
| Baixa aderência ao stack atual | `PyOCR`, `IronOCR`, `SwiftOCR` | wrappers ou ferramentas úteis apenas em contextos específicos |

## Resumo de Aderência

| Ferramenta | Categoria | Relevância potencial | Observação curta |
|---|---|---:|---|
| `Tesseract` | OCR clássico | Alta | baseline maduro e barato |
| `PaddleOCR` | OCR deep learning | Alta | forte para OCR local moderno |
| `docTR` | OCR deep learning estruturado | Alta | saída em blocos, linhas e palavras |
| `EasyOCR` | OCR deep learning | Média/alta | bom candidato local alternativo |
| `PyMuPDF` | PDF textual | Alta | muito útil para PDFs com camada de texto |
| `pdfplumber` | PDF textual/layout | Média/alta | forte para tabelas e coordenadas |
| `Dedoc` | parser universal | Média | bom conceito de pipeline unificado |
| `Docling` | parser/conversor | Média/alta | promissor para Markdown/estrutura |
| `SmolDocling` | multimodal/document conversion | Média/alta | forte em estrutura, tabelas e DocTags |
| `marker-pdf` | PDF para Markdown com visão | Média | alta fidelidade, mas pesado e licença exige atenção |
| `unstructured` | particionamento semântico | Média | útil para RAG/chunks, mais lento |
| `Amazon Textract` | cloud/comercial | Média/alta | forte para formulários e tabelas |
| `Azure AI Document Intelligence` | cloud/comercial | Média/alta | forte em documentos estruturados |
| `Google Cloud Vision` | cloud/comercial | Média | OCR geral gerenciado |
| `ABBYY` | comercial | Média | referência comercial madura |
| `Nanonets` | comercial/IDP | Média | automação documental customizável |
| `Rossum.AI` | comercial/IDP | Média | processamento inteligente de documentos |
| `DeepSeek-OCR` | multimodal emergente | Experimental | velocidade em GPU a validar |
| `Dots.OCR` | multimodal emergente | Experimental | compacto, estrutura a validar |
| `OLMo-OCR 2` | multimodal/PDF Markdown | Experimental | promissor para PDFs complexos |
| `Qwen3-VL` | vision-language | Experimental | OCR + raciocínio visual |
| `TrOCR` | reconhecimento transformer | Experimental | requer detecção/crops externos |
| `Keras-OCR` | OCR deep learning | Baixa | menos atraente para pipeline novo |
| `Kraken` | OCR histórico | Específica | útil se houver manuscritos/documentos antigos |
| `OCRopus` | OCR histórico/acadêmico | Baixa | mais legado/pesquisa |
| `PyOCR` | wrapper OCR | Baixa | interface, não motor OCR |
| `IronOCR` | comercial .NET | Baixa | desalinhado do stack Python |
| `SwiftOCR` | mobile/iOS | Baixa | útil apenas para frente mobile |

## OCR Local Clássico e Deep Learning

### Tesseract / pytesseract

Tipo:
- OCR clássico open source
- motor nativo com wrapper Python via `pytesseract`

Melhor uso:
- baseline local
- imagens com texto impresso razoavelmente limpo
- OCR barato e sem dependência de cloud
- extração simples de texto, palavras, confiança e bounding boxes

Saída:
- texto puro
- dados por palavra via `image_to_data`
- bounding boxes por caractere via `image_to_boxes`

Pontos fortes:
- maduro e amplamente usado
- suporte a muitos idiomas
- baixo custo operacional
- bom para comparação com ferramentas modernas

Limitações:
- costuma sofrer mais em layouts complexos, fundos ruins, ruído e documentos visualmente ricos
- instalação pode depender de binários do sistema
- não oferece compreensão semântica nem estrutura rica por padrão

Relevância para o Sherlock Holmes:
- alta como ferramenta de referência técnica
- menos indicada como solução final única se os documentos tiverem muito layout, tabela ou baixa qualidade visual

### PaddleOCR

Tipo:
- OCR deep learning open source
- usa ecossistema PaddlePaddle

Melhor uso:
- OCR local moderno
- documentos escaneados
- imagens com layouts mais variados
- cenários em que velocidade e qualidade importam

Saída:
- texto
- bounding boxes
- confiança por trecho

Pontos fortes:
- boa relação entre qualidade e velocidade
- suporte a múltiplos idiomas
- suporte a GPU
- modelos pré-treinados

Limitações:
- dependências mais pesadas que Tesseract
- ecossistema e documentação podem exigir mais cuidado
- saída estrutural ainda pode precisar de pós-processamento para tabelas e campos

Relevância para o Sherlock Holmes:
- alta para OCR local em documentos escaneados
- ferramenta central no radar de OCR open source moderno

### docTR

Tipo:
- framework OCR deep learning da Mindee
- detecção + reconhecimento
- também possui componentes relacionados a KIE, dependendo do uso

Melhor uso:
- OCR em imagens e PDFs
- análise com blocos, linhas e palavras
- casos em que a estrutura da página importa mais que texto bruto

Saída:
- estrutura em páginas, blocos, linhas e palavras
- bounding boxes
- valores textuais

Pontos fortes:
- saída mais organizada que OCR de texto bruto
- usa modelos modernos de detecção e reconhecimento
- bom encaixe para avaliação de ordem de leitura e layout

Limitações:
- ambiente mais pesado que Tesseract
- pode exigir PyTorch ou TensorFlow, conforme instalação
- não substitui uma etapa semântica de extração de campos

Relevância para o Sherlock Holmes:
- alta quando a estrutura do OCR for importante
- bom contraponto a `PaddleOCR` na avaliação de OCR local

### EasyOCR

Tipo:
- OCR deep learning open source
- usa CRAFT para detecção e CRNN para reconhecimento

Melhor uso:
- OCR local alternativo
- múltiplos idiomas
- imagens menos padronizadas
- casos em que bounding boxes e confiança por trecho sejam úteis

Saída:
- texto detectado
- bounding boxes
- confiança

Pontos fortes:
- simples de usar
- bom suporte multilíngue
- pode superar Tesseract em imagens menos limpas
- usa PyTorch e pode se beneficiar de GPU

Limitações:
- download de modelos na primeira execução
- consumo de memória maior que Tesseract
- pode ser mais lento dependendo do ambiente

Relevância para o Sherlock Holmes:
- média/alta como alternativa local
- especialmente interessante se o dataset real mostrar variação visual alta ou necessidade multilíngue

### Keras-OCR

Tipo:
- OCR deep learning baseado em Keras/TensorFlow
- usa CRAFT + CRNN

Melhor uso:
- estudo técnico
- comparação histórica com EasyOCR
- experimentos pontuais em inglês

Saída:
- palavras detectadas
- bounding boxes

Pontos fortes:
- pipeline relativamente claro
- pode produzir bons resultados em imagens simples

Limitações:
- menor aderência para projetos novos
- suporte linguístico mais limitado
- comunidade e manutenção menos atraentes que alternativas atuais

Relevância para o Sherlock Holmes:
- baixa
- deve permanecer como referência, não como prioridade prática

### TrOCR

Tipo:
- reconhecedor de texto baseado em transformers
- disponível via Hugging Face

Melhor uso:
- reconhecer texto em regiões já recortadas
- comparar qualidade de reconhecimento puro
- combinar com outro detector de texto

Saída:
- texto gerado a partir de imagem/crop

Pontos fortes:
- arquitetura moderna encoder-decoder
- bom potencial em reconhecimento quando a região de texto já está bem isolada

Limitações:
- não é OCR completo para páginas inteiras
- exige etapa anterior de detecção/segmentação
- pode adicionar complexidade sem resolver layout end-to-end

Relevância para o Sherlock Holmes:
- experimental
- mais útil em arquitetura híbrida do que como ferramenta direta de OCR documental

### Kraken

Tipo:
- OCR open source com foco em documentos históricos e manuscritos

Melhor uso:
- documentos antigos
- tipografias incomuns
- manuscritos
- corpora que permitam treinamento especializado

Pontos fortes:
- mais alinhado a digitalização histórica que OCRs generalistas
- pode ser relevante em acervos com material degradado ou não padronizado

Limitações:
- menos aderente a documentos administrativos modernos
- pode exigir treinamento e curadoria de dataset

Relevância para o Sherlock Holmes:
- específica
- vale considerar apenas se aparecerem documentos históricos, manuscritos ou tipografias muito fora do padrão

### OCRopus

Tipo:
- OCR open source histórico/acadêmico

Melhor uso:
- pesquisa
- digitalização histórica
- experimentos com pipelines antigos/customizados

Pontos fortes:
- relevância histórica na área de OCR

Limitações:
- menos prioritário que ferramentas modernas
- menor aderência para um pipeline operacional novo

Relevância para o Sherlock Holmes:
- baixa

## Modelos Multimodais e Document Understanding

### DeepSeek-OCR

Tipo:
- modelo OCR multimodal/open source citado como voltado a imagens e PDFs

Melhor uso:
- OCR com GPU
- cenários que exigem throughput alto
- experimentos com serving via `vLLM` ou `Transformers`

Saída:
- texto gerado a partir de imagem/documento

Pontos fortes:
- promete velocidade alta em hardware forte
- representa a linha recente de OCR com modelos multimodais

Limitações:
- requisitos de GPU e VRAM precisam ser confirmados
- maturidade, licença e custo operacional precisam de validação em fontes primárias
- pode ser excessivo para OCR simples

Relevância para o Sherlock Holmes:
- experimental
- candidato para estudo futuro de OCR multimodal local

### Dots.OCR

Tipo:
- modelo OCR open source compacto citado como capaz de lidar com texto, tabelas e layout

Melhor uso:
- OCR local com estrutura
- experimentos com modelos multimodais menores
- comparação com `PaddleOCR`, `docTR` e `SmolDocling`

Pontos fortes:
- proposta de ser mais leve que modelos multimodais grandes
- potencial para texto, tabelas e layout em uma abordagem unificada

Limitações:
- precisa de validação independente
- requisitos de GPU, licença, idiomas e formato de saída precisam ser confirmados

Relevância para o Sherlock Holmes:
- experimental

### OLMo-OCR 2

Tipo:
- ferramenta/modelo citada para OCR e conversão de PDFs para Markdown estruturado

Melhor uso:
- PDFs técnicos ou acadêmicos
- documentos com tabelas, equações, cabeçalhos e múltiplos blocos
- geração de Markdown com ordem de leitura mais limpa

Pontos fortes:
- proposta alinhada a documentos complexos e leitura estruturada
- pode competir mais com conversores/document parsers do que com OCR puro

Limitações:
- requisitos de hardware podem ser altos
- informações precisam ser validadas com documentação oficial
- aderência a documentos administrativos brasileiros ainda é incerta

Relevância para o Sherlock Holmes:
- experimental, com interesse médio/alto para PDFs complexos

### Qwen3-VL

Tipo:
- modelo vision-language multimodal
- não é apenas OCR

Melhor uso:
- OCR combinado com compreensão visual
- perguntas e respostas sobre documentos
- screenshots, interfaces e documentos multilíngues
- cenários com raciocínio espacial

Pontos fortes:
- pode entender texto, layout e contexto visual em uma mesma interface
- útil para document understanding, não só transcrição

Limitações:
- pode ser pesado e caro localmente
- requer avaliação cuidadosa de licença, VRAM, latência e privacidade
- pode ser mais amplo do que o necessário para extração textual inicial

Relevância para o Sherlock Holmes:
- experimental
- mais adequado a uma camada futura de compreensão visual/semântica

### Donut

Tipo:
- modelo OCR-free de document understanding
- desenvolvido pela NAVER Clova AI

Melhor uso:
- classificação e extração end-to-end a partir de imagens de documentos
- formulários e documentos visualmente complexos
- experimentos sem pipeline OCR tradicional

Saída:
- texto/estrutura gerada pelo modelo, dependendo da tarefa

Pontos fortes:
- reduz dependência de OCR separado
- une visão e extração estruturada
- relevante para documentos escaneados complexos

Limitações:
- fine-tuning pode ser necessário
- previsibilidade operacional menor que pipelines modulares
- custo computacional maior que OCR clássico

Relevância para o Sherlock Holmes:
- experimental
- útil como alternativa de document understanding, não como substituto imediato de OCR simples

### LayoutLM / LayoutLMv3

Tipo:
- modelos de document understanding que combinam texto, layout e imagem

Melhor uso:
- classificação de documentos
- extração de entidades/campos com layout
- documentos administrativos com estrutura recorrente

Entrada típica:
- texto já extraído
- bounding boxes
- imagem ou sinais visuais, conforme modelo

Pontos fortes:
- usa posição espacial como sinal importante
- bom para formulários, recibos e documentos com layout previsível

Limitações:
- requer OCR ou texto com coordenadas
- geralmente exige dataset rotulado e fine-tuning
- não é OCR por si só

Relevância para o Sherlock Holmes:
- média para fases futuras de classificação e extração supervisionada

### SmolDocling

Tipo:
- modelo vision compacto para document conversion
- associado ao ecossistema Docling/DocTags

Melhor uso:
- converter imagens ou páginas em representação estruturada
- preservar layout, ordem de leitura, tabelas e elementos visuais
- gerar Markdown/HTML por meio de DocTags

Saída:
- DocTags
- Markdown
- HTML, dependendo do fluxo

Pontos fortes:
- proposta compacta em comparação com modelos vision maiores
- foco em estrutura e layout
- interessante para tabelas, equações e documentos ricos

Limitações:
- ainda requer modelo e ambiente ML
- maturidade e desempenho devem ser testados no dataset real
- pode ser mais complexo que OCR tradicional

Relevância para o Sherlock Holmes:
- média/alta como ferramenta de document conversion estruturada

### MinerU

Tipo:
- parser moderno de documentos para Markdown/JSON

Melhor uso:
- preparar documentos para LLMs e RAG
- preservar ordem de leitura
- remover ruído estrutural como cabeçalhos, rodapés e numeração

Saída:
- Markdown
- JSON

Pontos fortes:
- alinhado a pipelines LLM-first
- pode produzir texto mais limpo que extração PDF simples

Limitações:
- ecossistema menos consolidado que bibliotecas mais antigas
- precisa de validação com documentos licitatórios brasileiros

Relevância para o Sherlock Holmes:
- média como parser/conversor futuro

## Parsers e Conversores Multi-formato

### Dedoc

Tipo:
- sistema universal de conversão e análise de documentos

Entradas:
- PDF
- DOCX, XLSX, PPTX, ODT
- HTML, EML, MHTML
- TXT, CSV, JSON
- imagens e PDFs escaneados
- arquivos compactados

Saída:
- texto
- estrutura lógica
- tabelas
- metadados
- formatação

Pontos fortes:
- tenta unificar múltiplos formatos
- possui fallback de OCR com Tesseract para imagens/PDFs escaneados
- pode detectar estrutura, tabelas e metadados

Limitações:
- pode ser pesado para casos simples
- qualidade de OCR depende de Tesseract quando usado como fallback
- precisa ser avaliado em instalação, compatibilidade e qualidade de saída

Relevância para o Sherlock Holmes:
- média
- interessante se a variedade de formatos for mais importante que controle fino por ferramenta

### Docling

Tipo:
- biblioteca de conversão e extração de documentos
- desenvolvida pela IBM

Entradas:
- PDF
- DOCX
- XLSX
- HTML
- outros formatos suportados pelo projeto

Saída:
- Markdown
- JSON
- HTML

Pontos fortes:
- foco em estrutura e conversão
- boa aderência a pipelines que precisam de Markdown limpo
- bom radar para PDFs e documentos Office

Limitações:
- em algumas referências, ainda precisa de exploração para PDFs com tabelas complexas
- não deve ser tratado como OCR puro

Relevância para o Sherlock Holmes:
- média/alta para conversão estruturada

### Markitdown

Tipo:
- biblioteca da Microsoft para converter múltiplos formatos em Markdown

Melhor uso:
- conversão simples para Markdown
- documentos Office
- fluxos em que Markdown seja a saída padrão

Pontos fortes:
- simples de usar
- boa ergonomia para conversão geral

Limitações:
- não é motor OCR
- pode falhar ou gerar saída limitada em PDFs complexos, tabelas e imagens

Relevância para o Sherlock Holmes:
- média/baixa
- útil como referência de conversão, não como solução de OCR

### pymupdf4llm

Tipo:
- conversor de PDF para Markdown baseado em PyMuPDF

Melhor uso:
- PDFs com camada textual
- preparação de conteúdo para LLMs/RAG
- preservar alguma estrutura em Markdown

Pontos fortes:
- saída Markdown limpa
- boa velocidade
- baseado em uma biblioteca PDF madura

Limitações:
- licença AGPL exige atenção para uso comercial
- pode sofrer em PDFs escaneados ou layouts muito complexos

Relevância para o Sherlock Holmes:
- média

### unstructured

Tipo:
- biblioteca de particionamento semântico de documentos

Melhor uso:
- RAG
- geração de chunks por tipo de elemento
- classificação de blocos como título, texto narrativo, tabela etc.

Pontos fortes:
- abstração semântica útil para pipelines LLM
- suporta múltiplos formatos
- bom para organizar documentos em blocos

Limitações:
- dependências podem ser pesadas
- performance tende a ser inferior a extratores simples
- qualidade varia por tipo de documento

Relevância para o Sherlock Holmes:
- média para fases de estruturação e RAG

### marker-pdf

Tipo:
- conversor PDF para Markdown com modelos vision

Melhor uso:
- alta fidelidade de layout
- PDFs complexos
- documentos em que estrutura visual seja essencial

Pontos fortes:
- alta qualidade em layout e Markdown
- bom para documentos ricos em imagens/tabelas

Limitações:
- muito mais pesado que alternativas simples
- modelos grandes podem exigir download e hardware adequado
- licença GPL-3.0 exige atenção

Relevância para o Sherlock Holmes:
- média como referência de alta fidelidade

### textract

Tipo:
- extrator multi-formato com fallback OCR

Melhor uso:
- extração uniforme de texto em vários formatos
- protótipos simples

Pontos fortes:
- interface simples
- suporta vários formatos
- pode usar Tesseract como dependência

Limitações:
- menos controle fino
- depende de binários do sistema
- menor precisão em documentos complexos

Relevância para o Sherlock Holmes:
- baixa/média

### OCRmyPDF

Tipo:
- ferramenta para adicionar camada OCR pesquisável a PDFs escaneados

Melhor uso:
- transformar PDFs escaneados em PDFs pesquisáveis
- aplicar deskew e rotação automática
- preservar arquivo PDF como artefato

Pontos fortes:
- workflow maduro para PDFs digitalizados
- usa Tesseract por baixo
- muito útil como etapa de normalização

Limitações:
- não resolve extração semântica
- não é ideal para comparação de OCR bruto em imagens isoladas
- depende de ferramentas do sistema

Relevância para o Sherlock Holmes:
- média se o pipeline precisar lidar com PDFs escaneados reais

### LibreOffice / soffice

Tipo:
- suíte de conversão de documentos

Melhor uso:
- converter DOCX, XLSX, PPT e ODT para PDF ou texto
- preservar layout antes de extração

Pontos fortes:
- suporta muitos formatos
- útil em modo headless
- maduro para conversão Office

Limitações:
- dependência pesada de sistema
- startup lento
- pode exigir ajustes em servidor

Relevância para o Sherlock Holmes:
- média como ferramenta auxiliar de conversão

## Extração de PDF com Camada Textual

### PyMuPDF

Tipo:
- biblioteca Python para leitura e manipulação de PDF

Melhor uso:
- PDFs com texto copiável
- extração rápida de texto
- acesso a páginas, coordenadas, imagens e metadados

Pontos fortes:
- rápido
- maduro
- flexível
- bom para detectar se um PDF já tem texto

Limitações:
- não faz OCR sozinho
- precisa de fallback para PDFs escaneados

Relevância para o Sherlock Holmes:
- alta para PDFs com camada textual e detecção de fallback

### pypdfium2

Tipo:
- binding Python para PDFium

Melhor uso:
- extração muito rápida de texto simples
- alto volume de PDFs com camada textual

Pontos fortes:
- velocidade
- simplicidade

Limitações:
- pouca estrutura
- não é focado em tabelas
- não resolve OCR

Relevância para o Sherlock Holmes:
- média como baseline rápido para PDFs textuais

### pypdf

Tipo:
- biblioteca Python pura para leitura/manipulação de PDF

Melhor uso:
- ambientes onde dependências C são indesejadas
- extração básica de texto
- manipulação simples de PDFs

Pontos fortes:
- puro Python
- confiável para casos simples
- bom em ambientes serverless/containers restritos

Limitações:
- menos preciso e menos rico que alternativas com análise de layout
- pode ter problemas de espaçamento

Relevância para o Sherlock Holmes:
- média/baixa

### pdfplumber

Tipo:
- biblioteca para extração de texto, tabelas e coordenadas em PDF

Melhor uso:
- PDFs com tabelas
- inspeção de layout
- extração com bounding boxes

Pontos fortes:
- excelente para tabelas em PDFs textuais
- controle fino de layout
- útil para debugging visual

Limitações:
- não faz OCR
- requer ajuste por documento em casos complexos

Relevância para o Sherlock Holmes:
- média/alta para documentos licitatórios com tabelas textuais

### pdfminer.six

Tipo:
- extrator clássico de texto e layout em PDF

Melhor uso:
- extração textual com análise de layout
- casos que exigem controle sobre parsing PDF

Pontos fortes:
- maduro
- muito usado historicamente
- base para outras ferramentas

Limitações:
- pode ser mais lento
- parsing pode ser frágil em PDFs complexos

Relevância para o Sherlock Holmes:
- média como componente indireto ou fallback

### PyPDF2

Tipo:
- biblioteca PDF antiga, sucedida na prática por `pypdf`

Melhor uso:
- manutenção de código legado
- manipulações simples de PDF

Pontos fortes:
- conhecida
- sem dependências C

Limitações:
- menos recomendada para novos projetos que `pypdf`

Relevância para o Sherlock Holmes:
- baixa

## Pré-processamento e Suporte de Imagem

### Pillow

Tipo:
- biblioteca Python para manipulação básica de imagens

Melhor uso:
- abrir, converter, redimensionar e salvar imagens
- grayscale
- ajuste simples de contraste, brilho e rotação

Pontos fortes:
- simples
- leve
- muito usada

Limitações:
- limitada para visão computacional avançada
- insuficiente sozinha para deskew, denoising complexo e análise de layout

Relevância para o Sherlock Holmes:
- alta como dependência auxiliar simples

### OpenCV

Tipo:
- biblioteca de visão computacional

Melhor uso:
- binarização
- deskew
- denoising
- detecção de bordas e contornos
- pré-processamento reprodutível de OCR

Pontos fortes:
- muito poderoso
- padrão de mercado
- cobre operações avançadas de imagem

Limitações:
- maior complexidade
- decisões de pré-processamento podem melhorar ou piorar OCR conforme o documento

Relevância para o Sherlock Holmes:
- alta como ferramenta de pré-processamento

### pdf2image

Tipo:
- conversor de PDF para imagens

Melhor uso:
- rasterizar PDFs para OCR
- controlar DPI antes de aplicar OCR em páginas

Pontos fortes:
- simples e confiável
- muito usado em pipelines OCR

Limitações:
- depende de Poppler/Ghostscript, conforme ambiente
- pode gerar alto consumo de memória e arquivos intermediários

Relevância para o Sherlock Holmes:
- média/alta quando PDFs escaneados precisarem virar imagens

## Cloud, APIs Comerciais e IDP

### Amazon Textract

Tipo:
- serviço cloud AWS para OCR, tabelas e formulários

Melhor uso:
- formulários
- tabelas
- documentos semi-estruturados
- workloads integrados à AWS

Pontos fortes:
- forte em tabelas e key-value pairs
- serviço gerenciado
- boa integração com ecossistema AWS

Limitações:
- custo por uso
- envio de documentos para cloud
- dependência de provedor

Relevância para o Sherlock Holmes:
- média/alta como referência cloud para documentos estruturados

### Azure AI Document Intelligence

Também conhecido historicamente como:
- Azure Form Recognizer

Tipo:
- serviço cloud Microsoft para OCR e análise documental

Melhor uso:
- formulários
- invoices
- recibos
- documentos estruturados
- cenários corporativos com requisitos Microsoft/compliance

Pontos fortes:
- forte para key-value pairs e tabelas
- modelos pré-construídos e customizáveis
- boa integração com Azure

Limitações:
- custo por uso
- dependência de cloud
- privacidade precisa ser avaliada

Relevância para o Sherlock Holmes:
- média/alta como alternativa cloud/comercial

### Google Cloud Vision

Tipo:
- serviço cloud de visão computacional e OCR geral

Melhor uso:
- OCR geral
- imagens variadas
- integração com Google Cloud

Pontos fortes:
- serviço maduro
- bom OCR geral
- APIs simples

Limitações:
- menos especializado em formulários/tabelas que Textract ou Azure AI Document Intelligence
- custo e dependência de cloud

Relevância para o Sherlock Holmes:
- média

### ABBYY FineReader / ABBYY Vantage

Tipo:
- OCR e Intelligent Document Processing comercial

Melhor uso:
- OCR corporativo
- PDFs escaneados
- documentos de alta exigência de qualidade
- fluxos empresariais

Pontos fortes:
- referência histórica em OCR comercial
- maturidade de mercado
- boa opção de benchmark comercial se houver acesso/licença

Limitações:
- custo e licenciamento
- menor transparência que open source

Relevância para o Sherlock Holmes:
- média como referência comercial

### Nanonets OCR

Tipo:
- plataforma comercial/cloud de OCR e automação documental

Melhor uso:
- invoices
- formulários
- workflows customizados
- documentos de negócio com revisão e automação

Pontos fortes:
- customização por caso de uso
- foco em automação documental

Limitações:
- custo
- dependência de plataforma externa
- precisa de avaliação de privacidade e integração

Relevância para o Sherlock Holmes:
- média como IDP comercial no radar

### Rossum.AI

Tipo:
- plataforma comercial de Intelligent Document Processing

Melhor uso:
- documentos estruturados e semi-estruturados
- invoices
- formulários corporativos
- workflows com revisão humana

Pontos fortes:
- foco operacional em processamento documental
- bom radar para automação empresarial

Limitações:
- custo
- dependência de plataforma
- pode ser mais voltado a workflows corporativos do que a experimentação técnica local

Relevância para o Sherlock Holmes:
- média como referência IDP

## Extração Semântica com LLM

### LangExtract

Tipo:
- biblioteca para extração estruturada com LLMs

Melhor uso:
- transformar texto já extraído em campos estruturados
- aplicar schemas
- lidar com variações de linguagem

Pontos fortes:
- saída estruturada
- abordagem semântica
- pode usar modelos cloud ou locais, conforme configuração

Limitações:
- não substitui OCR
- depende da qualidade do texto de entrada
- custo, latência e privacidade variam conforme o modelo usado

Relevância para o Sherlock Holmes:
- média/alta para etapas posteriores à extração textual

### LangChain / chamadas diretas a LLMs

Tipo:
- frameworks ou integrações diretas para orquestrar LLMs

Melhor uso:
- classificação
- extração de campos
- normalização de texto
- geração de JSON a partir do texto OCR

Pontos fortes:
- flexibilidade
- integração com múltiplos modelos
- pode combinar regras, chunks e validações

Limitações:
- não resolve OCR
- exige controle de custo, qualidade e alucinação
- precisa de validação estruturada da saída

Relevância para o Sherlock Holmes:
- alta em fases semânticas, não na extração visual inicial

## Ferramentas de Baixa Aderência ou Uso Específico

### PyOCR

Tipo:
- wrapper/interface Python para motores OCR

Uso possível:
- padronizar chamadas para ferramentas como Tesseract

Limitações:
- não é um motor OCR competitivo por si só
- adiciona pouco se a integração direta for simples

Relevância:
- baixa

### IronOCR

Tipo:
- biblioteca comercial de OCR com foco forte em .NET

Uso possível:
- projetos C#/.NET
- ambientes corporativos Windows

Limitações:
- desalinhado ao stack Python inicialmente previsto
- comercial

Relevância:
- baixa

### SwiftOCR

Tipo:
- OCR voltado ao ecossistema Apple/mobile

Uso possível:
- apps iOS/macOS

Limitações:
- pouco aderente a backend de processamento documental

Relevância:
- baixa no escopo atual

## Comparações por Cenário

### Imagens escaneadas

Ferramentas mais relevantes:
- `PaddleOCR`
- `docTR`
- `EasyOCR`
- `Tesseract`

Observação:
- `Tesseract` é bom baseline
- `PaddleOCR` e `docTR` tendem a ser mais interessantes quando o layout ou a qualidade da imagem varia
- `EasyOCR` é boa alternativa local, especialmente com múltiplos idiomas

### PDFs com camada textual

Ferramentas mais relevantes:
- `PyMuPDF`
- `pypdfium2`
- `pypdf`
- `pdfplumber`
- `pdfminer.six`

Observação:
- OCR não deve ser a primeira opção se o PDF já possui texto copiável
- `pdfplumber` ganha relevância quando tabelas e coordenadas importam

### PDFs escaneados

Ferramentas mais relevantes:
- `OCRmyPDF`
- `pdf2image` + OCR local
- `PaddleOCR`
- `docTR`
- `Tesseract`

Observação:
- uma etapa de rasterização ou criação de camada OCR pesquisável pode ser necessária
- pré-processamento com `OpenCV` pode melhorar ou piorar resultados, então precisa ser medido

### Layout, tabelas e Markdown estruturado

Ferramentas mais relevantes:
- `Docling`
- `SmolDocling`
- `marker-pdf`
- `pymupdf4llm`
- `unstructured`
- `pdfplumber`
- `MinerU`
- `OLMo-OCR 2`

Observação:
- estas ferramentas competem mais em estrutura/ordem de leitura do que em OCR puro
- tabelas exigem avaliação qualitativa, porque mais texto extraído não significa tabela corretamente entendida

### Documentos estruturados e formulários em cloud

Ferramentas mais relevantes:
- `Amazon Textract`
- `Azure AI Document Intelligence`
- `ABBYY`
- `Nanonets OCR`
- `Rossum.AI`
- `Google Cloud Vision`

Observação:
- cloud pode entregar melhor qualidade operacional, mas traz custo, privacidade e dependência externa
- `Google Cloud Vision` é mais OCR geral; `Textract`, `Azure`, `ABBYY`, `Nanonets` e `Rossum` tendem a ser mais documentais/IDP

### Documentos históricos, manuscritos ou tipografia incomum

Ferramentas mais relevantes:
- `Kraken`
- `OCRopus`

Observação:
- só devem ganhar peso se o dataset real tiver esse perfil

### OCR multimodal e document understanding experimental

Ferramentas mais relevantes:
- `DeepSeek-OCR`
- `Dots.OCR`
- `OLMo-OCR 2`
- `Qwen3-VL`
- `Donut`
- `SmolDocling`

Observação:
- exigem validação de licença, hardware e maturidade
- podem ser muito promissoras, mas não devem ser confundidas com OCR local simples

## Riscos e Perguntas em Aberto

- Qual ferramenta lida melhor com português em documentos administrativos brasileiros?
- Quais ferramentas preservam melhor ordem de leitura em documentos com múltiplas colunas?
- Qual ferramenta mantém tabelas em formato realmente utilizável?
- Qual o custo de hardware para modelos multimodais locais?
- Quais licenças permitem uso comercial ou operacional?
- Em quais casos cloud compensa frente a execução local?
- Qual saída é mais útil para fases posteriores: texto puro, Markdown, JSON, bounding boxes ou DocTags?
- Quais ferramentas têm instalação viável em Windows e em ambiente de produção futuro?

## Fontes e Artigos Consultados

### Levantamento inicial do projeto

Contribuição:
- listou ferramentas gerais de OCR, parsing PDF, conversão, pré-processamento e extração com LLM
- trouxe comparações iniciais entre `Dedoc`, `Docling`, `Markitdown`, `PyMuPDF`, `PaddleOCR`, `Tesseract`, `SmolDocling`, `unstructured`, `marker-pdf` e outras

### Artigo: OCR - Extracting Value from Unstructured Data

Contribuição:
- reforçou o papel do OCR na transformação de dados não estruturados em texto utilizável
- destacou `Tesseract`, `EasyOCR`, `Keras-OCR` e ferramentas cloud como opções comuns
- reforçou a importância de confiança, bounding boxes e pós-processamento

### Artigo: Markitdown vs Docling

Contribuição:
- destacou diferenças entre ferramentas de conversão para Markdown/estrutura
- sugeriu que `Docling` pode ser melhor em alguns casos de Excel/fórmulas
- indicou limitações de ambas em PDFs complexos com tabelas/imagens

### Artigo: The Ultimate Guide to Top OCR Solutions in 2025

Fonte:
- Mahernaija, publicado em 2025-01-20 e atualizado em 2025-01-22

Contribuição:
- reforçou critérios de escolha como acurácia, suporte a idiomas, customização, integração, custo e escala
- trouxe ao radar `Nanonets OCR`, `Rossum.AI`, `ABBYY`, `Kraken`, `OCRopus`, `PyOCR`, `IronOCR` e `SwiftOCR`
- reforçou ferramentas cloud como `Google Cloud Vision`, `Amazon Textract` e `Azure AI Document Intelligence`

### Artigo: Top 5 Python Libraries for Extracting Text from Images

Fonte:
- Eugenia Anello, Towards Data Science, publicado em 2023-07-25

Contribuição:
- comparou `pytesseract`, `EasyOCR`, `Keras-OCR`, `TrOCR` e `docTR`
- reforçou a diferença entre OCR completo e modelos apenas de reconhecimento
- adicionou `TrOCR` ao radar como reconhecedor transformer que precisa de detecção/crops externos

### Artigo: Top 4 Open-Source OCR Models

Fonte:
- Algo Insights, Coding Nexus, publicado em 2025-10-26

Contribuição:
- trouxe modelos recentes de OCR multimodal e vision-language ao radar
- adicionou `DeepSeek-OCR`, `OLMo-OCR 2`, `Qwen3-VL` e `Dots.OCR`
- reforçou a necessidade de tratar modelos emergentes como experimentais até validação com documentação oficial, requisitos de hardware e testes no dataset real

## Síntese

O radar atual cobre quatro famílias importantes:

- OCR local tradicional e deep learning para imagens escaneadas
- extração e parsing de PDFs com texto ou estrutura
- ferramentas cloud/comerciais para documentos estruturados
- modelos multimodais emergentes para OCR e document understanding

Nenhuma ferramenta resolve todo o problema sozinha. O caminho técnico mais realista tende a combinar extração textual, preservação de layout, pré-processamento, fallback e uma camada posterior de extração semântica.
