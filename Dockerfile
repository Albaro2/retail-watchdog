# 1. Imagen base ligera de Python
FROM python:3.11-slim

# 2. Variables de entorno para optimizar Python en contenedores
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo
WORKDIR /app

# 4. Instalar dependencias de sistema (SQLite es vital para tu DB)
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalar librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el código fuente y datos
COPY src/ src/
COPY data/ data/
COPY chainlit.md .

# 7. Exponer el puerto
EXPOSE 8000

# 8. Comando de arranque
CMD ["chainlit", "run", "src/app.py", "--host", "0.0.0.0", "--port", "8000"]
