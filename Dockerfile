# Usar una imagen base de Python 3.12.4, que por defecto es Debian Bullseye
FROM python:3.12.4-bullseye

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copiar el archivo de requerimientos
COPY requirements.txt /app/

# Actualizar PIP e instalar las dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . /app
