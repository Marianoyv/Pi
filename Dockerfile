# Imagen base actualizada
FROM python:3.11-slim-bullseye

# Actualiza los paquetes del sistema operativo para mitigar vulnerabilidades
RUN apt-get update && apt-get upgrade -y && apt-get clean;


# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Actualiza pip y las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Recolecta los archivos estáticos
RUN python manage.py collectstatic --noinput

# Expone el puerto que Google Cloud Run usará
EXPOSE 8080

# Define la variable de entorno para el puerto
ENV PORT 8080

# Comando para iniciar el servidor de producción con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "pi_development.wsgi:application"]

