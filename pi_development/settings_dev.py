from .settings import *

# 🔧 Modo desarrollo
DEBUG = True
ALLOWED_HOSTS = ["*"]

# 📂 Rutas de archivos estáticos (opcional si usás GCS)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# ✅ Activa GCS para archivos estáticos en desarrollo (podés desactivar con settings_local)
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# 🌍 ACL pública por defecto
GS_DEFAULT_ACL = 'publicRead'

# 🔐 Ruta al archivo de credenciales
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(BASE_DIR / "credentials" / "pidevelopment-d43bb26fcbc3.json")
