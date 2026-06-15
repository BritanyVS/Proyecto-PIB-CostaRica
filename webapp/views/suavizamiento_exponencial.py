from __future__ import annotations

import pandas as pd
import streamlit as st

from ..methods.suavizamiento_exponencial import SuavizamientoExponencial


def render_suavizamiento_exponencial_view(data: pd.DataFrame) -> None:
    st.markdown("### Suavizamiento exponencial")
    st.caption("Suaviza la serie dando mas peso a los datos recientes mediante un factor alpha.")

    numeric_columns = [column for column in data.columns if column != "Fecha"]
    default_column = "PIB_Precios_Mercado" if "PIB_Precios_Mercado" in numeric_columns else numeric_columns[0]

    control_cols = st.columns([2, 1])
    with control_cols[0]:
        selected_column = st.selectbox("Variable", numeric_columns, index=numeric_columns.index(default_column))
    with control_cols[1]:
        alpha = st.slider("Alpha", min_value=0.1, max_value=1.0, value=0.3, step=0.05)

    calculator = SuavizamientoExponencial(data=data, column=selected_column, alpha=alpha)
    result = calculator.calculate()

    latest_original = result[selected_column].iloc[-1]
    latest_smoothed = result["Suavizamiento_Exponencial"].iloc[-1]
    first_available = result["Fecha"].iloc[0]
    last_available = result["Fecha"].iloc[-1]

    metrics = st.columns(3)
    metrics[0].metric("Variable", selected_column)
    metrics[1].metric("Ultimo suavizado", f"{latest_smoothed:,.2f}")
    metrics[2].metric("Ultimo valor", f"{latest_original:,.2f}")

    st.line_chart(
        result.set_index("Fecha")[[selected_column, "Suavizamiento_Exponencial"]],
        use_container_width=True,
        height=420,
    )

    st.markdown(
        f"""
        <div class="card">
            <strong>Rango analizado:</strong> {first_available:%Y-%m-%d} a {last_available:%Y-%m-%d}<br>
            <strong>Alpha aplicado:</strong> {alpha:.2f}
        </div>
        """,
        unsafe_allow_html=True,
    )

    table_data = result.copy()
    table_data["Fecha"] = table_data["Fecha"].dt.strftime("%Y-%m-%d")
    st.dataframe(table_data, use_container_width=True, height=520)