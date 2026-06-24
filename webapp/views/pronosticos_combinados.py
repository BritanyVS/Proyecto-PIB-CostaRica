from __future__ import annotations

import pandas as pd
import streamlit as st

from ..methods.promedio_movil import PromedioMovil
from ..methods.regresion_lineal import RegresionLineal
from ..methods.suavizamiento_exponencial import SuavizamientoExponencial


SECTORES_PIB = [
    "Agricultura", "Minas", "Manufactura", "Electricidad_Agua",
    "Construccion", "Comercio", "Transporte", "Alojamiento",
    "Telecomunicaciones", "Financieras", "Inmobiliarias",
    "Profesionales", "Admin_Publica", "Educacion_Salud", "Otras",
]


def _interpretar_r2(r2: float) -> str:
    if r2 >= 0.90:
        return "Excelente"
    if r2 >= 0.75:
        return "Buena"
    if r2 >= 0.50:
        return "Moderada"
    return "Baja"


def _color_r2(r2: float) -> str:
    if r2 >= 0.90:
        return "#1a7a3a"
    if r2 >= 0.75:
        return "#2d8a4e"
    if r2 >= 0.50:
        return "#cc8b00"
    return "#b33c1a"


def render_pronosticos_combinados_view(data: pd.DataFrame) -> None:
    st.markdown("### Pronosticos combinados")
    st.caption("Visualiza promedio movil, suavizamiento exponencial y regresion lineal de un mismo sector en un solo grafico.")

    numeric_columns = [c for c in data.columns if c != "Fecha"]
    default_col = "PIB_Precios_Mercado" if "PIB_Precios_Mercado" in numeric_columns else numeric_columns[0]

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        selected_column = st.selectbox("Sector economico", numeric_columns, index=numeric_columns.index(default_col), key="pron_combo_sector")
    with col2:
        window = st.slider("Ventana PM", min_value=2, max_value=12, value=4, step=1, key="pron_combo_window")
    with col3:
        alpha = st.slider("Alpha SE", min_value=0.05, max_value=1.0, value=0.3, step=0.05, key="pron_combo_alpha")

    base = data[["Fecha", selected_column]].dropna().copy().reset_index(drop=True)

    pm = PromedioMovil(data, selected_column, window).calculate()
    se = SuavizamientoExponencial(data, selected_column, alpha).calculate()
    rl = RegresionLineal(data, selected_column).calculate()

    slope = rl.attrs.get("slope", 0.0)
    intercept = rl.attrs.get("intercept", 0.0)
    r2 = rl.attrs.get("r_squared", 0.0)

    chart = base.merge(pm[["Fecha", "Promedio_Movil"]], on="Fecha", how="left")
    chart = chart.merge(se[["Fecha", "Suavizamiento_Exponencial"]], on="Fecha", how="left")
    chart = chart.merge(rl[["Fecha", "Valor_Predicho"]], on="Fecha", how="left")

    chart_styled = chart.set_index("Fecha")[[
        selected_column, "Promedio_Movil", "Suavizamiento_Exponencial", "Valor_Predicho"
    ]].rename(columns={
        selected_column: "Original",
        "Promedio_Movil": "Promedio Movil",
        "Suavizamiento_Exponencial": "Suav. Exponencial",
        "Valor_Predicho": "Regresion Lineal",
    })

    LISTA_COLORES = ["#284332", "#e67e22", "#2980b9", "#c0392b"]

    st.line_chart(chart_styled, color=LISTA_COLORES, use_container_width=True, height=450)

    interp = _interpretar_r2(r2)
    color_r2 = _color_r2(r2)
    ultimo_orig = base[selected_column].iloc[-1]

    cols = st.columns(4)
    cols[0].metric("Sector", selected_column.replace("_", " "))
    cols[1].metric("Ultimo valor", f"{ultimo_orig:,.2f}")
    cols[2].metric("Pendiente RL", f"{slope:,.4f}")
    cols[3].metric("R²", f"{r2:.4f}")

    st.markdown(f"""\
<div style="background:{color_r2}15; border-left:5px solid {color_r2}; border-radius:10px; padding:0.8rem 1.2rem; margin:0.5rem 0;">
<strong style="color:{color_r2}; font-size:1.05rem;">Interpretacion del R²: {interp}</strong><br>
<span style="color:#284332;">
Un R² de <strong>{r2:.4f}</strong> indica que el <strong>{r2*100:.1f}%</strong> de la variacion del sector
<strong>{selected_column.replace('_', ' ')}</strong> se explica por su tendencia temporal.
{"Esto significa que el sector tiene un comportamiento altamente predecible y estable." if r2 >= 0.9 else ""}
{"El sector muestra una tendencia moderada, pero con influencia de factores externos." if 0.5 <= r2 < 0.9 else ""}
{"El sector no sigue una tendencia lineal clara y requiere modelos complementarios para su analisis." if r2 < 0.5 else ""}
</span>
</div>\
""", unsafe_allow_html=True)

    st.markdown(f"""\
<div style="background:#f2fbf4; border-radius:10px; padding:0.8rem 1.2rem; margin:0.5rem 0;">
<strong style="color:#284332;">Analisis de los modelos</strong><br>
<span style="color:#284332;">
<span style="color:#e67e22;"><strong>Promedio Movil</strong></span> (ventana {window}): suaviza las fluctuaciones de corto plazo para revelar la tendencia subyacente.<br>
<span style="color:#2980b9;"><strong>Suav. Exponencial</strong></span> (alpha={alpha:.2f}): da mayor peso a los datos recientes, reflejando cambios actuales.<br>
<span style="color:#c0392b;"><strong>Regresion Lineal</strong></span> (y = {slope:.4f}x + {intercept:.4f}): proyecta la tendencia lineal historica.
</span>
</div>\
""", unsafe_allow_html=True)

    st.markdown("#### Tabla de datos")
    display = chart.copy()
    display["Fecha"] = display["Fecha"].dt.strftime("%Y-%m-%d")
    st.dataframe(display, use_container_width=True, height=450)
