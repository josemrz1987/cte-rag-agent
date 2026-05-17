from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.utils.config import OPENAI_API_KEY, CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL

def crear_vectorstore(chunks):
    """Convierte los chunks en embeddings y los guarda en ChromaDB."""

    print("🔄 Generando embeddings y guardando en ChromaDB...")
    print("   (Esto puede tardar unos minutos según el tamaño del PDF)")

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DB_PATH
    )

    print(f"✅ {len(chunks)} chunks guardados en ChromaDB")
    print(f"   Ubicación: {CHROMA_DB_PATH}")

    return vectorstore


def cargar_vectorstore():
    """Carga un ChromaDB ya existente desde disco."""

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_PATH
    )

    print("✅ ChromaDB cargado desde disco")
    return vectorstore