from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from src.agent.prompts import SYSTEM_PROMPT, HUMAN_PROMPT
from src.agent.state import AgentState
from src.ingestion.embedder import cargar_vectorstore
from src.utils.config import OPENAI_API_KEY, LLM_MODEL, TOP_K_RESULTS, PAGE_OFFSET

vectorstore = cargar_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K_RESULTS})

llm = ChatOpenAI(
    model=LLM_MODEL,
    openai_api_key=OPENAI_API_KEY,
    temperature=0
)

def nodo_retrieve(state: AgentState) -> AgentState:
    """Busca en ChromaDB los chunks más relevantes para la pregunta."""
    print("🔍 Buscando en ChromaDB...")

    question = state["question"]
    docs = retriever.invoke(question)

    context = ""
    sources = []

    for doc in docs:
        pagina_raw = doc.metadata.get("page", 0)
        pagina = pagina_raw + PAGE_OFFSET if isinstance(pagina_raw, int) else pagina_raw
        archivo = doc.metadata.get("archivo", "CTE")
        context += f"[Página {pagina}]\n{doc.page_content}\n\n"
        sources.append({
            "pagina": pagina,
            "archivo": archivo,
            "fragmento": doc.page_content[:200]
        })

    print(f"   ✅ {len(docs)} fragmentos encontrados")

    return {**state, "context": context, "sources": sources}


def nodo_generate(state: AgentState) -> AgentState:
    """Genera la respuesta usando el LLM con el contexto recuperado."""
    print("🧠 Generando respuesta...")

    chat_history = ""
    for msg in state["messages"]:
        if isinstance(msg, HumanMessage):
            chat_history += f"Usuario: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            chat_history += f"Agente: {msg.content}\n"

    prompt = HUMAN_PROMPT.format(
        context=state["context"],
        question=state["question"],
        chat_history=chat_history
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    response = llm.invoke(messages)
    answer = response.content

    new_messages = state["messages"] + [
        HumanMessage(content=state["question"]),
        AIMessage(content=answer)
    ]

    print("   ✅ Respuesta generada")

    return {**state, "answer": answer, "messages": new_messages}