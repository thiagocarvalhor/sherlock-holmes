"""Streamlit renderers for the document-first Sherlock Holmes workflow."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from sherlock_holmes.application.use_cases import (
    InvestigationResult,
    build_audit_report,
    compare_manual_record,
    investigate_row,
    load_manual_rows,
    render_audit_report_markdown,
)
from sherlock_holmes.domain.entities import RecordComparison
from sherlock_holmes.domain.services import assess_review_needs
from sherlock_holmes.enrichment import BrasilApiCnpjRecord, BrasilApiError, fetch_cnpj
from sherlock_holmes.pncp.client import PncpApiError, compact_digits
from sherlock_holmes.webapp.comparison import (
    MANUAL_FIELDS,
    candidate_detail_url,
    candidates_dataframe,
    match_count,
)
from sherlock_holmes.webapp.pncp import (
    PRESET_ORGAOS,
    cached_contract_files,
    cached_contract_search,
    contract_detail_url,
    contract_file_download_url,
    filter_records_by_terms,
    record_label,
    suggested_terms,
)
from sherlock_holmes.webapp.ui import color_status, field_row_html, status_badge

ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_MANUAL_CSV = ROOT_DIR / "documentation" / "plans" / "pncp-api-smoke-sample.csv"

REVIEW_STATUS_OPTIONS = [
    "pendente",
    "em_revisao",
    "validado",
    "divergencia_confirmada",
    "precisa_revisar_documento",
]

REVIEW_STATUS_LABELS = {
    "pendente": "Pendente",
    "em_revisao": "Em revisao",
    "validado": "Validado",
    "divergencia_confirmada": "Divergencia confirmada",
    "precisa_revisar_documento": "Precisa revisar documento",
}

@dataclass(frozen=True)
class ContractCandidate:
    """One PNCP contract plus optional comparison score against a manual row."""

    contract: dict[str, Any]
    comparison: RecordComparison | None = None


@st.cache_data(show_spinner=False, ttl=900)
def cached_investigate_row(
    manual_row: dict, window_days: int, page_size: int, max_pages: int
) -> InvestigationResult:
    """Cached wrapper around the live investigation flow."""

    return investigate_row(
        manual_row,
        window_days=window_days,
        page_size=page_size,
        max_pages=max_pages,
    )


@st.cache_data(show_spinner=False, ttl=900)
def cached_cnpj_enrichment(cnpj: str) -> BrasilApiCnpjRecord:
    """Cached wrapper around BrasilAPI CNPJ enrichment."""

    return fetch_cnpj(cnpj)


def render_app() -> None:
    """Render the full Streamlit app in the intended investigation order."""

    render_document_search_section()
    st.divider()
    render_comparison_section()


def render_busca_tab() -> None:
    """Backward-compatible entry point for the old tab-based app."""

    render_document_search_section()


def render_comparacao_tab() -> None:
    """Backward-compatible entry point for the old tab-based app."""

    render_comparison_section()


def render_document_search_section() -> None:
    """Render the first workflow step: find PNCP contracts and documents."""

    st.header("Documentos PNCP")

    preset_options = [*PRESET_ORGAOS.keys(), "Manual"]
    preset = st.selectbox("Orgao", preset_options, key="doc_preset")
    preset_data = PRESET_ORGAOS.get(preset, {})

    col_orgao, col_unidade, col_ano, col_tema = st.columns([2, 1, 1, 1])
    if preset == "Manual":
        cnpj_orgao = col_orgao.text_input("CNPJ do orgao", key="doc_cnpj_manual")
        codigo_unidade = col_unidade.text_input("Unidade", key="doc_unidade_manual")
    else:
        cnpj_orgao = preset_data.get("cnpj", "")
        codigo_unidade = preset_data.get("unidade", "")
        col_orgao.text_input("CNPJ do orgao", value=cnpj_orgao, disabled=True, key="doc_cnpj_preset")
        col_unidade.text_input("Unidade", value=codigo_unidade, disabled=True, key="doc_unidade_preset")

    year = int(col_ano.number_input("Ano", min_value=2021, max_value=2100, value=2025, step=1, key="doc_year"))
    topic = col_tema.text_input("Tema", value="limpeza", key="doc_topic")

    with st.expander("Filtros"):
        filter_col, size_col, pages_col = st.columns([2, 1, 1])
        suggestions = suggested_terms(topic)
        selected_terms = filter_col.multiselect(
            "Palavras-chave",
            suggestions,
            default=suggestions,
            key="doc_terms",
        )
        page_size = int(
            size_col.slider(
                "Itens por pagina",
                min_value=10,
                max_value=500,
                value=500,
                step=10,
                key="doc_page_size",
            )
        )
        max_pages = int(
            pages_col.slider(
                "Paginas",
                min_value=1,
                max_value=100,
                value=20,
                key="doc_max_pages",
            )
        )
        custom_terms = st.text_input("Termos extras", key="doc_custom_terms")

    priority_manual_row, priority_source_row = _render_priority_controls()
    terms = selected_terms + [term.strip() for term in custom_terms.split(",") if term.strip()]
    search = st.button("Buscar documentos", type="primary", key="doc_search")

    if search:
        if not compact_digits(cnpj_orgao):
            st.error("Informe um CNPJ valido.")
            return
        st.session_state["document_search_params"] = {
            "year": year,
            "cnpj_orgao": cnpj_orgao,
            "codigo_unidade": codigo_unidade,
            "page_size": page_size,
            "max_pages": max_pages,
        }
        st.session_state["document_terms"] = terms

    search_params = st.session_state.get("document_search_params")
    if not search_params:
        return

    try:
        with st.spinner("Consultando contratos no PNCP..."):
            result = cached_contract_search(**search_params)
    except PncpApiError as exc:
        st.error(str(exc))
        return
    except OSError as exc:
        st.error(f"Erro de conexao com o PNCP: {exc}")
        return

    payload = result["payload"]
    records = payload.get("data", []) if isinstance(payload, dict) else []
    filtered_records = filter_records_by_terms(records, st.session_state.get("document_terms", []))

    st.caption(f"Consulta: {result['url']}")
    metric_cols = st.columns(3)
    metric_cols[0].metric("Contratos", len(records))
    metric_cols[1].metric("Filtrados", len(filtered_records))
    metric_cols[2].metric("Fonte", "PNCP")

    if not records:
        st.warning("Nenhum contrato encontrado.")
        return

    if not filtered_records:
        st.info("Nenhum contrato passou pelos filtros.")
        return

    candidates = _rank_contract_candidates(filtered_records, priority_manual_row)
    _render_contracts_table(candidates)

    selected_candidate = _render_contract_selector(candidates, priority_source_row=priority_source_row)
    selected = selected_candidate.contract
    st.session_state["selected_pncp_contract"] = selected
    st.session_state["selected_pncp_contract_comparison"] = selected_candidate.comparison
    st.session_state["selected_pncp_contract_comparison_context"] = (
        priority_source_row,
        str(selected.get("numeroControlePNCP", "")),
    )
    _render_contract_documents(selected)
    _render_cnpj_enrichment(selected)


def _render_priority_controls() -> tuple[dict[str, Any] | None, str | None]:
    with st.expander("Priorizacao pela planilha manual", expanded=True):
        enabled = st.checkbox(
            "Ranquear contratos encontrados contra uma linha manual",
            value=True,
            key="doc_rank_enabled",
        )
        if not enabled:
            st.caption("Sem priorizacao: a escolha do contrato e manual, a partir da lista filtrada.")
            return None, None

        csv_path = st.text_input("Planilha manual (CSV)", value=str(DEFAULT_MANUAL_CSV), key="doc_rank_csv")
        path = Path(csv_path)
        if not path.exists():
            st.warning(f"Planilha nao encontrada: `{path}`")
            return None, None

        rows = load_manual_rows(path)
        if not rows:
            st.warning("A planilha manual esta vazia.")
            return None, None

        by_row = {str(row.get("source_row", index)): row for index, row in enumerate(rows)}
        keys = list(by_row)
        default_index = keys.index("67") if "67" in keys else 0
        selected_key = st.selectbox(
            "Linha usada no ranking",
            keys,
            index=default_index,
            format_func=lambda key: _manual_row_label(by_row[key], key),
            key="doc_rank_row",
        )
        manual_row = by_row[selected_key]
        st.caption(
            "Criterio: cada contrato filtrado e comparado com essa linha; a lista fica ordenada pelo maior score."
        )
        return manual_row, selected_key


def _render_contracts_table(candidates: list[ContractCandidate]) -> None:
    dataframe = _contract_candidates_dataframe(candidates)
    st.dataframe(dataframe, use_container_width=True, hide_index=True)

    csv_data = dataframe.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Baixar CSV",
        data=csv_data,
        file_name="pncp-contratos-filtrados.csv",
        mime="text/csv",
        key="doc_download_csv",
    )


def _render_contract_selector(
    candidates: list[ContractCandidate], *, priority_source_row: str | None
) -> ContractCandidate:
    selected_index = st.selectbox(
        "Contrato escolhido",
        range(len(candidates)),
        format_func=lambda index: _candidate_label(candidates[index]),
        key="doc_contract",
    )
    selected_candidate = candidates[int(selected_index)]
    selected = selected_candidate.contract
    cnpj, contract_year, sequencial = _contract_parts(selected)

    detail_url = contract_detail_url(cnpj, contract_year, sequencial)
    cols = st.columns([3, 1])
    cols[0].markdown(f"**Contrato escolhido:** `{selected.get('numeroControlePNCP', '')}`")
    if selected_candidate.comparison is None:
        cols[0].caption("Criterio: escolha manual sobre a lista filtrada do PNCP.")
    else:
        matched, total = match_count(selected_candidate.comparison)
        cols[0].caption(
            f"Criterio: score {selected_candidate.comparison.overall_score:.2f} contra a linha "
            f"{priority_source_row}; {matched}/{total} campos em match."
        )
        cols[0].markdown(status_badge(selected_candidate.comparison.status), unsafe_allow_html=True)
    cols[1].link_button("Abrir contrato", detail_url)
    st.caption(str(selected.get("objetoContrato") or ""))
    return selected_candidate


def _rank_contract_candidates(
    records: list[dict[str, Any]], manual_row: dict[str, Any] | None
) -> list[ContractCandidate]:
    if manual_row is None:
        return [ContractCandidate(contract=record) for record in records]

    candidates = [
        ContractCandidate(
            contract=record,
            comparison=_compare_manual_with_contract(manual_row, record),
        )
        for record in records
    ]
    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.comparison.overall_score if candidate.comparison else 0.0,
            str(candidate.contract.get("numeroControlePNCP", "")),
        ),
        reverse=True,
    )


def _contract_candidates_dataframe(candidates: list[ContractCandidate]) -> pd.DataFrame:
    rows = []
    has_scores = any(candidate.comparison is not None for candidate in candidates)
    for position, candidate in enumerate(candidates, start=1):
        contract = candidate.contract
        comparison = candidate.comparison
        matched, total = match_count(comparison) if comparison else (None, None)
        row = {
            "rank": position if has_scores else "",
            "score": comparison.overall_score if comparison else "",
            "status": comparison.status if comparison else "",
            "matches": f"{matched}/{total}" if comparison else "",
            "numeroControlePNCP": contract.get("numeroControlePNCP"),
            "numeroContratoEmpenho": contract.get("numeroContratoEmpenho"),
            "processo": contract.get("processo"),
            "nomeRazaoSocialFornecedor": contract.get("nomeRazaoSocialFornecedor"),
            "valorGlobal": contract.get("valorGlobal"),
            "dataVigenciaInicio": contract.get("dataVigenciaInicio"),
            "dataVigenciaFim": contract.get("dataVigenciaFim"),
            "objetoContrato": contract.get("objetoContrato"),
        }
        rows.append(row)
    return pd.DataFrame(rows)


def _candidate_label(candidate: ContractCandidate) -> str:
    label = record_label(candidate.contract)
    if candidate.comparison is None:
        return label
    matched, total = match_count(candidate.comparison)
    return f"{candidate.comparison.overall_score:.2f} | {candidate.comparison.status} | {matched}/{total} | {label}"


def _render_contract_documents(contract: dict[str, Any]) -> None:
    st.subheader("Arquivos oficiais")
    cnpj, contract_year, sequencial = _contract_parts(contract)
    contract_context = str(contract.get("numeroControlePNCP", ""))

    try:
        with st.spinner("Buscando arquivos do contrato..."):
            files_result = cached_contract_files(cnpj, contract_year, sequencial)
    except PncpApiError as exc:
        st.error(str(exc))
        st.session_state["selected_pncp_contract_files"] = []
        st.session_state["selected_pncp_contract_files_context"] = contract_context
        return
    except OSError as exc:
        st.error(f"Erro de conexao com o PNCP: {exc}")
        st.session_state["selected_pncp_contract_files"] = []
        st.session_state["selected_pncp_contract_files_context"] = contract_context
        return

    files = files_result["payload"] if isinstance(files_result["payload"], list) else []
    st.session_state["selected_pncp_contract_files"] = files
    st.session_state["selected_pncp_contract_files_context"] = contract_context
    if not files:
        st.info("Nenhum arquivo encontrado para esse contrato.")
        return

    file_rows = [_document_row(file_record) for file_record in files]
    st.dataframe(pd.DataFrame(file_rows), use_container_width=True, hide_index=True)

    selected_index = st.selectbox(
        "Documento",
        range(len(files)),
        format_func=lambda index: _document_label(files[index]),
        key="doc_file",
    )
    selected_file = files[int(selected_index)]
    seq_doc = int(selected_file["sequencialDocumento"])
    download_url = contract_file_download_url(cnpj, contract_year, sequencial, seq_doc)

    action_cols = st.columns([3, 1])
    action_cols[0].caption(_document_label(selected_file))
    action_cols[1].link_button("Abrir arquivo", download_url)


def _render_cnpj_enrichment(contract: dict[str, Any]) -> None:
    st.subheader("Enriquecimento cadastral")
    targets = _cnpj_enrichment_targets(contract)
    if not targets:
        st.info("Nenhum CNPJ de orgao ou fornecedor disponivel para enriquecimento.")
        return

    target_index = st.selectbox(
        "CNPJ para enriquecer",
        range(len(targets)),
        format_func=lambda index: f"{targets[index]['label']} | {targets[index]['cnpj']}",
        key="cnpj_enrichment_target",
    )
    target = targets[int(target_index)]
    context = (target["role"], target["cnpj"], str(contract.get("numeroControlePNCP", "")))

    if st.button("Consultar BrasilAPI", type="secondary", key="cnpj_enrichment_fetch"):
        try:
            with st.spinner("Consultando CNPJ na BrasilAPI..."):
                st.session_state["cnpj_enrichment_record"] = cached_cnpj_enrichment(target["cnpj"])
                st.session_state["cnpj_enrichment_context"] = context
        except (BrasilApiError, ValueError) as exc:
            st.error(str(exc))
            return
        except OSError as exc:
            st.error(f"Erro de conexao com a BrasilAPI: {exc}")
            return

    record = st.session_state.get("cnpj_enrichment_record")
    record_context = st.session_state.get("cnpj_enrichment_context")
    if record and record_context == context:
        _render_cnpj_record(record)
    else:
        st.caption("A consulta e sob demanda para preservar controle de coleta e evitar chamadas repetidas.")


def _render_cnpj_record(record: BrasilApiCnpjRecord) -> None:
    summary = _cnpj_record_summary(record)
    st.markdown(f"**Razao social:** {summary['razao_social'] or '-'}")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Situacao", summary["situacao_cadastral"] or "-")
    metric_cols[1].metric("Municipio/UF", summary["municipio_uf"] or "-")
    metric_cols[2].metric("Socios", summary["socios_count"])
    metric_cols[3].metric("Capital social", summary["capital_social"] if summary["capital_social"] is not None else "-")

    st.dataframe(pd.DataFrame([summary]), use_container_width=True, hide_index=True)
    st.caption(f"Fonte: {record.source_url}")
    st.caption(f"Coletado em: {record.collected_at}")
    with st.expander("Payload bruto BrasilAPI"):
        st.json(record.raw_payload)


def _cnpj_enrichment_targets(contract: dict[str, Any]) -> list[dict[str, str]]:
    targets: list[dict[str, str]] = []
    seen: set[str] = set()

    orgao = contract.get("orgaoEntidade") or {}
    _append_cnpj_target(
        targets,
        seen,
        role="orgao",
        label="Orgao contratante",
        cnpj=str(orgao.get("cnpj") or contract.get("cnpjOrgao") or ""),
    )

    supplier_name = str(contract.get("nomeRazaoSocialFornecedor") or "Fornecedor")
    _append_cnpj_target(
        targets,
        seen,
        role="fornecedor",
        label=supplier_name,
        cnpj=str(contract.get("niFornecedor") or ""),
    )

    return targets


def _append_cnpj_target(
    targets: list[dict[str, str]],
    seen: set[str],
    *,
    role: str,
    label: str,
    cnpj: str,
) -> None:
    digits = compact_digits(cnpj)
    if len(digits) != 14 or digits in seen:
        return
    targets.append({"role": role, "label": label, "cnpj": digits})
    seen.add(digits)


def _cnpj_record_summary(record: BrasilApiCnpjRecord) -> dict[str, Any]:
    standardized = record.standardized()
    municipio = str(standardized.get("municipio") or "")
    uf = str(standardized.get("uf") or "")
    municipio_uf = f"{municipio}/{uf}" if municipio or uf else ""
    return {
        "cnpj": standardized["cnpj"],
        "razao_social": standardized["razao_social"],
        "nome_fantasia": standardized["nome_fantasia"],
        "situacao_cadastral": standardized["situacao_cadastral"],
        "municipio_uf": municipio_uf,
        "cnae_fiscal": standardized["cnae_fiscal"],
        "cnae_fiscal_descricao": standardized["cnae_fiscal_descricao"],
        "data_inicio_atividade": standardized["data_inicio_atividade"],
        "capital_social": standardized["capital_social"],
        "socios_count": standardized["socios_count"],
    }


def render_comparison_section() -> None:
    """Render the second workflow step: compare manual data against PNCP."""

    st.header("Comparacao manual")

    input_col, row_col = st.columns([3, 1])
    csv_path = input_col.text_input("Planilha manual (CSV)", value=str(DEFAULT_MANUAL_CSV), key="comp_csv")
    path = Path(csv_path)
    if not path.exists():
        st.warning(f"Planilha nao encontrada: `{path}`")
        return

    rows = load_manual_rows(path)
    if not rows:
        st.warning("A planilha manual esta vazia.")
        return

    by_row = {str(row.get("source_row", index)): row for index, row in enumerate(rows)}
    selected_key = row_col.selectbox(
        "Linha",
        list(by_row),
        format_func=lambda key: _manual_row_label(by_row[key], key),
        key="comp_row",
    )
    manual_row = by_row[selected_key]

    _render_manual_summary(manual_row)
    selected_contract = st.session_state.get("selected_pncp_contract")

    if selected_contract:
        st.markdown("**Contrato selecionado na busca**")
        st.caption(record_label(selected_contract))
        selected_context = (selected_key, str(selected_contract.get("numeroControlePNCP", "")))
        comparison = st.session_state.get("selected_pncp_contract_comparison")
        comparison_context = st.session_state.get("selected_pncp_contract_comparison_context")

        if comparison and comparison_context == selected_context:
            st.caption("Resultado calculado pela priorizacao da busca.")
            _render_single_comparison(
                comparison,
                title="Resultado da comparacao",
                contract=selected_contract,
                key_prefix="selected_ranked",
            )
        else:
            if st.button("Comparar com contrato selecionado", type="primary", key="comp_selected_contract"):
                st.session_state["selected_contract_comparison"] = _compare_manual_with_contract(
                    manual_row, selected_contract
                )
                st.session_state["selected_contract_comparison_context"] = selected_context

            direct_comparison = st.session_state.get("selected_contract_comparison")
            direct_context = st.session_state.get("selected_contract_comparison_context")
            if direct_comparison and direct_context == selected_context:
                _render_single_comparison(
                    direct_comparison,
                    title="Resultado da comparacao",
                    contract=selected_contract,
                    key_prefix="selected_direct",
                )
    else:
        st.info("Selecione um contrato na busca de documentos para comparar diretamente.")

    with st.expander("Investigacao automatica"):
        search_col, window_col, size_col, pages_col = st.columns([1, 1, 1, 1])
        run_search = search_col.button("Buscar candidatos", type="secondary", key="comp_investigate")
        window_days = int(window_col.slider("Janela", 0, 180, 45, step=5, key="comp_window"))
        page_size = int(size_col.slider("Itens", 10, 500, 500, step=10, key="comp_page_size"))
        max_pages = int(pages_col.slider("Paginas", 1, 50, 20, key="comp_max_pages"))

        if run_search:
            try:
                with st.spinner("Buscando e comparando candidatos no PNCP..."):
                    st.session_state["automatic_investigation"] = cached_investigate_row(
                        manual_row, window_days, page_size, max_pages
                    )
            except PncpApiError as exc:
                st.error(str(exc))
                return
            except OSError as exc:
                st.error(f"Erro de conexao com o PNCP: {exc}")
                return

        result = st.session_state.get("automatic_investigation")
        if result and result.source_row == selected_key:
            _render_investigation_result(result)


def _render_manual_summary(manual_row: dict[str, Any]) -> None:
    with st.container(border=True):
        st.markdown("**Registro manual**")
        cols = st.columns(4)
        display_fields = MANUAL_FIELDS[:4]
        for col, (key, label) in zip(cols, display_fields, strict=True):
            col.metric(label, manual_row.get(key, "-") or "-")

        cols = st.columns(3)
        for col, (key, label) in zip(cols, MANUAL_FIELDS[4:], strict=True):
            col.metric(label, manual_row.get(key, "-") or "-")
        st.caption(str(manual_row.get("objeto_contrato") or ""))


def _render_investigation_result(result: InvestigationResult) -> None:
    metric_cols = st.columns(3)
    metric_cols[0].metric("Candidatos", result.candidates_count)
    if result.best is None:
        metric_cols[1].metric("Melhor score", "-")
        metric_cols[2].metric("Campos match", "-")
        st.warning("Nenhum candidato encontrado no PNCP.")
        st.caption(f"Consulta: {result.query_url}")
        return

    matched, total = match_count(result.best)
    metric_cols[1].metric("Melhor score", f"{result.best.overall_score:.2f}")
    metric_cols[2].metric("Campos match", f"{matched}/{total}")
    _render_single_comparison(result.best, title="Melhor candidato", key_prefix="automatic_best")

    st.markdown(f"**Todos os candidatos ({len(result.comparisons)})**")
    df = candidates_dataframe(result.comparisons)
    styled = df.style.map(color_status, subset=["status"]).format({"score": "{:.4f}"})
    st.dataframe(styled, use_container_width=True, hide_index=True)
    st.caption(f"Consulta: {result.query_url}")


def _render_single_comparison(
    comparison: RecordComparison,
    *,
    title: str,
    contract: dict[str, Any] | None = None,
    key_prefix: str = "comparison",
) -> None:
    with st.container(border=True):
        head = st.columns([3, 1])
        head[0].markdown(f"**{title}:** `{comparison.numero_controle_pncp}`")
        head[0].markdown(status_badge(comparison.status), unsafe_allow_html=True)
        url = candidate_detail_url(comparison.numero_controle_pncp)
        if url:
            head[1].link_button("Abrir PNCP", url)

        matched, total = match_count(comparison)
        metrics = st.columns(2)
        metrics[0].metric("Score", f"{comparison.overall_score:.2f}")
        metrics[1].metric("Campos match", f"{matched}/{total}")

        rows_html = "".join(
            field_row_html(field.field_name, field.manual_value, field.official_value, field.status)
            for field in comparison.fields
        )
        st.markdown(rows_html, unsafe_allow_html=True)

        documents = _current_official_documents_for_report(contract)
        enrichments = _current_cnpj_enrichments_for_report(contract)
        review = _review_assessment(comparison, documents)
        review_status, review_notes = _render_review_workflow(
            comparison,
            review,
            key_prefix=key_prefix,
        )
        _render_audit_export(
            comparison,
            documents=documents,
            cnpj_enrichments=enrichments,
            review=review,
            review_status=review_status,
            review_notes=review_notes,
            key_prefix=key_prefix,
        )


def _render_review_workflow(
    comparison: RecordComparison,
    review: dict[str, Any],
    *,
    key_prefix: str,
) -> tuple[str, str]:
    st.markdown("**Revisao operacional**")
    status_key = f"{key_prefix}_review_status_{_safe_key(comparison.numero_controle_pncp)}"
    notes_key = f"{key_prefix}_review_notes_{_safe_key(comparison.numero_controle_pncp)}"

    default_status = "precisa_revisar_documento" if review["document_review_required"] else "pendente"
    current_status = st.session_state.get(status_key, default_status)
    default_index = REVIEW_STATUS_OPTIONS.index(current_status) if current_status in REVIEW_STATUS_OPTIONS else 0

    status_col, doc_col, ocr_col = st.columns([1, 1, 1])
    selected_status = status_col.selectbox(
        "Status",
        REVIEW_STATUS_OPTIONS,
        index=default_index,
        format_func=lambda value: REVIEW_STATUS_LABELS[value],
        key=status_key,
    )
    doc_col.metric("Revisao documental", review["document_review_label"])
    ocr_col.metric("OCR", review["ocr_label"])
    notes = st.text_area("Notas da revisao", key=notes_key, height=80)
    return selected_status, notes


def _render_audit_export(
    comparison: RecordComparison,
    *,
    documents: list[dict[str, Any]],
    cnpj_enrichments: list[dict[str, Any]],
    review: dict[str, Any],
    review_status: str,
    review_notes: str,
    key_prefix: str,
) -> None:
    report = _build_webapp_audit_report(
        comparison,
        official_documents=documents,
        cnpj_enrichments=cnpj_enrichments,
        review=review,
        review_status=review_status,
        review_notes=review_notes,
    )
    markdown = _render_webapp_audit_markdown(report)
    json_data = json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8")
    markdown_data = markdown.encode("utf-8")
    filename_base = _audit_filename_base(comparison)

    st.markdown("**Relatorio auditavel**")
    download_cols = st.columns([1, 1, 2])
    download_cols[0].download_button(
        "Baixar Markdown",
        data=markdown_data,
        file_name=f"{filename_base}.md",
        mime="text/markdown",
        key=f"{key_prefix}_audit_markdown",
    )
    download_cols[1].download_button(
        "Baixar JSON",
        data=json_data,
        file_name=f"{filename_base}.json",
        mime="application/json",
        key=f"{key_prefix}_audit_json",
    )
    download_cols[2].caption(
        f"Exporta {len(documents)} documentos oficiais e {len(cnpj_enrichments)} enriquecimentos CNPJ."
    )


def _build_webapp_audit_report(
    comparison: RecordComparison,
    *,
    official_documents: list[dict[str, Any]] | None = None,
    cnpj_enrichments: list[dict[str, Any]] | None = None,
    review: dict[str, Any] | None = None,
    review_status: str = "pendente",
    review_notes: str = "",
) -> dict[str, Any]:
    report = build_audit_report(
        [_comparison_to_report_dict(comparison)],
        official_documents=official_documents or [],
        cnpj_enrichments=cnpj_enrichments or [],
        title=f"Relatorio Auditavel - Linha {comparison.source_row}",
    )
    report["review_workflow"] = {
        "review_status": review_status,
        "review_status_label": REVIEW_STATUS_LABELS.get(review_status, review_status),
        "review_notes": review_notes,
        **(review or _review_assessment(comparison, official_documents or [])),
    }
    return report


def _render_webapp_audit_markdown(report: dict[str, Any]) -> str:
    markdown = render_audit_report_markdown(report)
    review = report.get("review_workflow") or {}
    lines = [
        "",
        "## Revisao Operacional",
        "",
        f"- Status: `{review.get('review_status_label', '')}`",
        f"- Revisao documental: `{review.get('document_review_label', '')}`",
        f"- OCR: `{review.get('ocr_label', '')}`",
        f"- Campos para revisao: `{review.get('review_fields_count', 0)}`",
    ]
    notes = str(review.get("review_notes") or "").strip()
    if notes:
        lines.append(f"- Notas: {notes}")
    return markdown + "\n".join(lines) + "\n"


def _comparison_to_report_dict(comparison: RecordComparison) -> dict[str, Any]:
    return {
        "source_row": comparison.source_row,
        "numero_controle_pncp": comparison.numero_controle_pncp,
        "overall_score": comparison.overall_score,
        "status": comparison.status,
        "fields": [
            {
                "field_name": field.field_name,
                "manual_value": field.manual_value,
                "official_value": field.official_value,
                "status": field.status,
                "similarity_score": field.similarity_score,
                "manual_evidence_id": field.manual_evidence_id,
                "official_evidence_id": field.official_evidence_id,
                "notes": field.notes,
            }
            for field in comparison.fields
        ],
    }


def _review_assessment(comparison: RecordComparison, documents: list[dict[str, Any]]) -> dict[str, Any]:
    return assess_review_needs(comparison, documents).to_dict()


def _current_official_documents_for_report(contract: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not contract:
        return []
    context = str(contract.get("numeroControlePNCP", ""))
    if st.session_state.get("selected_pncp_contract_files_context") != context:
        return []
    files = st.session_state.get("selected_pncp_contract_files") or []
    return _official_documents_for_report(contract, files)


def _official_documents_for_report(contract: dict[str, Any], files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cnpj, contract_year, sequencial = _contract_parts(contract)
    resource_id = f"{cnpj}/{contract_year}/{sequencial}"
    documents: list[dict[str, Any]] = []
    for file_record in files:
        if not isinstance(file_record, dict):
            continue
        document = dict(file_record)
        document["source"] = document.get("source") or "pncp"
        document["resource_type"] = document.get("resource_type") or "contract"
        document["resource_id"] = document.get("resource_id") or resource_id
        document["numero_controle_pncp"] = str(contract.get("numeroControlePNCP", ""))
        seq_doc = _optional_int(document.get("sequencialDocumento"))
        if seq_doc is not None and not document.get("url"):
            document["url"] = contract_file_download_url(cnpj, contract_year, sequencial, seq_doc)
        documents.append(document)
    return documents


def _current_cnpj_enrichments_for_report(contract: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not contract:
        return []
    record = st.session_state.get("cnpj_enrichment_record")
    context = st.session_state.get("cnpj_enrichment_context")
    contract_number = str(contract.get("numeroControlePNCP", ""))
    if not record or not context or context[2] != contract_number:
        return []

    role = str(context[0])
    if isinstance(record, BrasilApiCnpjRecord):
        enrichment = record.to_dict()
    elif isinstance(record, dict):
        enrichment = dict(record)
    else:
        return []
    enrichment["role"] = role
    return [enrichment]


def _audit_filename_base(comparison: RecordComparison) -> str:
    row = _safe_key(comparison.source_row or "linha")
    numero = _safe_key(comparison.numero_controle_pncp or "sem_pncp")
    return f"relatorio-auditavel-row{row}-{numero}"


def _safe_key(value: Any) -> str:
    text = str(value or "")
    clean = "".join(char if char.isalnum() else "_" for char in text)
    return "_".join(part for part in clean.split("_") if part) or "item"


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _compare_manual_with_contract(manual_row: dict[str, Any], contract: dict[str, Any]) -> RecordComparison:
    numero = str(contract.get("numeroControlePNCP", ""))
    url = candidate_detail_url(numero) or ""
    return compare_manual_record(
        manual_row,
        contract,
        source_url=url,
        method="pncp_contract_selected_in_webapp",
    )


def _contract_parts(contract: dict[str, Any]) -> tuple[str, int, int]:
    orgao = contract.get("orgaoEntidade") or {}
    cnpj = str(orgao.get("cnpj") or contract.get("cnpjOrgao") or "")
    contract_year = int(contract.get("anoContrato") or 0)
    sequencial = int(contract.get("sequencialContrato") or 0)
    return cnpj, contract_year, sequencial


def _document_row(file_record: dict[str, Any]) -> dict[str, Any]:
    return {
        "sequencial": file_record.get("sequencialDocumento"),
        "titulo": file_record.get("titulo"),
        "tipo": file_record.get("tipoDocumentoNome"),
        "publicado": file_record.get("dataPublicacaoPncp") or file_record.get("dataPublicacao"),
    }


def _document_label(file_record: dict[str, Any]) -> str:
    seq_doc = file_record.get("sequencialDocumento")
    title = file_record.get("titulo") or f"Documento {seq_doc}"
    doc_type = file_record.get("tipoDocumentoNome") or "Documento"
    return f"{seq_doc} | {doc_type} | {title}"


def _manual_row_label(row: dict[str, Any], key: str) -> str:
    municipio = row.get("municipio", "")
    uf = row.get("uf", "")
    objeto = str(row.get("objeto_contrato", ""))[:48]
    return f"Linha {key} | {municipio}/{uf} | {objeto}"
