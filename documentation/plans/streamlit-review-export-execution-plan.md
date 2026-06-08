# Plano de Execucao: Revisao e Exportacao Auditavel no Streamlit

## Objetivo

Evoluir a tela Streamlit para apoiar revisao operacional sem antecipar a execucao de OCR.

## Escopo

### Inclui

- exportar relatorio auditavel em Markdown;
- exportar relatorio auditavel em JSON;
- registrar status de revisao na sessao Streamlit;
- registrar notas de revisao;
- indicar necessidade de revisao documental;
- indicar se OCR nao e necessario, nao foi avaliado ou pode ser necessario;
- incluir documentos oficiais e enriquecimento CNPJ ja carregados no relatorio exportado;
- validar helpers e render basico com testes offline.

### Nao Inclui

- salvar status de revisao em banco ou arquivo;
- executar OCR;
- processar texto de documentos pela UI;
- criar fluxo de aprovacao multiusuario.

## Arquivos Esperados

- `src/sherlock_holmes/webapp/views.py`
- `tests/test_webapp_contract_selection.py`
- `documentation/reports/streamlit-review-export-001.md`

## Criterio de Conclusao

Dada uma comparacao exibida no Streamlit, o usuario deve conseguir escolher um status de revisao, registrar notas, ver se ha revisao documental/OCR pendente e baixar relatorio auditavel em Markdown ou JSON.
