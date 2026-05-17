from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes import nodo_retrieve, nodo_generate

def crear_grafo():
    """Crea y compila el grafo del agente."""

    grafo = StateGraph(AgentState)

    # Añadir nodos
    grafo.add_node("retrieve", nodo_retrieve)
    grafo.add_node("generate", nodo_generate)

    # Definir el flujo
    grafo.set_entry_point("retrieve")
    grafo.add_edge("retrieve", "generate")
    grafo.add_edge("generate", END)

    # Compilar
    agente = grafo.compile()

    print("✅ Agente creado")
    return agente