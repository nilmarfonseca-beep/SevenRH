import streamlit as st
#import psycopg2
#from funcoes import login_usuario
import funcoes

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
st.sidebar.image(r"img\logo_icon.png")

def main():
    
    st.set_page_config(page_title="Área de Login SevenRH", layout="centered", page_icon=("icons\logo_icon.png"))
    
    st.image(image= "icons\logo_icon.png",width=150)

    st.title("🔐 Faça login para acessar a área administrativa")



    with st.form("my_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Senha", type="password")

        submit = st.form_submit_button("Entrar")

        if submit:
            if login_usuario(username, password):
                st.session_state["logado"] = True
                st.session_state["usuario_logado"] = username
                st.success(f"Ola {username } vc esta logado")
                st.switch_page("pages/admin.py")  # redireciona para o arquivo principal
            else:
                st.session_state["logado"] = False
                st.error("Usuário ou senha inválidos")
    if st.button("Não sou cadastrado(a)"):
        st.write("Por favor contacte o administrador do sistema")



            


if __name__ == "__main__":

    main()
