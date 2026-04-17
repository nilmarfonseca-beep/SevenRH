import pandas as pd
import streamlit as st
import sqlite3
import funcoes
from pathlib import Path

st.set_page_config(page_title="Área adminstrativa SevenRH", layout="wide")

st.title("📝​ Planilha de Candidatos cadastrados")
st.write("**Clique no botão abaixo para fazer o download da planilha**")

st.write("")

df = pd.read_excel("clientes cadastrados.xlsx")
 
st.dataframe(df,hide_index=True, use_container_width=True)

st.write("")    




if st.button(" ✅ Baixar planilha"):
    funcoes.exportar_dados()
    arquivo = "clientes cadastrados.xlsx"
    caminho = Path.home() / "Downloads" / arquivo
    st.info(f"Planilha Criada no local : {caminho}")


