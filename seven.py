import streamlit as st
import streamlit.components.v1 as components
import re
import requests
import pandas as pd
from datetime import datetime, date
import funcoes
import sqlalchemy
from sqlalchemy import exists
from validate_docbr import CPF



def main():


    st.set_page_config(page_title="Área de Cadastro de Candidato", layout="centered")

    st.title("📋 Cadastro do Candidato")
    st.write("**Todos os campos devem ser preenchidos**")

    # criar navegacao e jogar st.image para la
    #st.sidebar.image(r"icons\logo_icon.png")
    #st.sidebar.title("Temos inumeras vagas á sua espera")

    st.sidebar.divider()

    carimbo = st.date_input("Data de cadastro", value = pd.Timestamp.today().date(),disabled=True, format="DD/MM/YYYY")

    # Confirma autorizacao para uso dos dados
    
    st.write("")
    st.write("**Os dados estão sujeitos à proteção da LGPD e seu uso e tratamento pela SEVENRH**")
    st.write("**é EXCLUSIVO para cadastro no sistema de vagas da empresa**")
    st.write("")

    
    

    autorizo = st.radio("Autoriza o uso dos dados? ",("Autorizo", "Não autorizo"))
    if autorizo != "Autorizo":
         st.info(" 🛑 Vc não autorizou o uso, por favor altere ou feche o app")
         return
    
    cpf = CPF()
    cpf_input = st.text_input("Digite seu CPF*")
    numero = cpf_input
    if cpf.validate(numero):
         cpf = cpf_input
    else:
         st.info(" ⏳ CPF inválido, confira!")
         return
    
    # verificando se existe o cpf digitado
    
    conexao = funcoes.conectaBD()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM Cliente WHERE cpf = ?", (cpf,))
    existe = cursor.fetchone()

    if existe:
            st.warning("⚠️ Este CPF já está cadastrado, verifique!")
            return




    nome = st.text_input("Digite seu nome completo*")
    cep = st.text_input("Digite seu CEP, 8 digitos", max_chars=8)


    if st.button(" ✉️ Busca CEP", disabled=len(cep) != 8, ):
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        data = response.json()
        if "erro" not in data:
            st.session_state["logradouro"] = data.get("logradouro","")
            st.session_state["bairro"] = data.get("bairro","")
            st.session_state["cidade"]= data.get("localidade","")
            st.session_state["uf"] = data.get("uf","")       
        else:
            st.error("🚨 CEP não encontrado")
            return

    endereco = st.text_input("Digite ou confira seu endereço*", key = "logradouro") 
    complemento = st.text_input("Digite ou confira o complemento(quadra, lote, numero)*") 
    bairro = st.text_input("Digite ou confira seu bairro*", key = "bairro")
    cidade = st.text_input("Digite ou confira sua cidade*", key = "cidade" )
    uf = st.text_input("Digite ou confira seu estado*", key = "uf")


    nascimento = st.date_input("Digite a data de nascimento*",min_value=date(1950,1,1), max_value=date(2030,1,1), format="DD/MM/YYYY" )
    idade = st.number_input("Digite a sua idade",min_value=0, step=1, format="%d")
    email = st.text_input("Digite seu email*")
    telefone = st.text_input("Digite seu numero de telefone*")
    contato = st.text_input("Digite o numero para contato*")
    opcoes = ["Pagarei taxa de cadastro qdo estiver trabalhando", "Pagarei taxa de cadastro apos cadastro efetuado","Autorizo desconto no 1o pagamento"]
    pagamento = st.selectbox("Escolha a forma como vi pagar", opcoes, key="opcao")
    origem = st.text_input("Origem do cadastro", value="Formulario", disabled=True)
    botaodesbilitado = not (cpf and nome and cep)

    if st.button(" 💾 Adicionar dados e fecha app",disabled=botaodesbilitado):
        funcoes.inseredados(carimbo, autorizo, cpf, nome, cep, endereco, complemento, bairro, cidade,
                uf, nascimento, idade, email, telefone, contato, pagamento, origem)
        st.success(" 👍 Parabéns, dados inseridos com sucesso")
        st.balloons()
                carimbo = ""
        autorizo = ""
        cpf = "" 
        nome = "" 
        cep = "" 
        endereco = "" 
        complemento = "" 
        bairro = "" 
        cidade = "" 
        uf = ""
        nascimento = ""
        idade = ""
        email = ""
        telefone = ""
        contato = ""
        pagamento= ""
        origem  = ""
        
if __name__ == "__main__":

    main()






