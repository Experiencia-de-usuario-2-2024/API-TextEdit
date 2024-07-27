# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias necesarias del sistema
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev && \
    apt-get clean

# Instalar las dependencias de Python
RUN pip install --upgrade pip

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación al contenedor
COPY . .

# Exponer el puerto que la aplicación usará
EXPOSE 8000

# Configurar el comando por defecto para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]