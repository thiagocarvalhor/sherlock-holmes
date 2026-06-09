# Sherlock Holmes

Sherlock Holmes e um pipeline investigativo e auditavel para contratos publicos.

```text
PNCP primeiro.
Documentos depois.
OCR apenas quando necessario.
Evidencia sempre.
```

O projeto compara registros manuais com dados oficiais do PNCP, preserva evidencias por campo, consulta documentos oficiais quando o dado estruturado nao basta e gera relatorios auditaveis para revisao tecnica.

## O que o projeto faz hoje

- busca contratos no PNCP;
- lista documentos oficiais vinculados;
- compara linha manual versus contrato PNCP;
- calcula score e status de candidatos;
- enriquece CNPJ via BrasilAPI sob demanda;
- gera relatorios auditaveis em JSON e Markdown;
- oferece uma interface Streamlit para investigacao;
- mantem OCR como fallback documental, sem tratar OCR como ponto de partida.

## Como ler esta documentacao

- Use [Comecar](getting-started.md) para instalar, testar e rodar o app.
- Use [Arquitetura](architecture.md) para entender a estrutura atual e a migracao planejada.
- Use [Streamlit](streamlit.md) para o fluxo de investigacao visual.
- Use [CLI](cli.md) para scripts operacionais.
- Use [Relatorios auditaveis](audit-reports.md) para entender os artefatos de auditoria.
- Use [Referencia](reference/comparison.md) para documentacao automatica de modulos Python.

## Historico de execucao

O diretorio `documentation/` continua sendo o historico auditavel de planos, relatorios e decisoes de implementacao. Esta pasta `docs/` e a documentacao navegavel e publicada do projeto.
