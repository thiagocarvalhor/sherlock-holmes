# API de Consultas PNCP

## Objetivo

Este documento consolida o contexto técnico inicial da API pública de consultas do Portal Nacional de Contratações Públicas (PNCP) para o projeto Sherlock Holmes.

O papel deste arquivo é servir como referência de trabalho para a branch `feature/pncp-api`, explicando:

- qual API deve ser usada para consultar dados públicos do PNCP
- quais documentos oficiais servem como fonte
- quais endpoints parecem mais relevantes para a primeira implementação
- como funcionam parâmetros, paginação e respostas
- quais dados devem ser preservados para etapas posteriores de OCR, extração e análise

## Fontes Locais

Documentos adicionados em `documentation/source`:

- `documentation/source/api_de_consultas.pdf`
- `documentation/source/manual_de_integracao_pncp.pdf`
- `documentation/source/exemplo_1.xlsx`

### Papel de cada documento

`api_de_consultas.pdf` é a fonte principal para a extração inicial de dados. Ele descreve a API pública de consulta, usada para buscar dados já publicados no PNCP.

`manual_de_integracao_pncp.pdf` é uma fonte complementar. Ele cobre a integração completa com o PNCP, incluindo serviços de envio, alteração, exclusão, autenticação, órgãos, unidades, usuários e consultas detalhadas. Para o Sherlock Holmes, ele deve ser usado principalmente como referência para endpoints detalhados e dicionário de campos.

`exemplo_1.xlsx` é uma fonte manual inicial do projeto. Ele contém uma lista consolidada de contratos coletados manualmente, que deve servir como manifesto inicial para validar se o Sherlock Holmes consegue reencontrar os registros via API, baixar documentos e extrair informações dos contratos.

## Manifesto Manual Inicial

O arquivo `documentation/source/exemplo_1.xlsx` contém a aba `CONSOLIDADO`, com uma planilha chamada visualmente de "MAPA DE CONTRATOS DOS MUNICÍPIOS BRASILEIROS".

Esse arquivo representa o primeiro conjunto de casos reais de validação. Em vez de começar buscando qualquer contratação no PNCP, o projeto deve primeiro tentar reproduzir automaticamente informações que já foram extraídas manualmente.

### Estrutura da aba `CONSOLIDADO`

A aba possui cabeçalhos principais nas linhas 4 e 5. Os dados começam na linha 6.

Colunas identificadas:

- `MUNICÍPIO`
- `ESTADO`
- `REGIÃO`
- `POPULAÇÃO`
- `FAIXA POPULACIONAL`
- `OBJETO DO CONTRATO`
- `NOME DA EMPRESA`
- `REVISÃO EMPRESAS`
- `CNPJ`
- `VIGÊNCIA INÍCIO`
- `VIGÊNCIA FIM`
- `VALOR DO CONTRATO`
- `NÚMERO DO CONTRATO`
- `FONTE`

Contagem observada na leitura inicial:

- `347` linhas de dados
- `345` linhas com município preenchido
- `162` linhas com CNPJ preenchido
- `158` linhas com número de contrato preenchido
- `134` linhas com fonte textual preenchida
- `25` linhas mencionando `PNCP` na fonte ou no campo de número/fonte

### Observações sobre os dados

As datas de vigência aparecem no arquivo Excel como números seriais, por exemplo:

```text
45577
52882
```

Na implementação, esses valores devem ser convertidos para datas reais usando a convenção de datas do Excel.

Algumas células da coluna `FONTE` possuem hyperlinks para portais de transparência, páginas municipais ou arquivos PDF. A extração futura do manifesto deve preservar tanto o texto exibido quanto o hyperlink real da célula.

Exemplos de linhas com `FONTE = PNCP`:

- Belford Roxo/RJ, contrato `02/SEMSEP/2025/2025`
- Ananindeua/PA, contrato `082025/2025`
- Ananindeua/PA, contrato `052025/2025`
- Vila Velha/ES, contrato `299/2025`
- Montes Claros/MG, contrato `2762501/2025`
- Betim/MG, contrato `ECO0011/2025`
- Betim/MG, contrato `ECO0012/2025`
- Bauru/SP, contrato `13636/2025`
- Bauru/SP, contrato `13659/2025`
- Caruaru/PE, contrato `174/2025`

### Papel do manifesto manual

O manifesto manual deve orientar a primeira validação da API:

1. ler a aba `CONSOLIDADO`
2. filtrar inicialmente linhas com `FONTE = PNCP`
3. usar campos como município, UF, empresa, CNPJ, número do contrato e vigência para tentar localizar registros oficiais
4. baixar os dados oficiais via API
5. comparar dados da API com os dados extraídos manualmente
6. buscar documentos/anexos relacionados aos contratos encontrados
7. avaliar se a informação contratual pode ser extraída por texto direto, OCR ou outro mecanismo

Campos do manifesto que provavelmente ajudam na busca:

- `MUNICÍPIO`
- `ESTADO`
- `OBJETO DO CONTRATO`
- `NOME DA EMPRESA`
- `CNPJ`
- `VIGÊNCIA INÍCIO`
- `VIGÊNCIA FIM`
- `VALOR DO CONTRATO`
- `NÚMERO DO CONTRATO`
- `FONTE`

Campos-alvo que queremos reproduzir ou validar:

- fornecedor/empresa contratada
- CNPJ do fornecedor
- objeto do contrato
- número do contrato
- vigência inicial
- vigência final
- valor do contrato
- órgão/município responsável
- fonte/documento que comprova o dado

## Escopo da API de Consultas

A API de Consultas é voltada à leitura de dados públicos já disponibilizados no PNCP.

Ela permite consultar, entre outros:

- itens do Plano de Contratações Anual (PCA)
- contratações publicadas
- contratações com período de recebimento de propostas em aberto
- atas de registro de preço
- contratos e empenhos com força de contrato

Esta API não deve ser confundida com a API de integração/manutenção usada por órgãos, entidades ou plataformas credenciadas para alimentar o PNCP.

## URL Base

Ambiente produtivo:

```text
https://pncp.gov.br/api/consulta
```

Swagger oficial:

```text
https://pncp.gov.br/api/consulta/swagger-ui/index.html
```

## Autenticação

Para a API pública de consultas, o uso esperado é sem autenticação.

Isso é diferente da API de integração do PNCP, que envolve credenciamento, login, senha, token JWT e permissões para publicar ou alterar dados.

## Protocolo e Formato

A API usa:

- HTTP/REST
- respostas em JSON
- parâmetros de consulta via query string
- datas no formato `AAAAMMDD`

Exemplo de data:

```text
20260504
```

## Resposta Paginada

As consultas principais retornam dados paginados.

Campos padronizados citados no manual:

- `data`: lista de registros retornados
- `totalRegistros`: total de registros encontrados
- `totalPaginas`: total de páginas disponíveis
- `numeroPagina`: número da página retornada
- `paginasRestantes`: quantidade de páginas restantes
- `empty`: indicador de lista vazia

Regra operacional recomendada:

1. consultar sempre a `pagina=1`
2. ler `totalPaginas` e `paginasRestantes`
3. iterar até não haver páginas restantes
4. salvar cada resposta bruta antes de transformar os dados

## Tamanho de Página

O parâmetro `tamanhoPagina` é opcional.

Nos endpoints consultivos, o limite máximo indicado pelo manual é geralmente de até `500` registros por página. Em algumas descrições, o padrão inicial aparece como `50` registros.

Recomendação inicial do projeto:

- começar com `tamanhoPagina=50` em smoke tests
- usar `tamanhoPagina=500` somente após validar estabilidade, tempo e volume de resposta

## Códigos de Retorno

Códigos recorrentes no manual:

- `200 OK`: sucesso com conteúdo
- `204 No Content`: sucesso sem registros
- `400 Bad Request`: erro de requisição
- `422 Unprocessable Entity`: parâmetros ou regras inválidas
- `500 Internal Server Error`: erro interno do serviço

Regra prática:

- tratar `204` como resultado vazio, não como falha
- registrar corpo da resposta de erro sempre que disponível
- persistir metadados da chamada, incluindo URL, parâmetros e status HTTP

### Instabilidade observada

Em `2026-05-26`, chamadas mínimas ao endpoint `/v1/contratos` feitas pelo Postman retornaram `504 Gateway Time-out`.

Exemplo testado:

```text
GET https://pncp.gov.br/api/consulta/v1/contratos?dataInicial=20251104&dataFinal=20251104&pagina=1&tamanhoPagina=1&cnpjOrgao=39485438000142
```

Resposta recebida:

```html
<html>
<body>
    <h1>504 Gateway Time-out</h1>
    The server didn't respond in time.
</body>
</html>
```

Interpretação:

- a consulta estava pequena e bem formada
- o erro não indica parâmetro inválido, pois nesse caso seriam esperados `400` ou `422`
- o caso deve ser tratado como instabilidade temporária do serviço/gateway PNCP
- antes de alterar a estratégia de consulta, retestar o endpoint em outro momento
- o cliente futuro deve registrar `504` e prever retry/backoff com limite de tentativas

## Endpoints Principais

### Consultar Contratações por Data de Publicação

Endpoint:

```text
GET /v1/contratacoes/publicacao
```

Objetivo:

- recuperar contratações publicadas no PNCP dentro de um período

Parâmetros principais:

- `dataInicial`: obrigatório, formato `AAAAMMDD`
- `dataFinal`: obrigatório, formato `AAAAMMDD`
- `codigoModalidadeContratacao`: obrigatório
- `pagina`: obrigatório
- `tamanhoPagina`: opcional

Filtros opcionais:

- `codigoModoDisputa`
- `uf`
- `codigoMunicipioIbge`
- `cnpj`
- `codigoUnidadeAdministrativa`
- `idUsuario`

Exemplo conceitual:

```text
GET https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao?dataInicial=20260501&dataFinal=20260504&codigoModalidadeContratacao=8&pagina=1
```

Campos importantes de retorno:

- `numeroControlePNCP`
- `numeroCompra`
- `anoCompra`
- `processo`
- `modalidadeId`
- `modalidadeNome`
- `modoDisputaId`
- `modoDisputaNome`
- `situacaoCompraId`
- `situacaoCompraNome`
- `objetoCompra`
- `informacaoComplementar`
- `srp`
- `amparoLegal`
- `valorTotalEstimado`
- `valorTotalHomologado`
- `dataAberturaProposta`
- `dataEncerramentoProposta`
- `dataPublicacaoPncp`
- `dataInclusao`
- `dataAtualizacao`
- `sequencialCompra`
- `orgaoEntidade`
- `unidadeOrgao`
- `usuarioNome`
- `linkSistemaOrigem`

Este deve ser o primeiro endpoint implementado, pois fornece a lista base de contratações para exploração posterior.

### Consultar Contratações com Propostas em Aberto

Endpoint:

```text
GET /v1/contratacoes/proposta
```

Objetivo:

- recuperar contratações com recebimento de propostas em aberto até uma data final

Parâmetros principais:

- `dataFinal`: obrigatório, formato `AAAAMMDD`
- `codigoModalidadeContratacao`: obrigatório
- `pagina`: obrigatório
- `tamanhoPagina`: opcional

Filtros opcionais:

- `uf`
- `codigoMunicipioIbge`
- `cnpj`
- `codigoUnidadeAdministrativa`
- `idUsuario`

Uso no projeto:

- útil para detectar oportunidades ainda ativas
- pode ser priorizado se o objetivo passar a incluir monitoramento de contratações abertas

### Consultar Atas de Registro de Preço por Vigência

Endpoint:

```text
GET /v1/atas
```

Objetivo:

- recuperar atas de registro de preço cujo período de vigência coincida com o intervalo informado

Parâmetros principais:

- `dataInicial`: obrigatório, formato `AAAAMMDD`
- `dataFinal`: obrigatório, formato `AAAAMMDD`
- `pagina`: obrigatório
- `tamanhoPagina`: opcional

Filtros opcionais:

- `idUsuario`
- `cnpj`
- `codigoUnidadeAdministrativa`

Campos importantes de retorno:

- `numeroControlePNCPAta`
- `numeroControlePNCPCompra`
- `numeroAtaRegistroPreco`
- `anoAta`
- `dataAssinatura`
- `vigenciaInicio`
- `vigenciaFim`
- `dataCancelamento`
- `cancelado`
- `dataPublicacaoPncp`
- `dataInclusao`
- `dataAtualizacao`
- `objetoContratacao`
- `cnpjOrgao`
- `nomeOrgao`
- `codigoUnidadeOrgao`
- `nomeUnidadeOrgao`
- `usuario`

Uso no projeto:

- relevante quando o Sherlock Holmes precisar acompanhar atas vigentes ou relacionadas a contratações específicas
- deve entrar depois do fluxo base de contratações

### Consultar Contratos por Data de Publicação

Endpoint:

```text
GET /v1/contratos
```

Objetivo:

- recuperar contratos e empenhos com força de contrato publicados no PNCP em um período

Parâmetros principais:

- `dataInicial`: obrigatório, formato `AAAAMMDD`
- `dataFinal`: obrigatório, formato `AAAAMMDD`
- `pagina`: obrigatório
- `tamanhoPagina`: opcional

Filtros opcionais:

- `cnpjOrgao`
- `codigoUnidadeAdministrativa`
- `usuarioId`

Campos importantes de retorno:

- `numeroControlePNCP`
- `numeroControlePNCPCompra`
- `numeroContratoEmpenho`
- `anoContrato`
- `sequencialContrato`
- `processo`
- `tipoContrato`
- `categoriaProcesso`

Uso no projeto:

- importante para relacionar contratações publicadas a contratos efetivamente firmados
- pode ser usado em uma segunda etapa de enriquecimento dos dados

### Consultar Itens de PCA por Usuário

Endpoint:

```text
GET /v1/pca/usuario
```

Objetivo:

- recuperar itens de Plano de Contratações Anual por ano e por sistema usuário

Parâmetros principais:

- `anoPca`: obrigatório
- `idUsuario`: obrigatório
- `pagina`: obrigatório
- `tamanhoPagina`: opcional

Filtro opcional:

- `codigoClassificacaoSuperior`

Uso no projeto:

- útil se o escopo incluir planejamento anual de compras
- não é prioridade para a primeira extração de contratações publicadas

### Consultar Itens de PCA por Classificação

Endpoint:

```text
GET /v1/pca/
```

Objetivo:

- recuperar itens de Plano de Contratações Anual por ano e classificação superior

Parâmetros principais:

- `anoPca`: obrigatório
- `codigoClassificacaoSuperior`: obrigatório
- `pagina`: obrigatório
- `tamanhoPagina`: opcional

Uso no projeto:

- útil para análises por classe de material ou grupo de serviço
- não é prioridade para o primeiro cliente da API

## Campos-Chave Para Encadear Consultas

Os campos abaixo devem ser preservados sem transformação agressiva:

- `numeroControlePNCP`
- `numeroControlePNCPCompra`
- `numeroControlePNCPAta`
- `cnpj`
- `cnpjOrgao`
- `orgaoEntidade.cnpj`
- `anoCompra`
- `sequencialCompra`
- `anoContrato`
- `sequencialContrato`
- `codigoUnidadeAdministrativa`
- `unidadeOrgao.codigoUnidade`
- `idUsuario`
- `usuarioId`

Esses campos permitem relacionar registros e acionar consultas detalhadas descritas no Manual de Integração.

## Relação com o Manual de Integração

O manual de consultas indica que há funcionalidades detalhadas descritas no Manual de Integração, incluindo:

- consultar uma contratação específica
- consultar todos os documentos de uma contratação
- consultar itens de uma contratação
- consultar resultados de item
- consultar histórico da contratação
- consultar imagens de um item de contratação
- consultar atas por compra
- consultar documentos de uma ata

Estratégia recomendada:

1. usar a API de Consultas para descobrir registros em lote
2. preservar identificadores técnicos de cada registro
3. usar endpoints detalhados do Manual de Integração apenas quando for necessário aprofundar um registro específico

## Relação com OCR

A API de Consultas retorna dados estruturados em JSON.

OCR só deve entrar quando o projeto precisar processar documentos anexos, como:

- edital
- termo de referência
- estudo técnico preliminar
- minuta de contrato
- contrato
- ata
- anexos do processo

Fluxo provável:

1. consultar contratações via API
2. selecionar contratações de interesse
3. buscar metadados e documentos associados
4. baixar documentos
5. identificar formato e presença de camada textual
6. aplicar extração textual direta ou OCR conforme necessário

## Estratégia Inicial de Implementação

### Decisão de organização do código

Por enquanto, a prioridade é fazer o fluxo de consulta da API funcionar de forma simples e verificável.

O script atual:

```text
scripts/run_pncp_api_smoke.py
```

deve continuar concentrando a lógica do smoke test enquanto a estratégia de consulta, matching e tratamento de respostas ainda estiver sendo validada.

Quando o fluxo estiver mais estável, a lógica reutilizável pode ser extraída para um módulo próprio dentro do pacote Python do projeto:

```text
src/sherlock_holmes/pncp/
  __init__.py
  client.py
  manifest.py
  matching.py
```

Responsabilidades previstas:

- `client.py`: chamadas HTTP para a API PNCP, montagem de URL, timeout, status HTTP e tratamento de erros
- `manifest.py`: leitura da amostra/manual, filtros por `source_row`, preparação de parâmetros e distinção futura entre CNPJ de órgão e CNPJ de fornecedor
- `matching.py`: normalização de texto/CNPJ/número de contrato, scoring de candidatos e escolha dos melhores matches

Essa extração não é prioridade imediata. A decisão atual é validar primeiro a consulta real contra a API, especialmente os casos em que o CNPJ da planilha pode representar órgão contratante ou fornecedor.

### Fase 1: Manifesto manual

Implementar ou preparar uma leitura controlada de `documentation/source/exemplo_1.xlsx` para:

- ler a aba `CONSOLIDADO`
- normalizar os cabeçalhos das linhas 4 e 5
- preservar número da linha original
- converter datas seriais do Excel em datas ISO
- preservar texto e hyperlink da coluna `FONTE`, quando houver
- filtrar inicialmente registros com `FONTE = PNCP`
- gerar um manifesto intermediário versionável ou reproduzível para o smoke da API

Campos mínimos do manifesto intermediário:

- `source_row`
- `municipio`
- `uf`
- `objeto_contrato`
- `nome_empresa`
- `revisao_empresas`
- `cnpj`
- `vigencia_inicio`
- `vigencia_fim`
- `valor_contrato`
- `numero_contrato`
- `fonte_texto`
- `fonte_url`

### Fase 2: Cliente mínimo

Implementar um cliente simples para:

- montar URLs a partir de `base_url`
- enviar requisições GET
- lidar com status `200`, `204`, `400`, `422` e `500`
- retornar JSON bruto
- registrar parâmetros usados

### Fase 3: Localização via API

Implementar comando ou script para tentar localizar, na API, os registros do manifesto manual.

Estratégia inicial:

- começar pelas linhas com `FONTE = PNCP`
- consultar contratos por data de publicação ou por janelas derivadas da vigência/ano do contrato
- usar `uf`, município, CNPJ da empresa, número do contrato e objeto como critérios de comparação
- salvar todas as respostas candidatas antes de decidir o match

Endpoint inicial provável:

```text
GET /v1/contratos
```

Motivo:

- o manifesto manual tem foco em contratos, não apenas em contratações
- campos como `numeroContratoEmpenho`, `numeroControlePNCPCompra`, `anoContrato`, `sequencialContrato`, órgão e processo ajudam a aproximar o registro da planilha

Endpoint complementar:

```text
GET /v1/contratacoes/publicacao
```

Motivo:

- pode ajudar a localizar a contratação original quando o contrato não for encontrado diretamente
- retorna `anoCompra`, `sequencialCompra`, órgão, unidade, objeto e datas úteis para consultas detalhadas

### Fase 4: Extração por data

Depois do smoke com o manifesto manual, implementar coleta mais ampla por data para:

- consultar `/v1/contratacoes/publicacao`
- aceitar `dataInicial`, `dataFinal`, `codigoModalidadeContratacao`, `uf`, `cnpj` e `pagina`
- salvar respostas brutas em `data/raw/pncp`
- salvar resumo tabular em `data/processed/pncp`

Observação: `data/raw` e `data/processed` já estão ignorados no Git.

### Fase 5: Paginação

Adicionar iteração automática:

- começar em `pagina=1`
- ler `totalPaginas`
- repetir até a última página
- salvar cada página separadamente
- consolidar os registros em um arquivo único por execução

### Fase 6: Enriquecimento

Adicionar consultas complementares:

- contratos por data
- atas por vigência
- detalhes por contratação
- documentos associados à contratação

## Organização Sugerida de Artefatos Locais

Dados brutos:

```text
data/raw/pncp/<run_id>/...
```

Dados normalizados:

```text
data/processed/pncp/<run_id>/...
```

Relatórios versionáveis:

```text
documentation/reports/pncp-*.md
```

Documentos fonte:

```text
documentation/source/api_de_consultas.pdf
documentation/source/manual_de_integracao_pncp.pdf
```

## Primeira Hipótese Técnica

O caminho mais seguro para começar é usar o manifesto manual em `exemplo_1.xlsx` e tentar reencontrar primeiro os contratos cuja fonte já está marcada como `PNCP`.

Consulta prioritária:

```text
GET /v1/contratos
```

Motivos:

- a planilha consolidada é um mapa de contratos
- os campos manuais incluem número do contrato, empresa, CNPJ, vigência e valor
- a resposta de contratos pode trazer `numeroControlePNCPCompra`, permitindo voltar para a contratação original

Consulta complementar:

```text
GET /v1/contratacoes/publicacao
```

Motivos:

- fornece a lista-base de contratações publicadas
- retorna identificadores necessários para consultas posteriores
- permite filtros por período, modalidade, UF, município, CNPJ, unidade e sistema usuário
- combina bem com um fluxo incremental de coleta

## Questões em Aberto

- Quais modalidades de contratação devem entrar primeiro no escopo?
- O projeto deve começar por uma UF, município ou CNPJ específico?
- Qual janela temporal inicial será usada no smoke test da API?
- Quais documentos anexos serão prioritários para download e OCR?
- O pipeline deve priorizar contratações abertas ou histórico já publicado?
- Como controlar reprocessamento de registros já coletados?
- Qual formato final será mais útil para análise: JSON bruto, CSV normalizado, Parquet ou banco local?

## Recomendação

Para a próxima etapa, criar um smoke test da API guiado pelo manifesto manual:

- ler `documentation/source/exemplo_1.xlsx`
- filtrar linhas com `FONTE = PNCP`
- escolher poucas linhas iniciais, por exemplo `5`
- tentar localizar os contratos via `/v1/contratos`
- salvar respostas candidatas
- comparar número do contrato, CNPJ, município/UF, empresa e valor
- registrar quais campos foram encontrados diretamente pela API
- registrar quais campos exigem documento/anexo e extração textual

Após esse smoke, expandir para:

- mais linhas PNCP da planilha
- paginação completa quando necessário
- enriquecimento via contratação relacionada
- busca e download de documentos
- extração textual direta ou OCR

Para uma coleta ampla posterior, usar:

- endpoint `/v1/contratacoes/publicacao`
- janelas curtas de datas
- modalidade obrigatória
- `tamanhoPagina` pequeno
- persistência do JSON bruto
- resumo simples com contagem de registros e principais campos

Depois que esse fluxo estiver confiável, expandir para paginação completa e enriquecimento por detalhes/documentos.
