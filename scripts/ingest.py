import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion.pdf_loader import cargar_pdfs
from src.ingestion.chunker import dividir_documentos
from src.ingestion.embedder import crear_vectorstore

def main():
    print("=" * 50)
    print("🚀 INGESTIÓN DEL CTE")
    print("=" * 50)

    print("\n📂 PASO 1: Cargando PDFs...")
    documentos = cargar_pdfs()

    if not documentos:
        print("❌ No se encontraron documentos. Revisa la carpeta data/raw")
        return

    print("\n✂️  PASO 2: Dividiendo en chunks...")
    chunks = dividir_documentos(documentos)

    print("\n🧠 PASO 3: Generando embeddings y guardando en ChromaDB...")
    vectorstore = crear_vectorstore(chunks)

    print("\n" + "=" * 50)
    print("✅ INGESTIÓN COMPLETADA")
    print(f"   Chunks indexados: {len(chunks)}")
    print("   Ya puedes usar el agente")
    print("=" * 50)

if __name__ == "__main__":
    main()