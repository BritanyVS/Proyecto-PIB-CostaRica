from __future__ import annotations

import pandas as pd
import streamlit as st

from ..methods.regresion_lineal import RegresionLineal


def render_regresion_lineal_view(data: pd.DataFrame) -> None:
    st.markdown("### Regresion lineal")
    st.caption("Ajusta una linea de tendencia sobre una variable del PIB usando el orden temporal de la serie.")

    numeric_columns = [column for column in data.columns if column != "Fecha"]
    default_column = "PIB_Precios_Mercado" if "PIB_Precios_Mercado" in numeric_columns else numeric_columns[0]

    selected_column = st.selectbox(
        "Variable",
        numeric_columns,
        index=numeric_columns.index(default_column),
    )

    calculator = RegresionLineal(data=data, column=selected_column)
    result = calculator.calculate()

    slope = result.attrs.get("slope", 0.0)
    intercept = result.attrs.get("intercept", 0.0)
    r_squared = result.attrs.get("r_squared", 0.0)

    latest_original = result[selected_column].iloc[-1]
    latest_predicted = result["Valor_Predicho"].iloc[-1]
    first_available = result["Fecha"].iloc[0]
    last_available = result["Fecha"].iloc[-1]

    metrics = st.columns(4)
    metrics[0].metric("Variable", selected_column)
    metrics[1].metric("Pendiente", f"{slope:,.4f}")
    metrics[2].metric("R2", f"{r_squared:,.4f}")
    metrics[3].metric("Ultimo predicho", f"{latest_predicted:,.2f}")

    st.line_chart(
        result.set_index("Fecha")[[selected_column, "Valor_Predicho"]],
        use_container_width=True,
        height=420,
    )

    st.markdown(
        f"""
        <div class="card">
            <strong>Rango analizado:</strong> {first_available:%Y-%m-%d} a {last_available:%Y-%m-%d}<br>
            <strong>Modelo:</strong> y = {slope:.4f}x + {intercept:.4f}
        </div>
        """,
        unsafe_allow_html=True,
    )

    table_data = result.copy()
    table_data["Fecha"] = table_data["Fecha"].dt.strftime("%Y-%m-%d")
    st.dataframe(table_data, use_container_width=True, height=520)