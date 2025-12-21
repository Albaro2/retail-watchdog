import sqlite3
import os
from langchain_core.tools import tool

# Definimos la ruta a la DB de forma robusta
DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/inventory.db")

@tool
def check_order_status(order_id: str) -> str:
    """
    Consulta el estado de un pedido y detalles del producto dado un Order ID (ej: ORD-9902).
    Devuelve un string con la información encontrada o un error si no existe.
    """
    print(f"🔍 TOOL CALL: Consultando DB para pedido {order_id}...")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        query = """
        SELECT o.order_id, o.status, o.order_date, p.name, p.stock, p.price 
        FROM orders o
        JOIN products p ON o.sku = p.sku
        WHERE o.order_id = ?
        """
        
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return (f"PEDIDO ENCONTRADO:\n"
                    f"- ID: {result[0]}\n"
                    f"- Estado: {result[1]}\n"
                    f"- Fecha: {result[2]}\n"
                    f"- Producto: {result[3]}\n"
                    f"- Stock Actual: {result[4]}\n"
                    f"- Precio: ${result[5]}")
        else:
            return f"❌ Error: El pedido {order_id} no existe en la base de datos."
            
    except Exception as e:
        return f"Error de sistema consultando SQL: {str(e)}"