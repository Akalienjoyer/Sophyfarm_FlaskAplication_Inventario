# Imagen base con Python
FROM python:3.12-slim

# Crear carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos de requerimientos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto donde correrá Flask
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "run.py"]
