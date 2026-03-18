import os
from pathlib import Path
from decouple import config


# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = config('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['*']

# Aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'pi_development.web',
    'storages',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL principal
ROOT_URLCONF = 'pi_development.urls'

# Plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'pi_development' / 'web' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pi_development.context_processors.site_settings',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'pi_development.wsgi.application'

# Base de datos local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseÃ±as
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# InternacionalizaciÃ³n
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

SITE_URL = config('SITE_URL', default='https://pidevelopment.web.app')

# Ruta a credenciales de Google
credentials_path = Path(config('GOOGLE_APPLICATION_CREDENTIALS'))
if not credentials_path.is_absolute():
    credentials_path = BASE_DIR / credentials_path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)

# ConfiguraciÃ³n de Google Cloud Storage
GS_BUCKET_NAME = config('GS_BUCKET_NAME')
GS_DEFAULT_ACL = None  # Requerido si el bucket tiene Uniform bucket-level access
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
STATICFILES_STORAGE = 'pi_development.storage.StaticRootGoogleCloudStorage'
DEFAULT_FILE_STORAGE = 'pi_development.storage.MediaRootGoogleCloudStorage'

# Ruta local de archivos estÃ¡ticos
STATICFILES_DIRS = [BASE_DIR / 'static']

# Requerido por Django
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = [
    'https://pidevelopment.web.app',
    'https://*.run.app',
]

# Campo por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




