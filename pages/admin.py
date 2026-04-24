import pandas as pd
import streamlit as st
import sqlite3
from pathlib import Path
#from st_aggrid import AgGrid, GridOptionsBuilder
streamlit-aggrid==0.3.4
from io import BytesIO
from docxtpl import DocxTemplate
from io import BytesIO
from num2words import num2words
from datetime import datetime, date
from funcoes import psycopg2
from funcoes import login_usuario
from auth import proteger_rota


proteger_rota()

   # CSS para ajustar a largura da sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
    min-width: 200px;
    max-width: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.image(r"icons\logo_icon.png")

# layout em linha
col1, col2 = st.columns([10, 1])

with col2:
    if st.button("🏃Sair"):
        st.session_state["usuario_logado"] = False
        st.switch_page("autentica.py")  # redireciona para o arquivo principal
        st.rerun()

with col1:
     st.write(f"**Olá {st.session_state['usuario_logado']} seja bem vinda(o)**")   


st.set_page_config(page_title="Área adminstrativa SevenRH", layout="wide", page_icon=("img\logo_icon.png"))
 

st.title("📝 Área adminstrativa -​ Manutenção de Candidatos cadastrados")
#st.write("**Clique no botão abaixo de download para gerar e fazer o download da planilha**")



# Usando HTML para mudar a cor
st.markdown(
    "<span style='color:red'>Pressione F5 para atualizar os dados e a página</span>",
    unsafe_allow_html=True
)

if st.sidebar.button("🏃Logout"):
    st.session_state["usuario_logado"] = False
    st.warning("Você saiu da conta.")
    st.switch_page("autentica.py")
    st.rerun()
    st.switch_page("autentica.py")
    #st.stop()
    


st.write("**Ao selecionar um registro, será mostrado novas opções.**")

conexao = sqlite3.connect("Clientes.db")
cursor = conexao.cursor()
cursor.execute("SELECT * FROM Cliente")
clientes_cadastrados = cursor.fetchall()

# Inicialização
clientes_cadastrados = pd.DataFrame(clientes_cadastrados, columns=["id_cliente", "carimbo", "autorizo", "cpf", "nome", "cep",  "endereco", "complemento", "bairro", "cidade", "uf", "nascimento", "idade", "email", "telefone", "contato",  "pagamento", "origem"])

# Injetando CSS para mudar a cor do botão
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0704FA; /* verde */
        color: white;
        border-radius: 8px;
        height: 50px;
        width: 160px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #65A2FA; /* verde mais escuro no hover */
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# CSS para estilizar o download_button
st.markdown("""
    <style>
    div[data-testid="stDownloadButton"] > button {
        background-color: #0704FA; /* azul */
        color: white;
        border-radius: 8px;
        height: 50px;
        width: 220px;
        font-weight: bold;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #0704FA; /* azul mais escuro no hover */
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Criando um buffer para armazenar o Excel
output = BytesIO()

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(clientes_cadastrados)
df = pd.DataFrame(clientes_cadastrados)

# Definindo o nome da aba (sheet_name)
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Respostas ao formulário 2", index=False)

output.seek(0)


gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection("single", use_checkbox=True, rowMultiSelectWithClick=True)  # clique direto

gridOptions = gb.build()

grid = AgGrid(
    df,
    gridOptions=gridOptions,
    update_mode="SELECTION_CHANGED",
    height=200
)


selected = grid.get("selected_rows")
#Alimenta variaveis apos selecionar registro
if selected is not None and len(selected) > 0:
    linha = selected.iloc[0].to_dict()
    id = linha["id_cliente"]

    # Converte o carimbo e nascimento para formato brasileiro (dd/mm/aaaa)
    carimbo_formatado = datetime.strptime(linha["carimbo"], "%Y-%m-%d").strftime("%d/%m/%Y")
    nascimento_formatado = datetime.strptime(linha["nascimento"], "%Y-%m-%d").strftime("%d/%m/%Y")
    
    if st.button("Gerar Contrato e promissória"):
        # Carregar modelo
        doc = DocxTemplate("model_contrato-Promissoria.docx")

        #Cria dicionario com variaveis para troca dos placehorders no modelo
        contexto = {
            "id": linha["id_cliente"],
            "carimbo" : carimbo_formatado,
            "nome": linha["nome"],
            "cpf": linha["cpf"],
            "nascimento": nascimento_formatado,
            "endereco": linha["endereco"],
            "complemento": linha["complemento"],
            "bairro": linha["bairro"],
            "cidade": linha["cidade"],
            "uf": linha["uf"],
            "telefone": linha["telefone"],
            "contato": linha["contato"],
            "email": linha["email"],
            "valor_contrato": "70,00",
            "valorextenso": "Setenta Reais",
            "meses" : "6",
            "mesExtenso" : "Seis",
            "valor_percentual": 20,
            "percentualextenso": "Vinte por cento",
            "origem": linha["origem"]
        }

        doc.render(contexto)

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="⬇️ Baixar documento",
            data=buffer,
            file_name=f"Contrato_{linha['nome']}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key="btn2"
        )
     

    if st.button(" 🗑️ Apagar registro", disabled=True):
        st.write("Cuidado, se apagar, nao tem como recuperar o registro")
        conexao = funcoes.conectaBD()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Cliente WHERE id_cliente = ?", (id,))
        conexao.commit()
        st.success('Registro apagado!')
        cursor.close()
        conexao.close()

            
st.divider()


# Botão de download com nome do arquivo e aba personalizada
st.download_button(
    label="📥 Baixar planilha Excel",
    data=output,
    file_name="clientes cadastrados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

      
