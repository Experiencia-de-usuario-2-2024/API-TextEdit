# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requirements.txt al contenedor
COPY requirements.txt requirements.txt

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación al contenedor
COPY . .

# Exponer el puerto que la aplicación usará
EXPOSE 3030

# Configurar el comando por defecto para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app"]
