from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Estado compartido entre todos los nodos del agente."""
    messages: List[BaseMessage]  # Historial de conversación
    question: str                # Pregunta actual del usuario
    context: str                 # Chunks recuperados de ChromaDB
    answer: str                  # Respuesta generada por el LLM
    sources: List[dict]          # Fuentes citadas en la respuesta