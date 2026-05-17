# 🏗️ Agente RAG para el Código Técnico de la Edificación (CTE)

Agente conversacional con IA que responde preguntas técnicas sobre el CTE español, citando siempre la página de origen del documento.

## 🧠 Arquitectura

```
PDF del CTE → Chunks → Embeddings → ChromaDB
                                        ↓
         Pregunta → Retriever → LLM (GPT-4o mini) → Respuesta con fuentes
```

## 🛠️ Stack tecnológico

- **LangChain** — pipeline de IA
- **LangGraph** — lógica del agente
- **ChromaDB** — base de datos vectorial persistente
- **OpenAI** — embeddings y modelo GPT-4o mini
- **Streamlit** — interfaz de chat
- **PyPDF** — extracción de texto de PDFs

## 📋 Requisitos previos

- Python 3.11
- Cuenta en [OpenAI](https://platform.openai.com) con crédito (mínimo 5€)
- PDF del CTE descargable

## 🚀 Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/josemrz1987/cte-rag-agent.git
cd cte-rag-agent
```

### 2. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 3. Configura las variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```
OPENAI_API_KEY=sk-tu-clave-aqui
```

### 4. Añade el PDF del CTE

Descarga el PDF del CTE y colócalo en:

```
data/raw/CTE_2026.pdf
```

### 5. Indexa el documento

```bash
python scripts/ingest.py
```

### 6. Lanza la aplicación

```bash
streamlit run app/streamlit_app.py
```

## 📁 Estructura del proyecto

    cte-rag-agent/
    ├── data/
    │   ├── raw/                    # PDF del CTE (no incluido)
    │   └── chroma_db/              # Vector store (generado automáticamente)
    ├── src/
    │   ├── ingestion/              # Carga, chunking y embeddings
    │   ├── retrieval/              # Búsqueda en ChromaDB
    │   ├── agent/                  # Grafo LangGraph, nodos y prompts
    │   └── utils/                  # Configuración
    ├── app/
    │   └── streamlit_app.py        # Interfaz de chat
    ├── scripts/
    │   └── ingest.py               # Script de ingestión
    ├── notebooks/
    │   └── evaluacion_rag.ipynb    # Evaluación del agente
    ├── .env                        # API keys (no incluido)
    └── requirements.txt

## ⚙️ Funcionamiento

1. El PDF del CTE se divide en fragmentos de 1000 caracteres con solapamiento de 200
2. Cada fragmento se convierte en un vector numérico con OpenAI Embeddings
3. Los vectores se guardan en ChromaDB de forma persistente
4. Cuando el usuario hace una pregunta, el agente busca los 5 fragmentos más relevantes
5. GPT-4o mini genera una respuesta citando siempre la página de origen

## 📊 Evaluación

El notebook `notebooks/evaluacion_rag.ipynb` incluye un conjunto de preguntas de evaluación para verificar que el agente recupera contexto real y no alucina.
