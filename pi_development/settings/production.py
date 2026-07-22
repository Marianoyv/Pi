from django.core.exceptions import ImproperlyConfigured
from decouple import config

from . import base
from .base import *


def _required_csv_setting(name):
    values = base.csv_setting(name)
    if not values:
        raise ImproperlyConfigured(f"Missing required environment variable: {name}")
    return values


DEBUG = False
SECRET_KEY = config("SECRET_KEY")
SITE_URL = config("SITE_URL")
ALLOWED_HOSTS = _required_csv_setting("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = _required_csv_setting("CSRF_TRUSTED_ORIGINS")

# Cloud Run remains stateless until a real production database is introduced.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.dummy",
        "NAME": "stateless-production",
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
ENABLE_ADMIN = config("ENABLE_ADMIN", default=False, cast=bool)
ENABLE_REMOTE_URL_TOOLS = config("ENABLE_REMOTE_URL_TOOLS", default=False, cast=bool)

# WhiteNoise serves the collected static files directly from the container image.
MIDDLEWARE = [
    base.MIDDLEWARE[0],
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *base.MIDDLEWARE[1:],
]

if MIDDLEWARE[0] != "django.middleware.security.SecurityMiddleware":
    raise ImproperlyConfigured("SecurityMiddleware must be first in production.")

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
