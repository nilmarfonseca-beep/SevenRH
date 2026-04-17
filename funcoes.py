import sqlite3
import streamlit as st
import re
import sqlalchemy
import pandas as pd
from validate_docbr import CPF
from pathlib import Path
 

def conectaBD():
    conexao = sqlite3.connect("Clientes.db")
    return conexao

def inseredados(
    Carimbo, 
    Autorizo,
    Cpf, 
    Nome, 
    Cep, 
    Endereco, 
    Complemento, 
    Bairro, 
    Cidade, 
    Uf,
    Nascimento ,
    Idade,
    Email,
    Telefone,
    Contato,
    Pagamento,
    Origem
    ):

    conexao = conectaBD()
    cursor = conexao.cursor()

    # Criando a query

    Query = """
        INSERT INTO Cliente(
            Carimbo, Autorizo, Cpf, Nome, Cep, Endereco, Complemento,
            Bairro, Cidade, Uf, Nascimento, Idade, Email,
            Telefone, Contato, Pagamento, Origem
        )
        VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? , ?, ?)
    """

    #cursor.execute(Query)

    cursor.execute(Query,(Carimbo, Autorizo, Cpf, Nome, Cep, Endereco, Complemento,
        Bairro, Cidade, Uf, Nascimento, Idade, Email,
        Telefone, Contato, Pagamento, Origem))

    conexao.commit()
    conexao.close()


def listadados():
    conexao=conectaBD()
    cursor = conexao.cursor()
    cursor.execute("select * FROM Cliente")
    dados = cursor.fetchall()
    cursor.close()
    return dados
    

def verifica_cpf(cpf):
    # verifica se CPF já existe

        conexao = conectaBD()
        cursor = conexao.cursor()
    
        cursor.execute("SELECT 1 FROM Cliente WHERE cpf = ?", (cpf,))
        existe = cursor.fetchone()

        if existe:
            st.warning("⚠️ Este CPF já está cadastrado.")
        
        conexao.close()
        cursor.close()
            

def exportar_dados():
    conexao = sqlite3.connect("Clientes.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM Cliente")
    clientes_cadastrados = cursor.fetchall()
    print(clientes_cadastrados)

    arquivo = "clientes cadastrados.xlsx"
    caminho = Path.home() / "Downloads" / arquivo
    
    clientes_cadastrados = pd.DataFrame(clientes_cadastrados, columns=["id_cliente", "carimbo", "autorizo", "cpf", "nome", "cep",  "endereco", "complemento", "bairro", "cidade", "uf", "nascimento", "idade", "email", "telefone", "contato",  "pagamento", "origem"])
    
    clientes_cadastrados.to_excel(caminho)
    conexao.commit()
    cursor.close()
    conexao.close()

