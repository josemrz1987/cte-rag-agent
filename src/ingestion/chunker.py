from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.config import CHUNK_SIZE, CHUNK_OVERLAP

def dividir_documentos(documentos):
    """Divide las páginas del PDF en chunks más pequeños."""
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "],
    )

    chunks = splitter.split_documents(documentos)

    print(f"✂️  Documento dividido en {len(chunks)} chunks")
    print(f"   Tamaño máximo por chunk: {CHUNK_SIZE} caracteres")
    print(f"   Solapamiento entre chunks: {CHUNK_OVERLAP} caracteres")

    return chunks