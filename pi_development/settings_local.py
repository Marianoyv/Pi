from .settings_dev import *

# Ignora Google Cloud y usa archivos estáticos locales
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/media/'

# Para que Django encuentre tus archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Recolecta en local si se usa collectstatic (opcional)
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'
