import os
from langchain_core.tools import tool
from langchain_openai import AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

# Cargar entorno para asegurar que tenemos las API Keys
load_dotenv()

# Rutas
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../../data/chroma_db")

@tool
def consult_policy(query: str) -> str:
    """
    Busca en las políticas corporativas (RAG) para responder dudas sobre devoluciones,
    reembolsos o compensaciones. Úsala cuando necesites saber qué regla aplicar.
    Input: Una pregunta natural (ej: '¿Cuándo corresponde reembolso?').
    """
    print(f"🔍 TOOL CALL: Buscando en Políticas: '{query}'...")
    
    try:
        # 1. Conectar al modelo de Embeddings (El mismo que usaste para ingesta)
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
            openai_api_version="2023-05-15",
        )
        
        # 2. Conectar a la DB Vectorial existente
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
        
        # 3. Buscar los 2 fragmentos más relevantes
        results = vectorstore.similarity_search(query, k=2)
        
        # 4. Formatear respuesta
        context = "\n\n".join([doc.page_content for doc in results])
        return f"INFORMACIÓN RELEVANTE ENCONTRADA EN POLÍTICAS:\n{context}"
        
    except Exception as e:
        return f"Error consultando el sistema RAG: {str(e)}"