"""Streamlit tab renderers for the Sherlock Holmes app."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from sherlock_holmes.investigation import (
    InvestigationResult,
    investigate_row,
    load_manual_rows,
)
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
    records_to_dataframe,
    suggested_terms,
)
from sherlock_holmes.webapp.ui import color_status, field_row_html, status_badge

ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_MANUAL_CSV = ROOT_DIR / "documentation" / "plans" / "pncp-api-smoke-sample.csv"


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


# --------------------------------------------------------------------------- #
# Tab: Comparação (live investigation)
# --------------------------------------------------------------------------- #

def render_comparacao_tab() -> None:
    st.subheader("Investigação ao vivo: planilha manual vs PNCP")

    with st.sidebar:
        st.markdown("### Comparação")
        csv_path = st.text_input(
            "Planilha manual (CSV)", value=str(DEFAULT_MANUAL_CSV), key="comp_csv"
        )
        with st.expander("Parâmetros da busca"):
            window_days = st.slider(
                "Janela de dias (± vigência início)", 0, 180, 45, step=5, key="comp_window"
            )
            page_size = st.slider("Tamanho da página", 10, 500, 500, step=10, key="comp_page_size")
            max_pages = st.slider("Máximo de páginas", 1, 50, 20, key="comp_max_pages")

    path = Path(csv_path)
    if not path.exists():
        st.error(f"Planilha não encontrada: `{path}`")
        return

    rows = load_manual_rows(path)
    if not rows:
        st.warning("A planilha manual está vazia.")
        return

    by_row = {str(r.get("source_row", i)): r for i, r in enumerate(rows)}

    def _row_label(key: str) -> str:
        r = by_row[key]
        return f"Linha {key} · {r.get('municipio', '')}/{r.get('uf', '')} · {r.get('objeto_contrato', '')[:40]}"

    selected_key = st.selectbox(
        "Linha da planilha", list(by_row), format_func=_row_label, key="comp_row"
    )
    manual_row = by_row[selected_key]

    if st.button("🔎 Investigar no PNCP", type="primary", key="comp_investigar"):
        st.session_state["investigation_key"] = selected_key

    if st.session_state.get("investigation_key") != selected_key:
        st.info("Selecione uma linha e clique em **Investigar no PNCP**.")
        return

    try:
        with st.spinner("Buscando e comparando candidatos no PNCP..."):
            result = cached_investigate_row(manual_row, window_days, page_size, max_pages)
    except PncpApiError as exc:
        st.error(str(exc))
        return
    except OSError as exc:
        st.error(f"Erro de conexão com o PNCP: {exc}")
        return

    _render_manual_card(manual_row)
    _render_summary_metrics(result)

    if result.best is None:
        st.warning("Nenhum candidato encontrado no PNCP para essa linha e janela de datas.")
        st.caption(f"Consulta: {result.query_url}")
        return

    _render_best_candidate(result)
    _render_all_candidates(result)
    st.caption(f"Consulta: {result.query_url}")


def _render_manual_card(manual_row: dict) -> None:
    with st.container(border=True):
        st.markdown("**Registro manual**")
        cols = st.columns(len(MANUAL_FIELDS))
        for col, (key, label) in zip(cols, MANUAL_FIELDS, strict=True):
            col.metric(label, manual_row.get(key, "—") or "—")
        st.caption(f"Objeto: {manual_row.get('objeto_contrato', '—')}")


def _render_summary_metrics(result: InvestigationResult) -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Candidatos avaliados", result.candidates_count)
    if result.best is not None:
        matched, total = match_count(result.best)
        col2.metric("Melhor score", f"{result.best.overall_score:.2f}")
        col3.metric("Campos coincidentes", f"{matched}/{total}")
    else:
        col2.metric("Melhor score", "—")
        col3.metric("Campos coincidentes", "—")


def _render_best_candidate(result: InvestigationResult) -> None:
    best = result.best
    assert best is not None
    with st.container(border=True):
        head = st.columns([3, 1])
        head[0].markdown(f"**Melhor candidato:** `{best.numero_controle_pncp}`")
        head[0].markdown(status_badge(best.status), unsafe_allow_html=True)
        url = candidate_detail_url(best.numero_controle_pncp)
        if url:
            head[1].link_button("Abrir no PNCP", url)

        rows_html = "".join(
            field_row_html(f.field_name, f.manual_value, f.official_value, f.status)
            for f in best.fields
        )
        st.markdown(rows_html, unsafe_allow_html=True)


def _render_all_candidates(result: InvestigationResult) -> None:
    with st.expander(f"Todos os candidatos ({len(result.comparisons)})"):
        df = candidates_dataframe(result.comparisons)
        styled = df.style.map(color_status, subset=["status"]).format({"score": "{:.4f}"})
        st.dataframe(styled, use_container_width=True, hide_index=True)

        numeros = [c.numero_controle_pncp for c in result.comparisons]
        chosen = st.selectbox("Inspecionar candidato", numeros, key="comp_inspect")
        chosen_cmp = next(c for c in result.comparisons if c.numero_controle_pncp == chosen)
        rows_html = "".join(
            field_row_html(f.field_name, f.manual_value, f.official_value, f.status)
            for f in chosen_cmp.fields
        )
        st.markdown(rows_html, unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Tab: Busca (live PNCP explorer)
# --------------------------------------------------------------------------- #

def render_busca_tab() -> None:
    st.subheader("Explorador PNCP")

    with st.sidebar:
        st.markdown("### Busca")
        preset = st.selectbox("Órgão", ["Manual", *PRESET_ORGAOS.keys()], key="busca_preset")
        default_cnpj = PRESET_ORGAOS.get(preset, {}).get("cnpj", "")
        default_unidade = PRESET_ORGAOS.get(preset, {}).get("unidade", "")

        cnpj_orgao = st.text_input("CNPJ do órgão", value=default_cnpj, key="busca_cnpj")
        codigo_unidade = st.text_input("Código da unidade", value=default_unidade, key="busca_unidade")
        year = st.number_input("Ano", min_value=2021, max_value=2100, value=2025, step=1, key="busca_year")
        page_size = st.slider(
            "Tamanho da página", min_value=10, max_value=500, value=500, step=10, key="busca_page_size"
        )
        max_pages = st.slider("Máximo de páginas", min_value=1, max_value=100, value=20, key="busca_max_pages")

        topic = st.text_input("Tema para filtrar", value="limpeza", key="busca_topic")
        suggestions = suggested_terms(topic)
        selected_terms = st.multiselect(
            "Palavras sugeridas", suggestions, default=suggestions, key="busca_terms"
        )
        custom_terms = st.text_input("Palavras extras separadas por vírgula", key="busca_custom")
        terms = selected_terms + [t.strip() for t in custom_terms.split(",") if t.strip()]

        search = st.button("Buscar contratos", type="primary", key="busca_search")

    if not compact_digits(cnpj_orgao):
        st.info("Informe o CNPJ do órgão para começar.")
        return

    if search:
        st.session_state["last_search"] = {
            "year": int(year),
            "cnpj_orgao": cnpj_orgao,
            "codigo_unidade": codigo_unidade,
            "page_size": page_size,
            "max_pages": max_pages,
        }

    search_params = st.session_state.get("last_search")
    if not search_params:
        st.info("Configure a busca na lateral e clique em Buscar contratos.")
        return

    try:
        with st.spinner("Consultando contratos no PNCP..."):
            result = cached_contract_search(**search_params)
    except PncpApiError as exc:
        st.error(str(exc))
        return
    except OSError as exc:
        st.error(f"Erro de conexão com o PNCP: {exc}")
        return

    payload = result["payload"]
    records = payload.get("data", []) if isinstance(payload, dict) else []
    filtered_records = filter_records_by_terms(records, terms)

    st.caption(f"Consulta: {result['url']}")
    col_total, col_filtered = st.columns(2)
    col_total.metric("Contratos encontrados", len(records))
    col_filtered.metric("Após filtro", len(filtered_records))

    if not records:
        st.warning("Nenhum contrato encontrado para esses parâmetros.")
        return

    dataframe = records_to_dataframe(filtered_records)
    st.dataframe(dataframe, use_container_width=True, hide_index=True)

    csv_data = dataframe.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Baixar CSV filtrado",
        data=csv_data,
        file_name=f"pncp-contratos-{search_params['cnpj_orgao']}-{search_params['year']}.csv",
        mime="text/csv",
    )

    if not filtered_records:
        st.info("Nenhum contrato passou pelo filtro de palavras-chave.")
        return

    with st.container(border=True):
        st.markdown("**Arquivos do contrato**")
        selected = st.selectbox("Contrato", filtered_records, format_func=record_label, key="busca_contract")
        cnpj = selected["orgaoEntidade"]["cnpj"]
        contract_year = int(selected["anoContrato"])
        sequencial = int(selected["sequencialContrato"])
        st.link_button("Abrir detalhe PNCP", contract_detail_url(cnpj, contract_year, sequencial))

        try:
            with st.spinner("Buscando arquivos do contrato..."):
                files_result = cached_contract_files(cnpj, contract_year, sequencial)
        except PncpApiError as exc:
            st.error(str(exc))
            return
        except OSError as exc:
            st.error(f"Erro de conexão com o PNCP: {exc}")
            return

        files = files_result["payload"] if isinstance(files_result["payload"], list) else []
        if not files:
            st.info("Nenhum arquivo encontrado para esse contrato.")
            return

        for file_record in files:
            seq_doc = int(file_record["sequencialDocumento"])
            download_url = contract_file_download_url(cnpj, contract_year, sequencial, seq_doc)
            title = file_record.get("titulo") or f"Documento {seq_doc}"
            doc_type = file_record.get("tipoDocumentoNome") or "Documento"
            st.markdown(f"**{title}**  \n{doc_type}  \n[abrir/baixar arquivo]({download_url})")
