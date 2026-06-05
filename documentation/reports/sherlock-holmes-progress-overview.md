# Overview Didatico do Progresso do Sherlock Holmes

## 1. Ideia Central Atual

O Sherlock Holmes foi reposicionado.

Antes, o projeto parecia girar principalmente em torno de OCR. Agora, a direcao ficou mais clara:

```text
PNCP primeiro.
Documentos depois.
OCR apenas quando necessario.
Evidencia sempre.
```

Isso significa que o projeto deve funcionar como um pipeline tecnico e auditavel para:

- localizar contratos e licitacoes em fontes oficiais;
- comparar dados oficiais com fontes manuais;
- preservar evidencias;
- encontrar documentos oficiais relacionados;
- tentar extrair texto diretamente dos documentos;
- usar OCR apenas como fallback.

OCR continua importante, mas deixou de ser o centro. O centro agora e a validacao investigativa com rastreabilidade.

## 2. O Que Foi Feito Primeiro: Reposicionamento

Foi atualizado o overview principal:

```text
documentation/overview-sherlock-holmes.md
```

Ele passou a explicar:

- PNCP como fonte primaria;
- planilhas e fontes manuais como entrada de investigacao;
- documentos oficiais como evidencia complementar;
- OCR como fallback;
- tipos de origem e niveis de confianca;
- diferenca do Sherlock frente a projetos como Licinexus, LicitaNow, n8n-nodes-pncp-aec e DeOlho.

Tambem foi criado o relatorio de decisao:

```text
documentation/reports/sherlock-holmes-repositioning-decision.md
```

Esse relatorio registra oficialmente a mudanca de direcao do projeto.

## 3. Pesquisa em Projeto Similar: Licinexus MCP

O repositorio `licinexus-mcp` foi clonado localmente como referencia tecnica:

```text
C:\Users\thiag\Documents\projetos\licinexus-mcp
```

A analise mostrou que o Licinexus organiza bem o dominio PNCP em:

- adaptadores de API;
- tools de dominio;
- schemas;
- validadores de CNPJ, datas e identificadores;
- endpoints para contratos, licitacoes, atas, orgaos, fornecedores, PCA e BrasilAPI.

A partir disso, foi criado um plano local de referencia:

```text
documentation/projetos-similares/analise-licinexus-para-sherlock.md
```

Essa pasta esta ignorada pelo Git e serve como area de pesquisa.

## 4. Nova Camada PNCP: Contratos

Foi criada a primeira reestruturacao tecnica da camada PNCP.

Arquivos principais:

```text
src/sherlock_holmes/pncp/ids.py
src/sherlock_holmes/pncp/dates.py
src/sherlock_holmes/pncp/contratos.py
```

Esses arquivos trouxeram:

- normalizacao de CNPJ;
- parsing de `numeroControlePNCP`;
- validacao de datas PNCP;
- busca de contratos;
- detalhe de contrato;
- listagem de arquivos de contrato.

Plano:

```text
documentation/plans/pncp-refactor-execution-plan.md
```

Relatorio:

```text
documentation/reports/pncp-refactor-001.md
```

## 5. Smoke PNCP Melhorado

O script:

```text
scripts/run_pncp_api_smoke.py
```

foi melhorado para:

- consultar multiplas paginas com `--max-pages`;
- deduplicar candidatos por `numeroControlePNCP`;
- melhorar scoring usando valor e vigencia;
- encontrar melhor o contrato esperado da linha `67`.

Resultado importante:

```text
source_row=67
HTTP 200
totalRegistros=22
totalPaginas=3
top candidate=39485438000142-2-000018/2025
```

Esse foi um marco relevante porque mostrou que a busca paginada + scoring melhorado consegue reencontrar o contrato correto dentro do PNCP.

## 6. Nova Camada PNCP: Licitacoes e Compras

Depois dos contratos, foi adicionada a camada de compras/licitacoes.

Arquivo:

```text
src/sherlock_holmes/pncp/licitacoes.py
```

Funcoes principais:

- `search_licitacoes`;
- `get_licitacao`;
- `list_licitacao_itens`;
- `list_licitacao_arquivos`.

Essa camada permite buscar contratacoes no PNCP e acessar:

- detalhe da compra;
- itens;
- arquivos/anexos.

Plano:

```text
documentation/plans/pncp-licitacoes-execution-plan.md
```

Relatorio:

```text
documentation/reports/pncp-licitacoes-001.md
```

Validacao real usada:

```text
23274194000119-1-000191/2024
```

Resultado:

- detalhe retornado;
- 10 itens encontrados;
- 1 arquivo encontrado.

## 7. Nova Camada PNCP: Referencias de Documentos

Depois de encontrar arquivos no PNCP, foi criada uma camada para transformar esses arquivos em referencias auditaveis.

Arquivo:

```text
src/sherlock_holmes/pncp/arquivos.py
```

Foi criada a dataclass:

```text
PncpDocumentReference
```

Ela guarda:

- fonte;
- tipo de recurso;
- identificador do recurso;
- titulo;
- tipo de documento;
- sequencial;
- URL;
- URI;
- data de publicacao;
- payload bruto.

Isso e importante porque o projeto passa a tratar documentos oficiais como evidencias rastreaveis, nao apenas como links soltos.

Plano:

```text
documentation/plans/pncp-documents-execution-plan.md
```

Relatorio:

```text
documentation/reports/pncp-documents-001.md
```

Validacao real:

- uma referencia de `Edital` foi criada a partir do PNCP;
- a URL oficial foi preservada.

## 8. Download Controlado de Documentos

Depois da camada de referencias, foi implementado download explicito de documentos.

Importante:

```text
Nada baixa automaticamente.
```

O download so acontece quando a funcao e chamada de forma direta.

Funcoes novas:

- `safe_document_filename`;
- `download_document_reference`.

Dataclass nova:

```text
PncpDownloadedDocument
```

Ela registra:

- fonte;
- tipo de recurso;
- identificador;
- URL;
- caminho local;
- content type;
- bytes gravados;
- timestamp do download;
- referencia original.

Plano:

```text
documentation/plans/pncp-document-download-execution-plan.md
```

Relatorio:

```text
documentation/reports/pncp-document-download-001.md
```

Validacao real:

- documento baixado para `data/raw/pncp/documents/...`;
- `1040085` bytes gravados;
- PNCP retornou `application/octet-stream`;
- tipo real inferido por assinatura como `.zip`.

## 9. Como Esta a Estrutura PNCP Agora

A pasta PNCP agora tem esta forma:

```text
src/sherlock_holmes/pncp/
|-- __init__.py
|-- arquivos.py
|-- client.py
|-- contratos.py
|-- dates.py
|-- ids.py
`-- licitacoes.py
```

Papel de cada arquivo:

- `client.py`: base HTTP e funcoes antigas ainda usadas pelo Streamlit;
- `ids.py`: CNPJ e identificadores PNCP;
- `dates.py`: datas no formato PNCP;
- `contratos.py`: contratos e arquivos de contrato;
- `licitacoes.py`: compras/licitacoes, itens e arquivos;
- `arquivos.py`: referencias e download controlado de documentos;
- `__init__.py`: exports publicos da camada PNCP.

## 10. O Que Ainda Nao Foi Feito

Ainda nao foi implementado:

- extracao textual direta de PDF;
- deteccao completa de tipo de arquivo;
- OCR integrado ao fluxo PNCP;
- camada de matching/comparacao formal;
- modelo completo de evidencia por campo;
- enriquecimento de CNPJ via BrasilAPI;
- interface Streamlit investigativa;
- banco de dados ou persistencia final.

Isso e bom: o projeto esta evoluindo em camadas pequenas, sem misturar tudo de uma vez.

## 11. Proximo Passo Recomendado

O proximo passo mais coerente e criar uma camada de identificacao de tipo de arquivo e extracao textual direta.

Fluxo desejado:

```text
Referencia PNCP
    |
    v
Download controlado
    |
    v
Identificar tipo real do arquivo
    |
    v
Se PDF com texto: extrair texto direto
    |
    v
Se imagem/PDF escaneado: acionar OCR
```

Isso preserva a regra central:

```text
OCR apenas quando necessario.
```

## 12. Resumo em Uma Frase

O Sherlock Holmes agora saiu de um conjunto de experimentos de OCR/PNCP e passou a ter uma base concreta para um pipeline auditavel: buscar contratos e licitacoes no PNCP, localizar anexos oficiais, transformar documentos em evidencias rastreaveis e baixar arquivos de forma controlada antes de decidir se OCR e realmente necessario.
