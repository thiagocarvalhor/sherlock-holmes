# Plano de Execucao: Reestruturacao Arquitetural do Repositorio

## Objetivo

Reorganizar o repositorio `sherlock-holmes` para reduzir acoplamento, deixar responsabilidades mais claras e preparar o projeto para crescer como uma aplicacao Python de dados/IA com documentacao automatica publicada.

Este plano segue a direcao do guia:

```text
Regra principal no centro.
Ferramentas nas bordas.
Documentacao como codigo.
Migracao incremental, sem big bang.
```

## Problema Atual

O projeto evoluiu rapido e ja possui varias entregas funcionais:

- consulta PNCP;
- referencias de documentos oficiais;
- comparacao manual versus PNCP;
- evidencia;
- relatorios auditaveis;
- enriquecimento CNPJ;
- Streamlit para investigacao;
- OCR como fallback.

Porem, a estrutura atual ainda esta organizada mais por trilhas tecnicas do que por responsabilidades arquiteturais:

```text
src/sherlock_holmes/
|-- pncp/
|-- enrichment/
|-- validation/
|-- documents/
|-- reporting/
|-- webapp/
|-- ocr/
`-- investigation.py
```

Isso cria alguns riscos:

- nao fica obvio onde colocar codigo novo;
- Streamlit e scripts podem acumular regra de negocio;
- PNCP e BrasilAPI aparecem como modulos centrais, embora sejam integracoes externas;
- `validation` mistura dominio, evidencia e aplicacao;
- `documentation/` virou historico de execucao, mas nao uma documentacao navegavel;
- testes ainda estao organizados por arquivo, nao por camada.

## Principios Da Migracao

- Migrar em fases pequenas.
- Manter `ruff` e `pytest` verdes em cada fase.
- Evitar quebrar scripts e Streamlit.
- Criar pontes temporarias para imports antigos quando necessario.
- Documentar a arquitetura antes de mover grandes blocos.
- Separar dominio, aplicacao, adapters e infraestrutura.
- Manter OCR real fora desta rodada, salvo reorganizacao de modulo.
- Tratar `documentation/` como historico e `docs/` como documentacao publicada.

## Arquitetura Alvo

Estrutura desejada para o pacote:

```text
src/sherlock_holmes/
|-- domain/
|   |-- entities/
|   |-- value_objects/
|   |-- services/
|   `-- exceptions/
|
|-- application/
|   |-- use_cases/
|   `-- ports/
|
|-- adapters/
|   |-- inbound/
|   |   |-- streamlit/
|   |   `-- cli/
|   |
|   `-- outbound/
|       |-- pncp/
|       |-- brasilapi/
|       |-- filesystem/
|       `-- ocr/
|
|-- infrastructure/
|   |-- config/
|   |-- logging/
|   `-- paths/
|
`-- shared/
```

## Papel Das Camadas

### `domain`

Conceitos centrais do Sherlock Holmes.

Exemplos:

- contrato;
- documento oficial;
- evidencia;
- comparacao;
- campo comparado;
- status de revisao;
- identificador PNCP;
- CNPJ;
- regra de matching.

Nao deve depender de:

- Streamlit;
- PNCP HTTP;
- BrasilAPI HTTP;
- filesystem;
- OCR engine;
- pandas.

### `application`

Casos de uso do sistema.

Exemplos:

- investigar linha manual;
- comparar linha manual com contrato oficial;
- gerar relatorio auditavel;
- preparar status de revisao;
- preparar exportacao;
- consolidar relatorios.

Pode depender de `domain` e de `ports`.

Nao deve depender diretamente de adapters concretos.

### `application/ports`

Contratos que a aplicacao precisa.

Exemplos:

- `PncpContractGateway`;
- `CnpjEnrichmentGateway`;
- `DocumentGateway`;
- `ReportWriter`;
- `ReviewStatusStore`.

No inicio, podem ser `Protocol` simples.

### `adapters/outbound`

Integracoes externas ou detalhes concretos de saida.

Exemplos:

- PNCP;
- BrasilAPI;
- OCR;
- leitura/escrita local;
- processamento de documentos locais.

### `adapters/inbound`

Entradas do sistema.

Exemplos:

- Streamlit;
- scripts CLI;
- jobs futuros.

### `infrastructure`

Configuracao e detalhes tecnicos compartilhados.

Exemplos:

- settings;
- paths padronizados;
- logging;
- bootstrap de ambiente.

## Documentacao Alvo

Criar documentacao automatica com MkDocs:

```text
docs/
|-- index.md
|-- getting-started.md
|-- architecture.md
|-- streamlit.md
|-- cli.md
|-- data-artifacts.md
|-- audit-reports.md
|-- development.md
|-- roadmap.md
|-- decisions/
|   |-- 0001-pncp-first.md
|   |-- 0002-ocr-as-fallback.md
|   `-- 0003-architecture-restructure.md
`-- reference/
    |-- domain.md
    |-- application.md
    |-- adapters.md
    `-- reporting.md
```

Manter:

```text
documentation/
```

como historico de planos, relatorios, experimentos e materiais de apoio.

## Ferramentas De Documentacao

Adicionar:

- `mkdocs`;
- `mkdocs-material`;
- `mkdocstrings[python]`.

Criar:

- `mkdocs.yml`;
- workflow de build/deploy para GitHub Pages;
- validacao `mkdocs build --strict`.

## Deploy Da Documentacao

Publicar via GitHub Pages com GitHub Actions.

Fluxo esperado:

```text
push em main
  -> CI roda lint/testes
  -> Docs build roda mkdocs build --strict
  -> GitHub Pages publica a documentacao
```

Observacao:

- usar `GITHUB_TOKEN` do Actions;
- configurar GitHub Pages para usar `GitHub Actions`;
- evitar uso de Personal Access Token.

## Mapeamento Inicial Dos Modulos

### Modulos atuais

```text
pncp/            -> adapters/outbound/pncp/
enrichment/      -> adapters/outbound/brasilapi/
webapp/          -> adapters/inbound/streamlit/
scripts/         -> adapters/inbound/cli/ + wrappers finos na raiz
validation/      -> domain/ + application/
reporting/       -> application/use_cases/ + possivel adapter filesystem
documents/       -> domain/documents + adapters/outbound/filesystem
ocr/             -> adapters/outbound/ocr/
investigation.py -> application/use_cases/investigate_manual_row.py
```

### Pontes temporarias

Durante a migracao, manter imports antigos como wrappers:

```python
# sherlock_holmes.validation.comparison
from sherlock_holmes.domain.entities.comparison import ...
```

Isso permite migrar codigo em ondas sem quebrar scripts, testes e Streamlit de uma vez.

## Fases De Execucao

### Fase 0: Documentacao automatica e mapa da migracao

Objetivo:

Criar a documentacao navegavel antes de mover codigo.

Entregas:

- `mkdocs.yml`;
- `docs/index.md`;
- `docs/getting-started.md`;
- `docs/architecture.md`;
- `docs/development.md`;
- `docs/decisions/0003-architecture-restructure.md`;
- `docs/reference/`;
- extras de documentacao no `pyproject.toml`;
- workflow `docs.yml` para build/deploy;
- atualizar README apontando para docs.

Criterio de conclusao:

- `mkdocs build --strict` passa;
- `ruff check .` passa;
- `pytest` passa;
- documentacao publicada no GitHub Pages apos push em `main`.

### Fase 1: Esqueleto arquitetural

Objetivo:

Criar as pastas novas sem mover regra critica.

Entregas:

- `src/sherlock_holmes/domain/`;
- `src/sherlock_holmes/application/`;
- `src/sherlock_holmes/adapters/`;
- `src/sherlock_holmes/infrastructure/`;
- `src/sherlock_holmes/shared/`;
- `README.md` curto ou docstring em cada camada explicando responsabilidade.

Criterio de conclusao:

- imports atuais continuam funcionando;
- testes continuam verdes.

### Fase 2: Dominio central

Objetivo:

Mover conceitos centrais para `domain`.

Candidatos:

- `validation/comparison.py`;
- `validation/evidence.py`;
- `pncp/ids.py`;
- modelos de revisao operacional;
- status de comparacao.

Destino sugerido:

```text
domain/entities/comparison.py
domain/entities/evidence.py
domain/value_objects/pncp_id.py
domain/value_objects/cnpj.py
domain/services/matching.py
domain/entities/review.py
```

Criterio de conclusao:

- regras puras ficam sem dependencias de PNCP HTTP, Streamlit ou filesystem;
- wrappers antigos preservam compatibilidade;
- testes unitarios de dominio passam.

### Fase 3: Casos de uso

Objetivo:

Mover orquestracao para `application/use_cases`.

Candidatos:

- `investigation.py`;
- geracao de relatorio auditavel;
- comparacao manual versus contrato;
- preparacao de revisao operacional.

Destino sugerido:

```text
application/use_cases/investigate_manual_row.py
application/use_cases/compare_manual_record.py
application/use_cases/build_audit_report.py
application/use_cases/prepare_review.py
```

Criterio de conclusao:

- Streamlit chama use cases em vez de montar regra complexa;
- scripts CLI chamam use cases em vez de duplicar fluxo;
- testes de application passam com dados fake/offline.

### Fase 4: Ports

Objetivo:

Definir contratos para dependencias externas.

Entregas sugeridas:

```text
application/ports/pncp_contract_gateway.py
application/ports/cnpj_enrichment_gateway.py
application/ports/document_gateway.py
application/ports/report_writer.py
application/ports/review_status_store.py
```

Criterio de conclusao:

- use cases dependem de ports;
- adapters concretos implementam ports;
- testes usam adapters fake/in-memory.

### Fase 5: Adapters outbound

Objetivo:

Mover integracoes externas para as bordas.

Movimentos sugeridos:

```text
pncp/       -> adapters/outbound/pncp/
enrichment/ -> adapters/outbound/brasilapi/
documents/  -> adapters/outbound/filesystem_documents/
ocr/        -> adapters/outbound/ocr/
```

Criterio de conclusao:

- adapters sabem chamar APIs e filesystem;
- dominio e use cases nao importam Streamlit, urllib ou detalhes de path;
- wrappers antigos preservam compatibilidade temporaria.

### Fase 6: Adapters inbound

Objetivo:

Organizar entradas do sistema.

Movimentos sugeridos:

```text
webapp/ -> adapters/inbound/streamlit/
scripts/ -> adapters/inbound/cli/ + scripts finos na raiz
```

Regra para scripts:

```python
from sherlock_holmes.adapters.inbound.cli.generate_audit_report import main

if __name__ == "__main__":
    main()
```

Criterio de conclusao:

- Streamlit fica mais fino;
- scripts viram wrappers;
- regra principal fica em `application`.

### Fase 7: Testes por camada

Objetivo:

Reorganizar testes para acompanhar a arquitetura.

Estrutura alvo:

```text
tests/
|-- unit/
|   |-- domain/
|   `-- application/
|
`-- integration/
    |-- adapters/
    |-- cli/
    `-- streamlit/
```

Criterio de conclusao:

- testes unitarios nao usam rede;
- testes de adapters externos usam mocks/injecao;
- testes Streamlit ficam em integration.

### Fase 8: Limpeza e remocao de pontes

Objetivo:

Remover compatibilidade antiga quando a migracao estiver consolidada.

Inclui:

- remover wrappers antigos;
- revisar `__all__`;
- atualizar README;
- atualizar docs;
- remover modulos orfaos;
- revisar nomes de scripts;
- revisar `.gitignore`;
- revisar dependencias no `pyproject.toml`.

Criterio de conclusao:

- nao ha imports antigos desnecessarios;
- docs descrevem a estrutura real;
- CI e docs passam.

## Fora De Escopo Nesta Rodada

- executar OCR pela UI;
- criar banco de dados;
- SQLAlchemy;
- Alembic;
- FastAPI;
- Docker;
- Unit of Work real;
- LLM ou agentes;
- persistencia multiusuario de revisao.

Esses itens podem entrar em planos futuros.

## Riscos E Mitigacoes

### Risco: big bang

Mitigacao:

- mover por camada;
- manter wrappers temporarios;
- validar com testes a cada fase.

### Risco: documentacao ficar desatualizada

Mitigacao:

- criar docs antes da migracao;
- incluir `mkdocs build --strict` no CI;
- atualizar `docs/architecture.md` a cada fase.

### Risco: Streamlit quebrar

Mitigacao:

- manter testes `AppTest`;
- deixar Streamlit como ultima borda a ser migrada;
- preservar wrappers antigos durante a transicao.

### Risco: scripts operacionais quebrarem

Mitigacao:

- transformar scripts em wrappers finos gradualmente;
- testar scripts principais apos cada fase.

## Ordem Recomendada De Commits

1. `feat: add mkdocs documentation site`
2. `docs: add architecture restructure plan`
3. `refactor: add architecture package skeleton`
4. `refactor: move comparison and evidence domain models`
5. `refactor: move investigation use case`
6. `refactor: introduce application ports`
7. `refactor: move pncp and brasilapi adapters`
8. `refactor: move streamlit and cli adapters`
9. `test: organize tests by architecture layer`
10. `refactor: remove legacy import bridges`

## Validacoes Por Fase

Comandos minimos:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
```

Quando MkDocs estiver instalado:

```powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

Scripts operacionais principais a revalidar quando afetados:

```powershell
.\.venv\Scripts\python.exe .\scripts\generate_audit_report.py
.\.venv\Scripts\python.exe .\scripts\generate_audit_batch_report.py
.\.venv\Scripts\python.exe -m streamlit run scripts\pncp_streamlit_app.py
```

## Primeiro Passo Concreto

Executar a Fase 0:

```text
criar MkDocs + docs/ + deploy GitHub Pages + pagina inicial de arquitetura
```

Depois disso, iniciar Fase 1 e Fase 2 com migracao pequena do dominio central.

## Criterio Geral De Conclusao

A migracao sera considerada concluida quando:

- a documentacao publicada explicar a estrutura real do projeto;
- `domain` concentrar conceitos centrais;
- `application` concentrar casos de uso;
- PNCP, BrasilAPI, filesystem, OCR, CLI e Streamlit estiverem nas bordas;
- scripts e Streamlit usarem use cases;
- testes estiverem organizados por camada;
- imports legados tiverem sido removidos ou justificados;
- `ruff`, `pytest` e `mkdocs build --strict` passarem no CI.
