import os
from dotenv import load_dotenv

# Imports de LangGraph y LangChain
from langgraph.prebuilt import create_react_agent
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage

# Imports de nuestras herramientas
from src.tools.inventory import check_order_status
from src.tools.policy import consult_policy

# 1. Configuración Inicial
load_dotenv()

def get_agent_graph():
    """
    Factory function que construye y devuelve el Grafo ejecutable.
    """
    
    # A. Configurar el LLM (Tu cerebro GPT-4o)
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0, # Temperatura 0 para máxima precisión en datos
        streaming=True
    )

    # B. Definir las Herramientas (Tus manos)
    tools = [check_order_status, consult_policy]

    # C. Definir la Personalidad (System Prompt)
    # Esto es clave: Le decimos quién es y cómo debe comportarse.
    system_prompt = """
    Eres el 'Retail Watchdog', un Asistente Senior de Operaciones y Logística.
    Tu misión es resolver incidencias de pedidos de forma autónoma y eficiente.

    TIENES ACCESO A DOS HERRAMIENTAS:
    1. check_order_status: Úsala SIEMPRE primero para ver qué pasa con un pedido.
    2. consult_policy: Úsala para saber qué compensación corresponde según el problema encontrado.

    REGLAS DE ACTUACIÓN (ALGORITMO MENTAL):
    1. Si el usuario te da un ID de pedido, PRIMERO consulta su estado en la DB.
    2. Analiza los datos:
       - Si el stock es 0, es una 'Rotura de Stock'.
       - Si el estado es 'Processing' y la fecha es antigua, es un 'Retraso'.
    3. Consulta las Políticas para ver qué solución aplica al caso concreto.
    4. Responde al usuario con una solución completa: Explica el problema y ofrece la compensación exacta (dinero o cupón) dictada por la política.
    
    Sé profesional, conciso y orientado a la solución.
    """

    # D. Crear el Agente ReAct (Patrón Standard de LangGraph)
    # Este grafo ya tiene pre-configurado el bucle: Pensar -> Ejecutar Tool -> Volver a Pensar
    graph = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )

    return graph