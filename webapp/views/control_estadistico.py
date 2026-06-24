from __future__ import annotations

import pandas as pd
import streamlit as st

from ..methods.control_estadistico import ControlEstadistico


def render_control_estadistico_view(data: pd.DataFrame) -> None:
    st.markdown("### Control estadistico de calidad")
    st.caption(
        "Analiza la estabilidad del PIB utilizando limites de control estadistico."
    )

    numeric_columns = [column for column in data.columns if column != "Fecha"]

    default_column = (
        "PIB_Precios_Mercado"
        if "PIB_Precios_Mercado" in numeric_columns
        else numeric_columns[0]
    )

    selected_column = st.selectbox(
        "Variable",
        numeric_columns,
        index=numeric_columns.index(default_column),
        key="ctrl_est_var",
    )

    calculator = ControlEstadistico(
        data=data,
        column=selected_column,
    )

    result = calculator.calculate()

    media = result.attrs["media"]
    desviacion = result.attrs["desviacion"]
    ucl = result.attrs["ucl"]
    lcl = result.attrs["lcl"]
    fuera_control = result.attrs["fuera_control"]

    first_available = result["Fecha"].iloc[0]
    last_available = result["Fecha"].iloc[-1]

    metrics = st.columns(4)

    metrics[0].metric("Media", f"{media:,.2f}")
    metrics[1].metric("Desviacion", f"{desviacion:,.2f}")
    metrics[2].metric("UCL", f"{ucl:,.2f}")
    metrics[3].metric("Fuera de control", fuera_control)

    chart_data = result.set_index("Fecha")[
        [
            selected_column,
            "Media",
            "UCL",
            "LCL",
        ]
    ]

    st.line_chart(
        chart_data,
        use_container_width=True,
        height=420,
    )

    st.markdown(f"""\
<div class="card">
<strong>Rango analizado:</strong>
{first_available:%Y-%m-%d} a {last_available:%Y-%m-%d}<br>
<strong>Limite superior:</strong>
{ucl:,.2f}<br>
<strong>Limite inferior:</strong>
{lcl:,.2f}
</div>\
""", unsafe_allow_html=True)

    if fuera_control > 0:
        st.warning(
            f"Se detectaron {fuera_control} observaciones fuera de control."
        )
    else:
        st.success(
            "Todos los datos se encuentran dentro de los limites de control."
        )

    rango = ucl - lcl
    proporcion_dentro = (1 - fuera_control / len(result)) * 100
    cv = (desviacion / media) * 100 if media != 0 else 0

    estabilidad = "Alta" if fuera_control == 0 else "Moderada" if fuera_control <= 3 else "Baja"
    color_est = "#1a7a3a" if fuera_control == 0 else "#cc8b00" if fuera_control <= 3 else "#b33c1a"

    st.markdown(f"""\
<div style="background:{color_est}10; border-left:5px solid {color_est}; border-radius:10px; padding:0.8rem 1.2rem; margin:1rem 0;">
<strong style="color:{color_est}; font-size:1.05rem;">Interpretacion: Estabilidad {estabilidad}</strong><br>
<span style="color:#284332;">
El sector <strong>{selected_column.replace('_', ' ')}</strong> tiene una <strong>media de {media:,.2f}</strong>
con una desviacion estandar de <strong>{desviacion:,.2f}</strong> (CV = {cv:.1f}%).<br>
El rango de control (UCL - LCL) es de <strong>{rango:,.2f}</strong> unidades.<br>
El <strong>{proporcion_dentro:.1f}%</strong> de las observaciones se encuentran dentro de los limites de control.
{"Esto indica un comportamiento estable y predecible." if fuera_control == 0 else ""}
{"Existen algunos periodos atipicos que requieren atencion." if 0 < fuera_control <= 3 else ""}
{"El sector presenta una alta variabilidad con multiples eventos fuera de lo normal." if fuera_control > 3 else ""}
</span>
</div>\
""", unsafe_allow_html=True)

    st.markdown("#### Tabla de datos")
    table_data = result.copy()
    table_data["Fecha"] = table_data["Fecha"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        table_data,
        use_container_width=True,
        height=520,
    )
