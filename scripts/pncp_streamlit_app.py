"""Streamlit app for exploring PNCP contracts."""

from __future__ import annotations

import streamlit as st

from sherlock_holmes.pncp.client import PncpApiError, compact_digits
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


def main() -> None:
    st.set_page_config(page_title="Explorador PNCP", layout="wide")
    st.title("Explorador PNCP")

    with st.sidebar:
        preset = st.selectbox("Órgão", ["Manual", *PRESET_ORGAOS.keys()])
        default_cnpj = PRESET_ORGAOS.get(preset, {}).get("cnpj", "")
        default_unidade = PRESET_ORGAOS.get(preset, {}).get("unidade", "")

        cnpj_orgao = st.text_input("CNPJ do órgão", value=default_cnpj)
        codigo_unidade = st.text_input("Código da unidade", value=default_unidade)
        year = st.number_input("Ano", min_value=2021, max_value=2100, value=2025, step=1)
        page_size = st.slider("Tamanho da página", min_value=10, max_value=500, value=500, step=10)
        max_pages = st.slider("Máximo de páginas", min_value=1, max_value=100, value=20)

        st.divider()
        topic = st.text_input("Tema para filtrar", value="limpeza")
        suggestions = suggested_terms(topic)
        selected_terms = st.multiselect("Palavras sugeridas", suggestions, default=suggestions)
        custom_terms = st.text_input("Palavras extras separadas por vírgula")
        terms = selected_terms + [term.strip() for term in custom_terms.split(",") if term.strip()]

        search = st.button("Buscar contratos", type="primary")

        st.divider()
        st.page_link("pages/comparacao_manual_pncp.py", label="Comparação Manual vs PNCP")

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

    st.subheader("Contratos")
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

    st.subheader("Arquivos do contrato")
    selected = st.selectbox("Contrato", filtered_records, format_func=record_label)
    cnpj = selected["orgaoEntidade"]["cnpj"]
    contract_year = int(selected["anoContrato"])
    sequencial = int(selected["sequencialContrato"])
    detail_url = contract_detail_url(cnpj, contract_year, sequencial)

    st.link_button("Abrir detalhe PNCP", detail_url)

    try:
        with st.spinner("Buscando arquivos do contrato..."):
            files_result = cached_contract_files(cnpj, contract_year, sequencial)
    except PncpApiError as exc:
        st.error(str(exc))
        return
    except OSError as exc:
        st.error(f"Erro de conexão com o PNCP: {exc}")
        return

    st.caption(f"Arquivos: {files_result['url']}")
    files = files_result["payload"] if isinstance(files_result["payload"], list) else []
    if not files:
        st.info("Nenhum arquivo encontrado para esse contrato.")
        return

    for file_record in files:
        sequencial_documento = int(file_record["sequencialDocumento"])
        download_url = contract_file_download_url(cnpj, contract_year, sequencial, sequencial_documento)
        title = file_record.get("titulo") or f"Documento {sequencial_documento}"
        doc_type = file_record.get("tipoDocumentoNome") or "Documento"
        st.markdown(f"**{title}**  \n{doc_type}  \n[abrir/baixar arquivo]({download_url})")


if __name__ == "__main__":
    main()
