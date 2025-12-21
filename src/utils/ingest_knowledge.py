import os
import sys

# Hack para que encuentre los módulos si ejecutas desde la carpeta utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_chroma import Chroma

# Configuración
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
PDF_PATH = os.path.join(DATA_DIR, "policies.pdf")
CHROMA_PATH = os.path.join(DATA_DIR, "chroma_db")

def ingest_docs():
    print("📚 INICIANDO PROCESO DE INGESTA (RAG)...")
    load_dotenv()
    
    # 1. Cargar PDF
    if not os.path.exists(PDF_PATH):
        print(f"❌ Error: No encuentro el PDF en {PDF_PATH}")
        return

    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    print(f"   🔹 Documento cargado: {len(docs)} páginas.")

    # 2. Trocear (Chunking)
    # Estrategia: Chunks de 500 caracteres con solapamiento para no cortar frases a medias
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    splits = text_splitter.split_documents(docs)
    print(f"   🔹 Generados {len(splits)} fragmentos de información (chunks).")

    # 3. Inicializar Modelo de Embeddings (Azure)
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        openai_api_version="2023-05-15",
    )

    # 4. Crear/Actualizar Base de Datos Vectorial (Chroma)
    print("   🔹 Vectorizando y guardando en ChromaDB (Local)...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print(f"✅ INGESTA COMPLETADA. Base de conocimiento lista en: {CHROMA_PATH}")

if __name__ == "__main__":
    ingest_docs()