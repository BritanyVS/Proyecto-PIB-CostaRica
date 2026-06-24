from __future__ import annotations

import pandas as pd
import streamlit as st

from ..methods.programacion_lineal import ProgramacionLineal


def render_programacion_lineal_view(
    data: pd.DataFrame
):

    st.markdown("### Programacion lineal")
    st.caption("Optimizacion de recursos entre sectores economicos.")

    numeric_columns = [
        c for c in data.columns
        if c != "Fecha" and not c.endswith("_Var")
    ]

    sectores = st.multiselect(
        "Sectores economicos",
        numeric_columns,
        default=numeric_columns[:5]
    )

    presupuesto = st.slider(
        "Presupuesto disponible",
        min_value=50, max_value=500, value=100, step=10
    )

    if len(sectores) < 2:
        st.warning("Seleccione al menos dos sectores.")
        return

    modelo = ProgramacionLineal(
        data=data, sectores=sectores, presupuesto=presupuesto
    )
    resultado = modelo.calculate()

    valor_optimo = resultado.attrs["valor_optimo"]
    coeficientes = resultado.attrs["coeficientes"]

    df = resultado.copy()
    df["Promedio_Historico"] = df["Sector"].map(coeficientes)
    df["Participacion"] = df["Asignacion"] / df["Asignacion"].sum() * 100

    max_row = df.loc[df["Asignacion"].idxmax()]
    min_row = df.loc[df["Asignacion"].idxmin()]

    st.metric("Valor economico maximo", f"{valor_optimo:,.2f}")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Presupuesto", f"{presupuesto:,.0f}")
    col_b.metric("Sectores", len(sectores))
    col_c.metric("Asignado", f"{df['Asignacion'].sum():,.2f}")

    st.markdown(f"""\
<div style="background:#f2fbf4; border-left:5px solid #284332; border-radius:10px; padding:0.8rem 1.2rem; margin:0.5rem 0;">
<strong style="color:#284332;">Por que se asignan asi los recursos</strong><br>
<span style="color:#284332;">
El modelo distribuye el presupuesto de <strong>{presupuesto:,.0f}</strong> entre los sectores para maximizar el retorno economico total.
Cada sector tiene un <strong>rendimiento promedio historico</strong> (su contribucion media al PIB). El optimizador asigna mas recursos
a los sectores con mayor rendimiento, respetando los limites minimo (5) y maximo (40) por sector.<br><br>
<strong style="color:#1a7a3a;">Mayor asignacion:</strong> {max_row['Sector'].replace('_', ' ')} con {max_row['Asignacion']:.2f} ({max_row['Participacion']:.1f}% del total)
— rendimiento promedio de {coeficientes[max_row['Sector']]:,.2f}.<br>
<strong style="color:#c0392b;">Menor asignacion:</strong> {min_row['Sector'].replace('_', ' ')} con {min_row['Asignacion']:.2f} ({min_row['Participacion']:.1f}% del total)
— rendimiento promedio de {coeficientes[min_row['Sector']]:,.2f}.
</span>
</div>\
""", unsafe_allow_html=True)

    st.markdown("#### Asignacion optima por sector")
    st.dataframe(
        df.style.format({
            "Asignacion": "{:,.2f}",
            "Promedio_Historico": "{:,.2f}",
            "Participacion": "{:.1f}%",
        }),
        use_container_width=True,
    )

    st.bar_chart(
        resultado.set_index("Sector"),
        use_container_width=True,
    )