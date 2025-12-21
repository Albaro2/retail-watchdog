import sys
import os
# Añadir raíz al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.inventory import check_order_status
from src.tools.policy import consult_policy

print("🧪 INICIANDO TEST DE HERRAMIENTAS (TOOLS)...")
print("-" * 50)

# 1. Prueba SQL
print("1️⃣ Probando Herramienta de Inventario...")
resultado_sql = check_order_status.invoke("ORD-9902")
print(resultado_sql)
print("-" * 20)

# 2. Prueba RAG
print("2️⃣ Probando Herramienta de Políticas...")
resultado_rag = consult_policy.invoke("retraso envio 48 horas")
print(resultado_rag)

print("-" * 50)
print("✅ SI VES DATOS ARRIBA, LAS TOOLS FUNCIONAN.")