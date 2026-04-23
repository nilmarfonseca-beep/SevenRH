import streamlit as st

def proteger_rota():
    if "usuario_logado" not in st.session_state:
        st.session_state["usuario_logado"] = False

    if not st.session_state.get("usuario_logado"):
        st.title("⚠️ Precisa estar logado!")
        st.stop()