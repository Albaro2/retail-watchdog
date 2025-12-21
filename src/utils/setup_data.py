import os
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "inventory.db")
PDF_PATH = os.path.join(DATA_DIR, "policies.pdf")

def create_database():
    print(f"🛠️  Creando Base de Datos SQL en: {DB_PATH}")
    
    # Asegurar que directorio existe
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Conectar (crea el archivo si no existe)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabla de PRODUCTOS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        sku TEXT PRIMARY KEY,
        name TEXT,
        stock INTEGER,
        price REAL
    )
    ''')
    
    # 2. Tabla de PEDIDOS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        customer_email TEXT,
        sku TEXT,
        status TEXT,
        order_date TEXT,
        FOREIGN KEY(sku) REFERENCES products(sku)
    )
    ''')
    
    # Limpiar datos viejos (Idempotencia)
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM orders")
    
    # --- DATOS DE PRUEBA (CASOS DE USO) ---
    
    # Productos
    products = [
        ('HEADPH-001', 'Auriculares Noise Cancelling', 50, 250.00),
        ('GAMING-LAP-99', 'Laptop Gamer Xtreme', 0, 1500.00), # ⚠️ STOCK 0 (Rotura de stock)
        ('TSHIRT-BASIC', 'Camiseta Algodón', 1000, 15.00)
    ]
    cursor.executemany("INSERT INTO products VALUES (?,?,?,?)", products)
    
    # Pedidos
    orders = [
        # Caso 1: Pedido Normal
        ('ORD-1001', 'juan@email.com', 'HEADPH-001', 'Delivered', '2025-12-01'),
        
        # Caso 2: El Pedido "Maldito" (Retrasado y sin stock)
        ('ORD-9902', 'cliente_furioso@gmail.com', 'GAMING-LAP-99', 'Processing', '2025-12-10'),
        
        # Caso 3: Pedido Reciente (No aplica devolución)
        ('ORD-2025', 'nuevo@email.com', 'TSHIRT-BASIC', 'Shipped', '2025-12-18')
    ]
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders)
    
    conn.commit()
    conn.close()
    print("✅ Base de datos poblada correctamente.")

def create_policy_pdf():
    print(f"📄 Generando Documento de Políticas en: {PDF_PATH}")
    
    c = canvas.Canvas(PDF_PATH, pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "SUPPLY CHAIN & CUSTOMER SERVICE POLICIES")
    c.drawString(50, height - 70, "Confidential - Internal Use Only")
    
    # Cuerpo del texto
    text_content = """
    1. POLÍTICA DE DEVOLUCIONES Y REEMBOLSOS
    
    1.1. Retrasos en el Envío:
    Si un pedido permanece en estado 'Processing' por más de 48 horas sin justificación,
    el cliente tiene derecho a un reembolso del 10% en forma de cupón o envío express gratuito.
    
    1.2. Roturas de Stock (Out of Stock):
    Si un producto pagado no tiene stock físico (Stock = 0), se debe ofrecer inmediatamente:
    a) Reembolso completo inmediato.
    b) Espera con un descuento del 15% adicional.
    
    1.3. Productos Electrónicos:
    Los laptops y auriculares no admiten devolución si el precinto está abierto,
    salvo defecto de fábrica confirmado.
    
    2. COMPENSACIONES AUTOMÁTICAS
    El agente de IA está autorizado a emitir reembolsos de hasta $50 sin supervisión humana.
    Para montos superiores, escalar a Manager.
    """
    
    c.setFont("Helvetica", 12)
    y_position = height - 120
    for line in text_content.split('\n'):
        c.drawString(50, y_position, line.strip())
        y_position -= 15
        
    c.save()
    print("✅ PDF generado correctamente.")

if __name__ == "__main__":
    create_database()
    create_policy_pdf()