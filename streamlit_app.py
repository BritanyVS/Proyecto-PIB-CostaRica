import streamlit as st

from webapp.components.header import render_header
from webapp.components.table import render_date_filter, render_table
from webapp.config import APP_TITLE, PALETA
from webapp.data import load_data_from_excel, load_default_data
from webapp.views.regresion_lineal import render_regresion_lineal_view
from webapp.views.promedio_movil import render_promedio_movil_view
from webapp.views.suavizamiento_exponencial import render_suavizamiento_exponencial_view
from webapp.views.control_estadistico import render_control_estadistico_view
from webapp.views.cadena_markov import render_markov_view


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
            #MainMenu {{
                visibility: hidden;
            }}
            header {{
                visibility: hidden;
                height: 0;
            }}
            footer {{
                visibility: hidden;
                height: 0;
            }}
            [data-testid="stToolbar"] {{
                visibility: hidden;
                height: 0;
            }}
            .stApp {{
                background: linear-gradient(180deg, {PALETA['fondo']} 0%, #ffffff 100%);
                color: {PALETA['texto']};
            }}
            .block-container {{
                padding-top: 1.6rem;
                padding-bottom: 2rem;
                max-width: 100% !important;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.86);
                border: 1px solid {PALETA['linea']};
                border-radius: 18px;
                padding: 1rem 1.15rem;
                box-shadow: 0 8px 24px rgba(40, 67, 50, 0.05);
            }}
            h1, h2, h3, p, span, div, label {{
                color: {PALETA['texto']};
            }}
            [data-testid="stDataFrame"] {{
                border-radius: 16px;
                overflow: hidden;
                border: 1px solid {PALETA['linea']};
                box-shadow: 0 8px 22px rgba(40, 67, 50, 0.05);
            }}
            [data-testid="stDataFrame"] table {{
                background: #ffffff;
            }}
            .stButton > button {{
                background: {PALETA['panel_fuerte']};
                color: {PALETA['texto']};
                border: 0;
                border-radius: 12px;
                padding: 0.5rem 1rem;
                font-weight: 600;
            }}
            .stButton > button:hover {{
                background: {PALETA['acento']};
                color: {PALETA['texto']};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    inject_css()
    selected_view = render_header()

    default_data = load_default_data()

    if default_data is not None:
        st.success("Excel detectado correctamente")
    else:
        st.info("Carga el Excel manualmente.")

    with st.expander("Cargar Excel manualmente", expanded=False):
        uploaded_file = st.file_uploader(
            "Seleccionar archivo",
            type=["xlsx"],
        )

    if uploaded_file is not None:
        data = load_data_from_excel(uploaded_file)
    elif default_data is not None:
        data = default_data
    else:
        st.info("Carga el archivo para ver la tabla completa.")
        st.stop()

    if data.empty:
        st.warning("El archivo se cargó, pero no contiene filas válidas después del procesamiento.")
        st.stop()

    if selected_view == "Base de datos":
        filtered_data = render_date_filter(data)
        render_table(filtered_data)
    elif selected_view == "Promedio movil":
        render_promedio_movil_view(data)
    elif selected_view == "Suavizamiento exponencial":
        render_suavizamiento_exponencial_view(data)

    elif selected_view == "Control estadistico":
        render_control_estadistico_view(data)

    elif selected_view == "Cadena de Markov":
        render_markov_view(data)
    else:
        render_regresion_lineal_view(data)


if __name__ == "__main__":
    main()