from .settings_dev import *

# 🚫 Ignora Google Cloud y usa archivos estáticos locales
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Para que Django encuentre tus archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Recolecta en local si se usa collectstatic (opcional)
STATIC_ROOT = BASE_DIR / 'staticfiles'
