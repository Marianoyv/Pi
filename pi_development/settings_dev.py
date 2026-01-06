from .settings import *
import os

# Modo desarrollo
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Usa GCS también en dev (usa settings_local para servir /static localmente)
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
STATICFILES_STORAGE = 'pi_development.storage.StaticRootGoogleCloudStorage'
DEFAULT_FILE_STORAGE = 'pi_development.storage.MediaRootGoogleCloudStorage'

# Ruta al archivo de credenciales si no viene de las variables de entorno
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(BASE_DIR / "credentials" / "pidevelopment-26f464065269.json")
