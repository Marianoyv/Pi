# Imagen base
FROM python:3.11-slim-bullseye

# Evita .pyc y buffer de logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Actualiza sistema base
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia el contenido del proyecto
COPY . /app

# Copia archivo .env.prod
COPY .env.prod /app/.env

# Instala dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Recolecta archivos estaticos
RUN python manage.py collectstatic --noinput

# Expone el puerto que usara Cloud Run
EXPOSE 8080
ENV PORT 8080

# Comando para iniciar el servidor con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "pi_development.wsgi:application"]
