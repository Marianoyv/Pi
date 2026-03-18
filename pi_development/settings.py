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
    'pi_development.middleware.CleanHtmlResponseMiddleware',
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

# Validadores de contrasenas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalizacion
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

SITE_URL = config('SITE_URL', default='https://pidevelopment.web.app')
CONTACT_EMAIL = config('CONTACT_EMAIL', default='pidev.founder@gmail.com')
CONTACT_PHONE = config('CONTACT_PHONE', default='+54 9 11 7061 9703')
CONTACT_PHONE_WA = config('CONTACT_PHONE_WA', default='5491170619703')
CONTACT_LOCATION = config('CONTACT_LOCATION', default='Buenos Aires, Argentina')
PAGESPEED_API_KEY = config('PAGESPEED_API_KEY', default='')
PAGESPEED_API_ENDPOINT = config(
    'PAGESPEED_API_ENDPOINT',
    default='https://www.googleapis.com/pagespeedonline/v5/runPagespeed',
)
TOOLS_HTTP_TIMEOUT = config('TOOLS_HTTP_TIMEOUT', default=12, cast=int)
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
OPENAI_API_BASE = config('OPENAI_API_BASE', default='https://api.openai.com/v1')
OPENAI_AUDITOR_MODEL = config('OPENAI_AUDITOR_MODEL', default='')

# Ruta a credenciales de Google
credentials_path = Path(config('GOOGLE_APPLICATION_CREDENTIALS'))
if not credentials_path.is_absolute():
    credentials_path = BASE_DIR / credentials_path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)

# Configuracion de Google Cloud Storage
GS_BUCKET_NAME = config('GS_BUCKET_NAME')
GS_DEFAULT_ACL = None
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
STATICFILES_STORAGE = 'pi_development.storage.StaticRootGoogleCloudStorage'
DEFAULT_FILE_STORAGE = 'pi_development.storage.MediaRootGoogleCloudStorage'

# Ruta local de archivos estaticos
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
