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
        key="markov_sector",
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
        use_container_width=True,
    )

    prob_estabilidad = 0.0
    for estado in CadenaMarkov.ESTADOS:
        if estado in matriz.index and estado in matriz.columns:
            prob_estabilidad = matriz.loc[estado, estado]

    color_markov = "#1a7a3a" if prob_estabilidad >= 0.7 else "#cc8b00" if prob_estabilidad >= 0.4 else "#b33c1a"

    st.markdown(f"""\
<div style="background:{color_markov}10; border-left:5px solid {color_markov}; border-radius:10px; padding:0.8rem 1.2rem; margin:1rem 0;">
<strong style="color:{color_markov}; font-size:1.05rem;">Interpretacion de la matriz</strong><br>
<span style="color:#284332;">
La probabilidad de permanecer en el <strong>mismo estado</strong> para el sector
<strong>{selected_column.replace('_', ' ')}</strong> es del <strong>{prob_estabilidad*100:.1f}%</strong>.<br>
{"El sector muestra una alta inercia: una vez que entra en un estado, tiende a mantenerse." if prob_estabilidad >= 0.7 else ""}
{"El sector tiene una moderada tendencia a cambiar de estado economico." if 0.4 <= prob_estabilidad < 0.7 else ""}
{"El sector es muy volatil: baja probabilidad de permanecer en el mismo estado." if prob_estabilidad < 0.4 else ""}
</span>
</div>\
""", unsafe_allow_html=True)

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

    total_periodos = len(result)
    pct_crecimiento = (conteo.get("Crecimiento", 0) / total_periodos) * 100
    pct_estancamiento = (conteo.get("Estancamiento", 0) / total_periodos) * 100
    pct_recesion = (conteo.get("Recesion", 0) / total_periodos) * 100

    st.markdown(f"""\
<div style="display:flex; gap:1rem; flex-wrap:wrap; margin:0.5rem 0;">
<div style="flex:1; min-width:140px; background:#d5f5e3; border-radius:10px; padding:0.8rem; text-align:center;">
<div style="color:#1a7a3a; font-size:0.75rem; font-weight:600;">CRECIMIENTO</div>
<div style="color:#1a7a3a; font-size:1.3rem; font-weight:700;">{pct_crecimiento:.1f}%</div>
</div>
<div style="flex:1; min-width:140px; background:#fef9e7; border-radius:10px; padding:0.8rem; text-align:center;">
<div style="color:#b7950b; font-size:0.75rem; font-weight:600;">ESTANCAMIENTO</div>
<div style="color:#b7950b; font-size:1.3rem; font-weight:700;">{pct_estancamiento:.1f}%</div>
</div>
<div style="flex:1; min-width:140px; background:#fdedec; border-radius:10px; padding:0.8rem; text-align:center;">
<div style="color:#c0392b; font-size:0.75rem; font-weight:600;">RECESION</div>
<div style="color:#c0392b; font-size:1.3rem; font-weight:700;">{pct_recesion:.1f}%</div>
</div>
</div>\
""", unsafe_allow_html=True)
