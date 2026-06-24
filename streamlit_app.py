import streamlit as st

from webapp.components.header import render_header
from webapp.components.table import render_date_filter, render_table, render_pie_chart, render_info_database
from webapp.config import APP_TITLE, PALETA
from webapp.data import load_data_from_excel, load_default_data
from webapp.views.pronosticos_combinados import render_pronosticos_combinados_view
from webapp.views.control_estadistico import render_control_estadistico_view
from webapp.views.cadena_markov import render_markov_view
from webapp.views.programacion_lineal import render_programacion_lineal_view


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_css() -> None:
    st.markdown(f"""\
<style>
    #MainMenu, header, footer, [data-testid="stToolbar"] {{visibility: hidden; height: 0;}}
    .stApp {{background: linear-gradient(180deg, {PALETA['fondo']} 0%, #ffffff 100%); color: {PALETA['texto']};}}
    .block-container {{padding-top: 1.6rem; padding-bottom: 2rem; max-width: 100% !important;}}
    .card {{background: rgba(255, 255, 255, 0.86); border: 1px solid {PALETA['linea']}; border-radius: 18px; padding: 1rem 1.15rem; box-shadow: 0 8px 24px rgba(40, 67, 50, 0.05);}}
    h1, h2, h3, p, span, div, label {{color: {PALETA['texto']};}}
    [data-testid="stDataFrame"] {{border-radius: 16px; overflow: hidden; border: 1px solid {PALETA['linea']}; box-shadow: 0 8px 22px rgba(40, 67, 50, 0.05);}}
    [data-testid="stDataFrame"] table {{background: #ffffff;}}
    .stButton > button {{background: {PALETA['panel_fuerte']}; color: {PALETA['texto']}; border: 0; border-radius: 12px; padding: 0.5rem 1rem; font-weight: 600;}}
    .stButton > button:hover {{background: {PALETA['acento']}; color: {PALETA['texto']};}}
    div[data-testid="stRadio"] label {{font-size: 0.95rem; padding: 0.35rem 1.2rem; border-radius: 30px; background: {PALETA['panel_fuerte']}; transition: all 0.2s;}}
    div[data-testid="stRadio"] label:hover {{background: {PALETA['acento']};}}
    div[data-testid="stRadio"] label[data-selected="true"] {{background: {PALETA['texto']}; color: #ffffff !important;}}
    div[data-testid="stExpander"] {{border: 1px solid {PALETA['linea']}; border-radius: 12px; background: rgba(255,255,255,0.6);}}
    .stAlert {{border-radius: 12px; border: none;}}
    div[data-testid="stMetricValue"] {{font-size: 1.5rem; font-weight: 700;}}
</style>\
""", unsafe_allow_html=True)


def main() -> None:
    inject_css()
    selected_view = render_header()

    default_data = load_default_data()

    if default_data is not None:
        st.markdown(f"""\
<div style="background:#d5f5e3; border:1px solid #a3d9b1; border-radius:12px; padding:0.5rem 1rem; margin-bottom:0.5rem; color:#1a7a3a; font-size:0.9rem;">
Base de datos cargada automaticamente
</div>\
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""\
<div style="background:#fef9e7; border:1px solid #f0e5a0; border-radius:12px; padding:0.5rem 1rem; margin-bottom:0.5rem; color:#7d6608; font-size:0.9rem;">
No se encontro el archivo Excel por defecto. Cargalo manualmente.
</div>\
""", unsafe_allow_html=True)

    with st.expander("Cargar archivo Excel manualmente", expanded=False):
        uploaded_file = st.file_uploader(
            "Seleccionar archivo .xlsx",
            type=["xlsx"],
        )

    if uploaded_file is not None:
        data = load_data_from_excel(uploaded_file)
    elif default_data is not None:
        data = default_data
    else:
        st.info("Sube un archivo Excel para visualizar los datos.")
        st.stop()

    if data.empty:
        st.warning("El archivo se cargó, pero no contiene filas válidas.")
        st.stop()

    if selected_view == "Base de datos":
        render_info_database(data)
        filtered_data = render_date_filter(data)
        render_pie_chart(filtered_data)
        st.markdown("### Tabla completa de datos")
        render_table(data)
    elif selected_view == "Pronosticos":
        render_pronosticos_combinados_view(data)
    elif selected_view == "Control estadistico":
        render_control_estadistico_view(data)
    elif selected_view == "Cadena de Markov":
        render_markov_view(data)
    elif selected_view == "Programacion lineal":
        render_programacion_lineal_view(data)


if __name__ == "__main__":
    main()
