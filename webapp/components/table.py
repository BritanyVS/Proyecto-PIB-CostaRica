import pandas as pd
import streamlit as st


TABLE_STYLE = [
    {"selector": "thead th", "props": [("background-color", "#e3f7e7"), ("color", "#284332"), ("font-weight", "700"), ("border", "1px solid #dfeee2")]},
    {"selector": "tbody td", "props": [("background-color", "#ffffff"), ("color", "#284332"), ("border", "1px solid #edf4ee")]},
    {"selector": "tbody tr:nth-child(even) td", "props": [("background-color", "#f8fcf8")]},
    {"selector": "th", "props": [("font-family", "Segoe UI, sans-serif"), ("padding", "0.45rem 0.6rem")]},
    {"selector": "td", "props": [("font-family", "Segoe UI, sans-serif"), ("padding", "0.45rem 0.6rem")]},
]


def render_date_filter(data: pd.DataFrame) -> pd.DataFrame:
    st.markdown("### Filtro por año")

    years = sorted(data["Fecha"].dt.year.dropna().unique().tolist())
    if "year_filter_mode" not in st.session_state:
        st.session_state.year_filter_mode = "year"
    if "selected_year" not in st.session_state:
        st.session_state.selected_year = years[-1]
    if "last_selected_year" not in st.session_state:
        st.session_state.last_selected_year = st.session_state.selected_year

    left, right = st.columns([2, 1])
    with left:
        selected_year = st.selectbox("Selecciona un año", years, index=years.index(st.session_state.selected_year))
    with right:
        clear_clicked = st.button("Limpiar filtro")

    if clear_clicked:
        st.session_state.year_filter_mode = "all"
    elif selected_year != st.session_state.last_selected_year:
        st.session_state.year_filter_mode = "year"
        st.session_state.selected_year = selected_year
        st.session_state.last_selected_year = selected_year

    if st.session_state.year_filter_mode == "all":
        filtered = data.copy()
        filter_label = "Sin filtro"
        visible_label = "Todos los registros"
    else:
        filtered = data[data["Fecha"].dt.year == selected_year].copy()
        filter_label = "Solo por año"
        visible_label = str(selected_year)

    st.metric("Registros totales", len(data))

    summary_cols = st.columns(3)
    summary_cols[0].metric("Registros visibles", len(filtered))
    summary_cols[1].metric("Año seleccionado", visible_label)
    summary_cols[2].metric("Filtro", filter_label)

    return filtered


def render_table(data: pd.DataFrame) -> None:
    display_data = data.copy()
    display_data["Fecha"] = display_data["Fecha"].dt.strftime("%Y-%m-%d")
    styled_data = display_data.style.set_table_styles(TABLE_STYLE)
    st.dataframe(styled_data, use_container_width=True, height=700)