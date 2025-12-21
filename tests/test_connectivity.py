import os
import sys

# Añadimos la raíz al path para poder ejecutar esto como script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

# Colores para la consola (Efecto "Matrix" profesional)
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def run_quality_gate():
    print(f"\n🚀 {GREEN}INICIANDO QUALITY GATE 1: INFRA & CONECTIVIDAD{RESET}")
    print("-" * 50)

    # 1. Validación de Secretos
    load_dotenv()
    key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    if not key or not endpoint or "PEGAR_AQUI" in key:
        print(f"❌ {RED}FALLO: Variables de entorno (.env) no configuradas correctamente.{RESET}")
        return

    print(f"✅ Variables de entorno detectadas.")
    print(f"   Target: {endpoint}")
    print(f"   Deployment: {deployment}")

    # 2. Prueba de Conexión Real
    print("\n📡 Enviando 'Ping' a Azure OpenAI (East US 2)...")
    
    try:
        llm = AzureChatOpenAI(
            azure_deployment=deployment,
            api_version="2024-05-01-preview",
            temperature=0,
            max_retries=1
        )
        
        msg = HumanMessage(content="Responde solo con la palabra: 'CONECTADO'.")
        response = llm.invoke([msg])
        
        content = response.content.strip()
        
        if "CONECTADO" in content:
            print(f"✅ {GREEN}ÉXITO: Respuesta recibida del modelo.{RESET}")
            print(f"   Payload: {content}")
            print("-" * 50)
            print(f"🏆 {GREEN}QUALITY GATE 1 SUPERADO. LISTO PARA FASE DE DATOS.{RESET}\n")
        else:
            print(f"⚠️ {RED}ALERTA: Se conectó, pero la respuesta fue inesperada: {content}{RESET}")

    except Exception as e:
        print(f"\n❌ {RED}ERROR FATAL DE CONEXIÓN:{RESET}")
        print(e)
        print("\nPosibles causas:")
        print("1. El nombre del 'deployment' en Azure no coincide con 'gpt-4o'.")
        print("2. La API Key es incorrecta.")
        print("3. El recurso aún se está aprovisionando (espera 5 min).")

if __name__ == "__main__":
    run_quality_gate()