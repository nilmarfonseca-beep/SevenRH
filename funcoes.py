import sqlite3
import streamlit as st
import re
import sqlalchemy
import pandas as pd
from validate_docbr import CPF
from pathlib import Path
from io import BytesIO
from docxtpl import DocxTemplate
from io import BytesIO
from num2words import num2words
#import psycopg2
import  bcrypt
 

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

def deletaDados(id):
    conexao = conectaBD()
    cursor = conexao.cursor()

    # Query correta com placeholder
    cursor.execute("DELETE FROM Cliente WHERE id_cliente = ?", (id,))
    
    conexao.commit()
    linhas_afetadas = cursor.rowcount  # número de linhas deletadas
    st.write(linhas_afetadas)
    cursor.close()
    conexao.close()
    return linhas_afetadas



def apagaDados(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    id = id
    st.write(id)
    linhas_afetadas = cursor.execute(f"DELETE FROM Cliente WHERE id_cliente = ?", (id,))

    linhas_afetadas = cursor.rowcount
    if linhas_afetadas > 0:
         st.info(linhas_afetadas)
    else:
         st.info('nada apagado')
    conexao.commit()
    cursor.close()
    conexao.close()
    return linhas_afetadas


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

    arquivo = "clientes cadastrados.xlsx"
    caminho = Path.home() / "Downloads" / arquivo
    
    clientes_cadastrados = pd.DataFrame(clientes_cadastrados, columns=["id_cliente", "carimbo", "autorizo", "cpf", "nome", "cep",  "endereco", "complemento", "bairro", "cidade", "uf", "nascimento", "idade", "email", "telefone", "contato",  "pagamento", "origem"])
    
    clientes_cadastrados.to_excel(caminho)
    conexao.commit()
    cursor.close()
    conexao.close()

def Grar_Contrato():    
# Upload da planilha
    arquivo = st.file_uploader("Envie a planilha", type=["xlsx"])

    if arquivo is not None:
        # Ler a planilha
        if arquivo.name.endswith(".xlsx"):
            df = pd.read_excel(arquivo)
        else:
            df = pd.read_csv(arquivo)

        st.write("Selecione um registro da planilha:")
        indice = st.selectbox("Escolha o índice:", df.index)

    if st.button("Gerar DOCX"):
        row = df.loc[indice]

        # Carregar modelo
        doc = DocxTemplate("model_contrato-Promissoria.dotx")

        # Contexto para substituir os placeholders
        contexto = {
            "nome": row["Nome"],
            "codigo": row["Codigo"]
        }

        doc.render(contexto)

        # Salvar em memória
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="Baixar documento",
            data=buffer,
            file_name=f"Contrato_{row['Nome']}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


def valor_por_extenso(valor: float) -> str:
    reais = int(valor)
    centavos = round((valor - reais) * 100)

    # Singular/plural
    if reais == 1:
        extenso_reais = num2words(reais, lang='pt') + " real"
    else:
        extenso_reais = num2words(reais, lang='pt') + " reais"

    if centavos > 0:
        if centavos == 1:
            extenso_centavos = num2words(centavos, lang='pt') + " centavo"
        else:
            extenso_centavos = num2words(centavos, lang='pt') + " centavos"
        return f"{extenso_reais} e {extenso_centavos}"
    return extenso_reais

def percentual_por_extenso(valor: float) -> str:
    inteiro = int(valor)
    decimal = round((valor - inteiro) * 100)

    if decimal > 0:
        return f"{num2words(valor, lang='pt')} por cento"
    else:
        return f"{num2words(inteiro, lang='pt')} por cento"  
    

def login_usuario(username, password):
    conn = sqlite3.connect("Clientes.db")
    cur = conn.cursor()

    cur.execute("SELECT password_hash FROM usuarios WHERE username=?", (username,))
    result = cur.fetchone()

    cur.close()
    #conn.close()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        return True
        #st.success(f"Olá {username }, vc esta logado")
    else:
        return False    
