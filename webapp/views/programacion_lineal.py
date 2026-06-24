from __future__ import annotations

import pandas as pd
import streamlit as st

from ..methods.programacion_lineal import ProgramacionLineal


def render_programacion_lineal_view(
    data: pd.DataFrame
):

    st.markdown(
        "### Programación lineal"
    )

    st.caption(
        "Optimización de recursos entre sectores económicos."
    )

    numeric_columns = [
        column
        for column in data.columns
        if column != "Fecha"
    ]

    sectores = st.multiselect(
        "Sectores económicos",
        numeric_columns,
        default=numeric_columns[:5]
    )

    presupuesto = st.slider(
        "Presupuesto disponible",
        min_value=50,
        max_value=500,
        value=100,
        step=10
    )

    if len(sectores) < 2:
        st.warning(
            "Seleccione al menos dos sectores."
        )
        return

    modelo = ProgramacionLineal(
        data=data,
        sectores=sectores,
        presupuesto=presupuesto
    )

    resultado = modelo.calculate()

    valor_optimo = (
        resultado.attrs["valor_optimo"]
    )

    st.metric(
        "Valor económico máximo",
        f"{valor_optimo:,.2f}"
    )

    st.dataframe(
        resultado,
        use_container_width=True
    )

    st.bar_chart(
        resultado.set_index("Sector")
    )