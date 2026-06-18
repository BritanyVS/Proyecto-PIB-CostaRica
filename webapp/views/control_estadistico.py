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

    st.markdown(
        f"""
        <div class="card">
            <strong>Rango analizado:</strong>
            {first_available:%Y-%m-%d} a {last_available:%Y-%m-%d}<br>

            <strong>Limite superior:</strong>
            {ucl:,.2f}<br>

            <strong>Limite inferior:</strong>
            {lcl:,.2f}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if fuera_control > 0:
        st.warning(
            f"Se detectaron {fuera_control} observaciones fuera de control."
        )
    else:
        st.success(
            "Todos los datos se encuentran dentro de los limites de control."
        )

    table_data = result.copy()
    table_data["Fecha"] = table_data["Fecha"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        table_data,
        use_container_width=True,
        height=520,
    )