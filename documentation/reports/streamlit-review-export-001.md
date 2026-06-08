# Relatorio: Revisao e Exportacao Auditavel no Streamlit - Entrega 001

## Objetivo

Adicionar exportacao de relatorio auditavel, status de revisao e indicador operacional de OCR ao Streamlit.

## Artefatos Criados

- `documentation/plans/streamlit-review-export-execution-plan.md`

## Artefatos Atualizados

- `src/sherlock_holmes/webapp/views.py`
- `tests/test_webapp_contract_selection.py`
- `documentation/projetos-similares/plano-execucao-roadmap-sherlock-holmes.md`

## Funcionalidades

- cada comparacao exibida passa a mostrar `Revisao operacional`;
- o usuario pode selecionar status:
  - `pendente`;
  - `em revisao`;
  - `validado`;
  - `divergencia confirmada`;
  - `precisa revisar documento`;
- notas de revisao ficam na sessao Streamlit;
- a UI mostra `Revisao documental`;
- a UI mostra indicador de OCR:
  - `Nao necessario`;
  - `Nao avaliado`;
  - `Pode precisar`;
- a UI exporta relatorio auditavel em Markdown;
- a UI exporta relatorio auditavel em JSON;
- documentos oficiais carregados na busca entram no relatorio exportado;
- enriquecimento CNPJ ja consultado na tela entra no relatorio exportado.

## Decisoes

- OCR nao e executado nesta entrega.
- O indicador `Pode precisar` e apenas operacional, usado quando ha campos divergentes/parciais e documentos oficiais vinculados.
- Status e notas ainda nao sao persistidos fora da sessao Streamlit.
- A exportacao usa `sherlock_holmes.reporting.audit`, mantendo o mesmo formato dos scripts operacionais.

## Validacoes Automatizadas

- `ruff check src/sherlock_holmes/webapp/views.py tests/test_webapp_contract_selection.py` - passou.
- `pytest tests/test_webapp_contract_selection.py` - 9 testes passaram.

## Observacoes

A entrega fecha a parte mais importante da Fase 8 sem abrir a frente pesada de OCR. O proximo refinamento natural e decidir se o status de revisao deve ser salvo em arquivo JSON/CSV por execucao.
