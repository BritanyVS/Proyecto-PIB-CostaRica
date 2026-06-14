import streamlit as st

from ..config import APP_TITLE, PALETA


def render_header() -> None:
    st.markdown(
        f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between; gap:1rem; align-items:flex-start; flex-wrap:wrap;">
                <div>
                    <div style="font-size:0.82rem; letter-spacing:0.12em; text-transform:uppercase; color:{PALETA['texto_suave']}; font-weight:700;">Base de datos</div>
                    <h1 style="margin:0.18rem 0 0.32rem 0; font-size:2rem; font-weight:800;">{APP_TITLE}</h1>
                </div>
                <div style="background:{PALETA['panel_fuerte']}; color:{PALETA['texto']}; border-radius:999px; padding:0.5rem 0.85rem; font-weight:700; border:1px solid {PALETA['linea']};">Vista Base de datos</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )