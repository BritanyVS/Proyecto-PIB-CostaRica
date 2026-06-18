from __future__ import annotations

import pandas as pd
import streamlit as st

from ..methods.cadena_markov import CadenaMarkov


def render_markov_view(data: pd.DataFrame):

    st.markdown("### Cadenas de Markov")

    st.caption(
        "Analiza las probabilidades de transición entre estados económicos."
    )

    numeric_columns = [
        c
        for c in data.columns
        if c != "Fecha"
    ]

    selected_column = st.selectbox(
        "Sector económico",
        numeric_columns,
    )

    calculator = CadenaMarkov(
        data=data,
        column=selected_column,
    )

    result = calculator.calculate()

    matriz = result.attrs["matriz"]

    ultimo_estado = result["Estado"].iloc[-1]

    st.metric(
        "Estado actual",
        ultimo_estado
    )

    st.markdown("#### Matriz de transición")

    st.dataframe(
        matriz,
        use_container_width=True
    )

    st.markdown("#### Historial de estados")

    table = result[
        [
            "Fecha",
            "Variacion",
            "Estado"
        ]
    ].copy()

    table["Fecha"] = (
        table["Fecha"]
        .dt.strftime("%Y-%m-%d")
    )

    st.dataframe(
        table,
        use_container_width=True,
        height=500
    )

    st.markdown("#### Distribución de estados")

    conteo = (
        result["Estado"]
        .value_counts()
    )

    st.bar_chart(conteo)