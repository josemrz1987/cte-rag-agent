import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.agent.graph import crear_grafo
from langchain_core.messages import HumanMessage, AIMessage

# Configuración de la página
st.set_page_config(
    page_title="Agente CTE",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Agente CTE")
st.caption("Consulta el Código Técnico de la Edificación con IA")

# Inicializar el agente y el historial en la sesión
if "agente" not in st.session_state:
    with st.spinner("Cargando agente..."):
        st.session_state.agente = crear_grafo()
        st.session_state.messages = []
        st.session_state.historial = []

# Mostrar historial de conversación
for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("📚 Fuentes consultadas"):
                for source in msg["sources"]:
                    st.markdown(f"**Página {source['pagina']}** — {source['archivo']}")
                    st.caption(source["fragmento"] + "...")

# Input del usuario
if pregunta := st.chat_input("Escribe tu pregunta sobre el CTE..."):

    # Mostrar pregunta del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.historial.append({
        "role": "user",
        "content": pregunta
    })

    # Ejecutar el agente
    with st.chat_message("assistant"):
        with st.spinner("Buscando en el CTE..."):

            estado_inicial = {
                "question": pregunta,
                "messages": st.session_state.messages,
                "context": "",
                "answer": "",
                "sources": []
            }

            resultado = st.session_state.agente.invoke(estado_inicial)

            respuesta = resultado["answer"]
            sources = resultado["sources"]

            st.session_state.messages = resultado["messages"]

        st.markdown(respuesta)

        with st.expander("📚 Fuentes consultadas"):
            for source in sources:
                st.markdown(f"**Página {source['pagina']}** — {source['archivo']}")
                st.caption(source["fragmento"] + "...")

    st.session_state.historial.append({
        "role": "assistant",
        "content": respuesta,
        "sources": sources
    })