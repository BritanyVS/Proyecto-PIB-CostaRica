from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from ..config import PALETA

TABLE_STYLE = [
    {"selector": "thead th", "props": [("background-color", "#e3f7e7"), ("color", "#284332"), ("font-weight", "700"), ("border", "1px solid #dfeee2")]},
    {"selector": "tbody td", "props": [("background-color", "#ffffff"), ("color", "#284332"), ("border", "1px solid #edf4ee")]},
    {"selector": "tbody tr:nth-child(even) td", "props": [("background-color", "#f8fcf8")]},
    {"selector": "th", "props": [("font-family", "Segoe UI, sans-serif"), ("padding", "0.45rem 0.6rem")]},
    {"selector": "td", "props": [("font-family", "Segoe UI, sans-serif"), ("padding", "0.45rem 0.6rem")]},
]

SECTORES_PIB = [
    "Agricultura", "Minas", "Manufactura", "Electricidad_Agua",
    "Construccion", "Comercio", "Transporte", "Alojamiento",
    "Telecomunicaciones", "Financieras", "Inmobiliarias",
    "Profesionales", "Admin_Publica", "Educacion_Salud", "Otras",
]

COLORES_SECTORES = [
    "#284332", "#e67e22", "#2980b9", "#c0392b", "#8e44ad",
    "#27ae60", "#d35400", "#1abc9c", "#2c3e50", "#f39c12",
    "#7f8c8d", "#16a085", "#3498db", "#e74c3c", "#95a5a6",
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
        selected_year = st.selectbox("Selecciona un año", years, index=years.index(st.session_state.selected_year), key="year_select")
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

    st.metric("Registros totales", len(data), help="Cantidad total de trimestres en la base")

    summary_cols = st.columns(3)
    summary_cols[0].metric("Registros visibles", len(filtered), help="Trimestres mostrados segun filtro")
    summary_cols[1].metric("Año seleccionado", visible_label)
    summary_cols[2].metric("Filtro", filter_label)

    return filtered


def render_table(data: pd.DataFrame) -> None:
    display_data = data.copy()
    display_data["Fecha"] = display_data["Fecha"].dt.strftime("%Y-%m-%d")
    styled_data = display_data.style.set_table_styles(TABLE_STYLE)
    st.dataframe(styled_data, use_container_width=True, height=550)


def render_pie_chart(data: pd.DataFrame) -> None:
    st.markdown("### Distribucion del PIB por sector economico")

    years = sorted(data["Fecha"].dt.year.dropna().unique().tolist())
    default_year = years[-1] if years else None

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        pie_year = st.selectbox("Selecciona año para el grafico", years, index=len(years) - 1, key="pie_year")

    year_data = data[data["Fecha"].dt.year == pie_year]

    if year_data.empty:
        st.info("No hay datos para el año seleccionado.")
        return

    last_row = year_data.iloc[-1]
    valores = {s: last_row[s] for s in SECTORES_PIB if s in data.columns and pd.notna(last_row.get(s, None)) and last_row[s] > 0}

    if not valores:
        st.info("No hay datos de sectores disponibles para este año.")
        return

    df_pie = pd.DataFrame({"Sector": list(valores.keys()), "Valor": list(valores.values())})
    df_pie["Sector"] = df_pie["Sector"].str.replace("_", " ")

    total_pib = sum(valores.values())

    fig = px.pie(
        df_pie,
        names="Sector",
        values="Valor",
        color_discrete_sequence=COLORES_SECTORES,
        hole=0.4,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Valor: %{value:,.2f}<br>Participacion: %{percent}",
    )
    fig.add_annotation(
        text=f"PIB {pie_year}<br>{total_pib:,.2f}",
        x=0.5, y=0.5,
        font=dict(size=16, color="#284332", family="Segoe UI, sans-serif"),
        showarrow=False,
        align="center",
        xanchor="center",
        yanchor="middle",
    )
    fig.update_layout(
        height=480,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    sectores_ord = sorted(valores.items(), key=lambda x: x[1], reverse=True)
    pct_mayor = sectores_ord[0][1] / total_pib * 100
    pct_menor = sectores_ord[-1][1] / total_pib * 100

    st.markdown(f"""\
<div style="display:flex; gap:1rem; flex-wrap:wrap; margin:0.5rem 0;">
<div style="flex:1; min-width:200px; background:#e3f7e7; border-radius:12px; padding:0.8rem;">
<strong style="color:#284332;">PIB total {pie_year}</strong><br>
<span style="font-size:1.4rem; font-weight:700;">{total_pib:,.2f}</span>
</div>
<div style="flex:1; min-width:200px; background:#fef9e7; border-radius:12px; padding:0.8rem;">
<strong style="color:#b7950b;">Mayor aporte</strong><br>
<span>{sectores_ord[0][0].replace('_', ' ')}: {pct_mayor:.1f}%</span>
</div>
<div style="flex:1; min-width:200px; background:#fdedec; border-radius:12px; padding:0.8rem;">
<strong style="color:#c0392b;">Menor aporte</strong><br>
<span>{sectores_ord[-1][0].replace('_', ' ')}: {pct_menor:.1f}%</span>
</div>
<div style="flex:1; min-width:200px; background:#eaf2f8; border-radius:12px; padding:0.8rem;">
<strong style="color:#2980b9;">Sectores reportados</strong><br>
<span>{len(valores)} de {len(SECTORES_PIB)}</span>
</div>
</div>\
""", unsafe_allow_html=True)


def render_info_database(data: pd.DataFrame) -> None:
    st.markdown("### Informacion de la base de datos")

    years = sorted(data["Fecha"].dt.year.dropna().unique().tolist())
    total_sectores = len([c for c in SECTORES_PIB if c in data.columns])
    periodos = f"{years[0]} - {years[-1]}" if years else "N/A"
    total_trimestres = len(data)

    st.markdown(f"""\
<div style="display:flex; gap:1rem; flex-wrap:wrap; margin:0.5rem 0;">
<div style="flex:1; min-width:160px; background:#d5f5e3; border-radius:12px; padding:1rem; color:#1a3c2a; border-left:4px solid #1a7a3a;">
<div style="font-size:0.7rem; font-weight:600; text-transform:uppercase; opacity:0.7;">Periodo</div>
<div style="font-size:1.35rem; font-weight:700;">{periodos}</div>
</div>
<div style="flex:1; min-width:160px; background:#d6eaf8; border-radius:12px; padding:1rem; color:#1a3c2a; border-left:4px solid #2980b9;">
<div style="font-size:0.7rem; font-weight:600; text-transform:uppercase; opacity:0.7;">Trimestres</div>
<div style="font-size:1.35rem; font-weight:700;">{total_trimestres}</div>
</div>
<div style="flex:1; min-width:160px; background:#e8daef; border-radius:12px; padding:1rem; color:#1a3c2a; border-left:4px solid #8e44ad;">
<div style="font-size:0.7rem; font-weight:600; text-transform:uppercase; opacity:0.7;">Sectores</div>
<div style="font-size:1.35rem; font-weight:700;">{total_sectores}</div>
</div>
<div style="flex:1; min-width:160px; background:#d1f2eb; border-radius:12px; padding:1rem; color:#1a3c2a; border-left:4px solid #1abc9c;">
<div style="font-size:0.7rem; font-weight:600; text-transform:uppercase; opacity:0.7;">Fuente</div>
<div style="font-size:1.35rem; font-weight:700;">Banco Central</div>
</div>
</div>
<div style="background:#f8fcf8; border:1px solid #dfeee2; border-radius:12px; padding:1rem; margin:0.5rem 0;">
<strong style="color:#284332;">Acerca de los datos</strong><br>
<span style="color:#284332;">
Esta base contiene el <strong>Producto Interno Bruto (PIB) de Costa Rica</strong> desagregado por
<strong>actividad economica</strong>, con periodicidad <strong>trimestral</strong>. Los datos son publicados
por el <strong>Banco Central de Costa Rica</strong> y comprenden el periodo {periodos}.
Las variables incluyen el PIB a precios de mercado, el valor agregado bruto, los impuestos sobre los productos,
y el detalle de <strong>{total_sectores} sectores productivos</strong> que componen la economia nacional.
</span>
</div>\
""", unsafe_allow_html=True)
