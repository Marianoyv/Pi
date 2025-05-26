#!/bin/bash

# 🚀 DEPLOY PI DEVELOPMENT

# Paso 0: Validar entorno virtual activado
if [[ "$VIRTUAL_ENV" == "" ]]; then
  echo "⚠️  No tenés activado el entorno virtual (.venv)"
  echo "👉 Ejecutá: source .venv/Scripts/activate"
  exit 1
fi

# Paso 1: Subir archivos estáticos
echo "📦 1. Subiendo archivos estáticos a GCS..."
python upload_static_to_gcs.py || { echo "❌ Falló al subir archivos estáticos"; exit 1; }

# Paso 2: Build con Cloud Build
echo "🐳 2. Construyendo imagen Docker..."
gcloud builds submit --tag gcr.io/pidevelopment/pi-development || { echo "❌ Falló el build"; exit 1; }

# Paso 3: Deploy a Cloud Run
echo "🚢 3. Desplegando en Cloud Run..."
gcloud run deploy pi-development \
  --image gcr.io/pidevelopment/pi-development \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated || { echo "❌ Falló el deploy"; exit 1; }

echo "✅ ¡Despliegue completado exitosamente!"
