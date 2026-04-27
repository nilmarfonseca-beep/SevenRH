import streamlit as st
import os
from auth import proteger_rota

proteger_rota()

ARQUIVO = "dados.txt"

#st.popover("Configura valores para cadastro")
with st.popover("Configura valores referente ao cadastro"):

    # Inicializa variáveis
    valor_default = ""
    percentual_default = ""

    # Se já existe arquivo, carrega valores
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = f.read().split(";")
            if len(dados) == 2:
                valor_default, percentual_default = dados

    # Inputs com valores carregados
    valor = st.text_input("Valor do cadastro (moeda):", value=valor_default)
    percentual = st.text_input("Percentual a cobrar (%):", value=percentual_default)

    # Botão para salvar
    if st.button("Salvar"):
        if valor and percentual:
            with open(ARQUIVO, "w", encoding="utf-8") as f:
                f.write(f"{valor};{percentual}")
            st.success("Dados gravados com sucesso!")
        else:
            st.warning("Preencha os dois campos antes de salvar.")

    # Botão para ler (recarrega os inputs)
    if st.button("Ler"):
        if os.path.exists(ARQUIVO):
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                dados = f.read().split(";")
                if len(dados) == 2:
                    st.rerun()  # força recarregar a página com os valores
        else:
            st.warning("Nenhum dado gravado ainda.")

with st.popover("Configura local de gravaçao dos contratos"):
    pasta_contrato = st.text_input("Digite cole o caminho da pasta para salvar o contrato:")
    if st.button("Salvar caminho contrato"):
        if pasta_contrato and os.path.isdir(pasta_contrato):
            with open("contrato_path.txt", "w", encoding="utf-8") as f:
                f.write(pasta_contrato)
            st.success(f"Caminho da pasta salvo: {pasta_contrato}")
        else:
            st.warning("Informe um caminho válido de pasta.")

with st.popover("Local de gravação - Planilha"):
    pasta_planilha = st.text_input("Digite ou cole o caminho da pasta para salvar a planilha:")
    if st.button("Salvar caminho planilha"):
        if pasta_planilha and os.path.isdir(pasta_planilha):
            with open("planilha_path.txt", "w", encoding="utf-8") as f:
                f.write(pasta_planilha)
            st.success(f"Caminho da pasta salvo: {pasta_planilha}")
        else:
            st.warning("Informe um caminho válido de pasta.")
