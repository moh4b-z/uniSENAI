import streamlit as st
import pymysql
import pandas as pd
import time

st.set_page_config(page_title="GRANT / REVOKE", layout="centered")
st.title("GRANT / REVOKE - Banco de Dados")

# Função de conexão
def conectar(usuario, senha):
    try:
        conn = pymysql.connect(
            host="localhost",
            user=usuario,
            password=senha,
            database="sistema_empresa"  # ajuste conforme seu banco
        )
        return conn
    except pymysql.MySQLError as err:
        st.error(f"Erro de conexão: {err}")
        return None

# Estado da sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "conn" not in st.session_state:
    st.session_state.conn = None
if "user" not in st.session_state:
    st.session_state.user = None

# Interface de Login
if not st.session_state.logged_in:
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        conn = conectar(user, password)
        if conn:
            st.session_state.logged_in = True
            st.session_state.conn = conn
            st.session_state.user = user
            st.success(f"Usuário {user} conectado com sucesso!")
            time.sleep(1.5)
            st.rerun() 

# Interface principal
else:
    st.write(f"Usuário conectado: **{st.session_state.user}**")

    query = st.text_area("Digite um comando SQL:")

    if st.button("Executar Query"):
        try:
            cursor = st.session_state.conn.cursor()
            cursor.execute(query)

            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(rows, columns=cols)
                st.dataframe(df)
            else:
                st.session_state.conn.commit()
                st.success("Operação realizada com sucesso!")
            cursor.close()
        except pymysql.MySQLError as err:
            st.error(f"Erro SQL: {err}")

    if st.button("Sair"):
        if st.session_state.conn:
            st.session_state.conn.close()
        st.session_state.logged_in = False
        st.session_state.conn = None
        st.success("Logout realizado com sucesso.")