import sys
import os

# --- FIX DEL PATH (CRÍTICO) ---
# Añadimos el directorio raíz del proyecto al sys.path para que Python encuentre 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ------------------------------

import chainlit as cl
from src.agents.graph import get_agent_graph
from langchain_core.messages import HumanMessage

# Instanciamos el grafo al arrancar la app
graph = get_agent_graph()

@cl.on_chat_start
async def start():
    """Mensaje de bienvenida al cargar la página"""
    await cl.Message(
        content="👋 **Hola, soy el Retail Watchdog.**\n\nDame un ID de pedido (ej: `ORD-9902`) y gestionaré la incidencia automáticamente consultando inventario y políticas."
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """
    Este es el bucle principal: Recibe mensaje del usuario -> Ejecuta Agente -> Responde
    """
    
    # 1. Preparamos el input para LangGraph
    initial_state = {"messages": [HumanMessage(content=message.content)]}
    
    # 2. Ejecutamos el grafo en modo "stream" para ver los pasos intermedios
    final_answer = cl.Message(content="")
    
    # Stream de eventos (Pensamiento del robot)
    async for event in graph.astream_events(initial_state, version="v1"):
        kind = event["event"]
        
        # A. Detectar cuando empieza a usar una herramienta (Feedback visual)
        if kind == "on_tool_start":
            tool_name = event['name']
            if tool_name not in ["__start__", "_Exception"]: # Filtramos ruido
                await cl.Message(
                    content=f"🛠️ *Consultando herramienta: {tool_name}...*", 
                    parent_id=message.id 
                ).send()
                
        # B. Detectar cuando el LLM genera la respuesta final (Token a token)
        elif kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                await final_answer.stream_token(content)

    # 3. Enviar respuesta final cerrada
    await final_answer.send()