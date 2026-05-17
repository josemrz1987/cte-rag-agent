from langchain_community.document_loaders import PyPDFLoader
import os

def cargar_pdfs(carpeta="data/raw"):
    """Carga todos los PDFs de la carpeta y les añade metadata."""
    documentos = []

    archivos = [f for f in os.listdir(carpeta) if f.endswith(".pdf")]

    if not archivos:
        print("⚠️  No se encontraron PDFs en la carpeta data/raw")
        return []

    for archivo in archivos:
        ruta = os.path.join(carpeta, archivo)
        print(f"📄 Cargando {archivo}...")

        loader = PyPDFLoader(ruta)
        paginas = loader.load()

        for pagina in paginas:
            pagina.metadata["documento"] = "CTE"
            pagina.metadata["descripcion"] = "Código Técnico de la Edificación"
            pagina.metadata["archivo"] = archivo

        documentos.extend(paginas)
        print(f"   ✅ {len(paginas)} páginas cargadas")

    print(f"\n📚 Total: {len(documentos)} páginas cargadas")
    return documentos