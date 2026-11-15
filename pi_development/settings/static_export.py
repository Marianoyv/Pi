"""Minimal build-time settings for the static Pi Development site."""

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = "static-build-only"
DEBUG = False
STATIC_EXPORT = True
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "pi_development.web",
]
MIDDLEWARE = []
ROOT_URLCONF = "pi_development.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "pi_development" / "web" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "pi_development.context_processors.site_settings",
            ]
        },
    }
]

DATABASES = {"default": {"ENGINE": "django.db.backends.dummy", "NAME": "static-build"}}
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_URL = os.environ.get("SITE_URL", "https://pidevelopment.web.app").rstrip("/")
GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", "G-6XVTWEY4LW")
ANALYTICS_ALLOWED_HOSTS = os.environ.get("ANALYTICS_ALLOWED_HOSTS", "pidevelopment.web.app,pidevelopment.firebaseapp.com")
GOOGLE_SITE_VERIFICATION = os.environ.get("GOOGLE_SITE_VERIFICATION", "")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "pidev.founder@gmail.com")
CONTACT_LOCATION = "Buenos Aires, Argentina"
CONTACT_PHONE = "+54 9 11 7061 9703"
CONTACT_PHONE_WA = "5491170619703"
CONTACT_FORM_ENABLED = False
ENABLE_REMOTE_URL_TOOLS = False

STATIC_URL = "/static/"
STATICFILES_DIRS = [("web", BASE_DIR / "static" / "web")]
STORAGES = {
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
