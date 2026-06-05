"""Streamlit renderers for the document-first Sherlock Holmes workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from sherlock_holmes.investigation import (
    InvestigationResult,
    investigate_row,
    load_manual_rows,
)
from sherlock_holmes.pncp.client import PncpApiError, compact_digits
from sherlock_holmes.validation import (
    RecordComparison,
    compare_records,
    evidence_from_manual_spreadsheet,
    evidence_from_official_api,
)
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

    try:
        with st.spinner("Buscando arquivos do contrato..."):
            files_result = cached_contract_files(cnpj, contract_year, sequencial)
    except PncpApiError as exc:
        st.error(str(exc))
        return
    except OSError as exc:
        st.error(f"Erro de conexao com o PNCP: {exc}")
        return

    files = files_result["payload"] if isinstance(files_result["payload"], list) else []
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
            _render_single_comparison(comparison, title="Resultado da comparacao")
        else:
            if st.button("Comparar com contrato selecionado", type="primary", key="comp_selected_contract"):
                st.session_state["selected_contract_comparison"] = _compare_manual_with_contract(
                    manual_row, selected_contract
                )
                st.session_state["selected_contract_comparison_context"] = selected_context

            direct_comparison = st.session_state.get("selected_contract_comparison")
            direct_context = st.session_state.get("selected_contract_comparison_context")
            if direct_comparison and direct_context == selected_context:
                _render_single_comparison(direct_comparison, title="Resultado da comparacao")
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
    _render_single_comparison(result.best, title="Melhor candidato")

    st.markdown(f"**Todos os candidatos ({len(result.comparisons)})**")
    df = candidates_dataframe(result.comparisons)
    styled = df.style.map(color_status, subset=["status"]).format({"score": "{:.4f}"})
    st.dataframe(styled, use_container_width=True, hide_index=True)
    st.caption(f"Consulta: {result.query_url}")


def _render_single_comparison(comparison: RecordComparison, *, title: str) -> None:
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


def _compare_manual_with_contract(manual_row: dict[str, Any], contract: dict[str, Any]) -> RecordComparison:
    source_row = str(manual_row.get("source_row", ""))
    numero = str(contract.get("numeroControlePNCP", ""))
    url = candidate_detail_url(numero) or ""

    manual_evidence = evidence_from_manual_spreadsheet(
        evidence_id=f"manual_row{source_row}",
        field_name="",
        value=manual_row,
        source_row=source_row,
    )
    official_evidence = evidence_from_official_api(
        evidence_id=f"pncp_{numero}",
        source_url=url,
        method="pncp_contract_selected_in_webapp",
        value=contract,
        metadata={"numeroControlePNCP": numero},
    )
    return compare_records(
        source_row=source_row,
        manual_record=manual_row,
        pncp_record=contract,
        manual_evidence=manual_evidence,
        official_evidence=official_evidence,
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
