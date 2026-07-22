from pathlib import Path

from decouple import config


def csv_setting(name, default=""):
    raw_value = config(name, default=default)
    return [item.strip() for item in raw_value.split(",") if item.strip()]


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-local-only")
DEBUG = False
ALLOWED_HOSTS = csv_setting("ALLOWED_HOSTS", default="localhost,127.0.0.1,testserver")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "pi_development.web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "pi_development.middleware.CleanHtmlResponseMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pi_development.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "pi_development" / "web" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pi_development.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "pi_development.wsgi.application"
ASGI_APPLICATION = "pi_development.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("es", "Spanish"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

SITE_URL = config("SITE_URL", default="https://pidevelopment.web.app")
GOOGLE_ANALYTICS_ID = config("GOOGLE_ANALYTICS_ID", default="")
GOOGLE_SITE_VERIFICATION = config("GOOGLE_SITE_VERIFICATION", default="")
CONTACT_EMAIL = config("CONTACT_EMAIL", default="pidev.founder@gmail.com")
CONTACT_PHONE = config("CONTACT_PHONE", default="+54 9 11 7061 9703")
CONTACT_PHONE_WA = config("CONTACT_PHONE_WA", default="5491170619703")
CONTACT_LOCATION = config("CONTACT_LOCATION", default="Buenos Aires, Argentina")
PAGESPEED_API_KEY = config("PAGESPEED_API_KEY", default="")
PAGESPEED_API_ENDPOINT = config(
    "PAGESPEED_API_ENDPOINT",
    default="https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
)
TOOLS_HTTP_TIMEOUT = config("TOOLS_HTTP_TIMEOUT", default=12, cast=int)
ENABLE_REMOTE_URL_TOOLS = config("ENABLE_REMOTE_URL_TOOLS", default=False, cast=bool)
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
OPENAI_API_BASE = config("OPENAI_API_BASE", default="https://api.openai.com/v1")
OPENAI_AUDITOR_MODEL = config("OPENAI_AUDITOR_MODEL", default="")

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    ("web", BASE_DIR / "static" / "web"),
]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.db"
ENABLE_ADMIN = True

CSRF_TRUSTED_ORIGINS = csv_setting(
    "CSRF_TRUSTED_ORIGINS",
    default="http://127.0.0.1:8000,http://localhost:8000",
)
USE_X_FORWARDED_HOST = False
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOG_LEVEL = config("LOG_LEVEL", default="INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
