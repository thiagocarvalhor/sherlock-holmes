<section class="sh-hero">
  <div class="sh-hero__content">
    <img class="sh-hero__brand" src="assets/images/logo-sherlock-holmes-horizontal.png" alt="Sherlock Holmes">
    <p>Pipeline investigativo e auditável para localizar contratos públicos, comparar fontes manuais com dados oficiais e preservar evidências técnicas.</p>
    <div class="sh-rule">Evidência sempre</div>
    <div class="sh-action-row">
      <a href="getting-started/">Começar</a>
      <a href="architecture/">Arquitetura</a>
      <a href="audit-reports/">Relatórios</a>
    </div>
  </div>
</section>

## Norte

```text
PNCP primeiro.
Documentos depois.
OCR apenas quando necessário.
Evidência sempre.
```

O projeto compara registros manuais com dados oficiais do PNCP, preserva evidências por campo, consulta documentos oficiais quando o dado estruturado não basta e gera relatórios auditáveis para revisão técnica.

## O que o projeto faz hoje

<div class="sh-card-grid">
  <div class="sh-card">
    <strong>PNCP primeiro</strong>
    <p>Busca contratos, candidatos e documentos oficiais antes de acionar camadas mais caras.</p>
  </div>
  <div class="sh-card">
    <strong>Comparação auditável</strong>
    <p>Compara linha manual contra dado oficial, campo a campo, com score e status.</p>
  </div>
  <div class="sh-card">
    <strong>Evidência</strong>
    <p>Preserva origem, método e confiança para cada valor relevante.</p>
  </div>
  <div class="sh-card">
    <strong>Relatórios</strong>
    <p>Exporta JSON e Markdown para revisão técnica e rastreabilidade.</p>
  </div>
</div>

## Como ler esta documentação

- Use [Começar](getting-started.md) para instalar, testar e rodar o app.
- Use [Arquitetura](architecture.md) para entender a estrutura atual e a migração planejada.
- Use [Streamlit](streamlit.md) para o fluxo de investigação visual.
- Use [CLI](cli.md) para scripts operacionais.
- Use [Relatórios auditáveis](audit-reports.md) para entender os artefatos de auditoria.
- Use [Referência](reference/comparison.md) para documentação automática de módulos Python.

## Histórico de execução

O diretório `documentation/` continua sendo o histórico auditável de planos, relatórios e decisões de implementação. Esta pasta `docs/` é a documentação navegável e publicada do projeto.
