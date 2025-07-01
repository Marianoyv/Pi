# Imagen base
FROM python:3.11-slim-bullseye

# Actualiza sistema base
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia el contenido del proyecto
COPY . /app

# Copia archivo .env.prod
COPY .env.prod /app/.env

# Crea carpeta de credenciales y copia el archivo .json
RUN mkdir -p /app/credentials
COPY credentials/pidevelopment-d43bb26fcbc3.json /app/credentials/

# Instala dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Recolecta archivos estáticos
RUN python manage.py collectstatic --noinput

# Expone el puerto que usará Cloud Run
EXPOSE 8080
ENV PORT 8080

# Comando para iniciar el servidor con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "pi_development.wsgi:application"]
