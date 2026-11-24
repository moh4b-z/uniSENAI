import pandas as pd
import streamlit as st
from pymongo import MongoClient

st.set_page_config(page_title="Secretaria online")

@st.cache_resource
def conectar():
    client = MongoClient(st.secrets["MONGO_URI"])
    return client["escola"]["alunos"]

alunos = conectar()
st.title("Secretaria online")

# 1. Cadastro
with st.form("cadastro", clear_on_submit=True):
    st.subheader("Cadastrar aluno")
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=14, max_value=99, value=20, step=1)
    curso = st.text_input("Curso")
    if st.form_submit_button("Salvar"):
        if nome and curso:
            alunos.insert_one({"nome": nome, "idade": int(idade), "curso": curso})
            st.success(f"{nome} cadastrado(a)!")
        else:
            st.error("Preencha nome e curso.")

# 2. Filtro
cursos = ["Todos"] + sorted(alunos.distinct("curso"))
escolha = st.selectbox("Filtrar por curso", cursos)
filtro = {} if escolha == "Todos" else {"curso": escolha}
dados = list(alunos.find(filtro, {"_id": 0, "nome": 1, "idade": 1, "curso": 1}).sort("nome", 1))

# 3. Indicadores e tabela
col1, col2 = st.columns(2)
col1.metric("Alunos", len(dados))
media = sum(d["idade"] for d in dados) / len(dados) if dados else 0
col2.metric("Idade média", f"{media:.1f}")

st.dataframe(pd.DataFrame(dados), hide_index=True)
