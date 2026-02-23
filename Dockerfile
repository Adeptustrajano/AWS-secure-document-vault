# Dockerfile para la API de FastAPI con enfoque en seguridad.   
#Principio de Mínimo Privilegio:creando un usuario no-root.
# Usamos una imagen base ligera de Python enfocada en seguridad: menor superficie de ataque
FROM python:3.11-slim

# Prevenir que Python escriba archivos .pyc y forzar logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# SEGURIDAD: Crear un usuario "no root" para ejecutar la app.
# Si alguien vulnera la app, no tendrá permisos de administrador en el contenedor.
RUN adduser --disabled-password --gecos "" appuser

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos primero los requerimientos para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la aplicación
COPY ./app ./app

# Cambiamos el propietario de los archivos al usuario seguro que creamos
RUN chown -R appuser:appuser /app

# Cambiamos del usuario root al usuario seguro
USER appuser

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Comando por defecto para iniciar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]