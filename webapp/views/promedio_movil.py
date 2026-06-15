from __future__ import annotations

import pandas as pd
import streamlit as st

from ..methods.promedio_movil import PromedioMovil


def render_promedio_movil_view(data: pd.DataFrame) -> None:
    st.markdown("### Promedio movil")
    st.caption("Calcula una tendencia suavizada sobre una variable del PIB usando una ventana deslizante.")

    numeric_columns = [column for column in data.columns if column != "Fecha"]
    default_column = "PIB_Precios_Mercado" if "PIB_Precios_Mercado" in numeric_columns else numeric_columns[0]
    max_window = max(2, min(12, len(data)))

    control_cols = st.columns([2, 1])
    with control_cols[0]:
        selected_column = st.selectbox("Variable", numeric_columns, index=numeric_columns.index(default_column))
    with control_cols[1]:
        window = st.slider("Ventana", min_value=2, max_value=max_window, value=min(4, max_window), step=1)

    calculator = PromedioMovil(data=data, column=selected_column, window=window)
    result = calculator.calculate()

    if result.empty:
        st.warning("No hay suficientes datos para calcular el promedio movil con esa ventana.")
        return

    latest_original = result[selected_column].iloc[-1]
    latest_average = result["Promedio_Movil"].iloc[-1]
    first_available = result["Fecha"].iloc[0]
    last_available = result["Fecha"].iloc[-1]

    metrics = st.columns(3)
    metrics[0].metric("Variable", selected_column)
    metrics[1].metric("Ultimo promedio", f"{latest_average:,.2f}")
    metrics[2].metric("Ultimo valor", f"{latest_original:,.2f}")

    st.line_chart(
        result.set_index("Fecha")[[selected_column, "Promedio_Movil"]],
        use_container_width=True,
        height=420,
    )

    st.markdown(
        f"""
        <div class="card">
            <strong>Rango analizado:</strong> {first_available:%Y-%m-%d} a {last_available:%Y-%m-%d}<br>
            <strong>Ventana aplicada:</strong> {window} periodos
        </div>
        """,
        unsafe_allow_html=True,
    )

    table_data = result.copy()
    table_data["Fecha"] = table_data["Fecha"].dt.strftime("%Y-%m-%d")
    st.dataframe(table_data, use_container_width=True, height=520)