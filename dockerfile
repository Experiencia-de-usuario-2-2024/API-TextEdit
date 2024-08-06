# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias necesarias del sistema y Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev python3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Deshabilitar las opciones de OneDNN
ENV DNNL_DISABLE_CHECKS=1

# Copiar el resto de la aplicación al contenedor
COPY . .

# Exponer el puerto que la aplicación usará
EXPOSE 8000

# Configurar el comando por defecto para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
