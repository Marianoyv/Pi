import importlib
import os
import sys
from unittest.mock import patch

from django.test import SimpleTestCase


class ProductionSettingsImportTests(SimpleTestCase):
    def test_production_settings_import_with_required_env(self):
        module_name = "pi_development.settings.production"
        sys.modules.pop(module_name, None)

        with patch.dict(
            os.environ,
            {
                "SECRET_KEY": "test-secret",
                "SITE_URL": "https://pidevelopment.web.app",
                "ALLOWED_HOSTS": "pidevelopment.web.app,.run.app",
                "CSRF_TRUSTED_ORIGINS": "https://pidevelopment.web.app,https://*.run.app",
            },
            clear=True,
        ):
            production = importlib.import_module(module_name)

        self.assertEqual(
            production.ALLOWED_HOSTS,
            ["pidevelopment.web.app", ".run.app"],
        )
        self.assertEqual(
            production.CSRF_TRUSTED_ORIGINS,
            ["https://pidevelopment.web.app", "https://*.run.app"],
        )
        self.assertEqual(production.MIDDLEWARE[0], "django.middleware.security.SecurityMiddleware")
        self.assertEqual(production.MIDDLEWARE[1], "whitenoise.middleware.WhiteNoiseMiddleware")
        self.assertEqual(production.SECURE_PROXY_SSL_HEADER, ("HTTP_X_FORWARDED_PROTO", "https"))
        self.assertTrue(production.SECURE_SSL_REDIRECT)
        self.assertTrue(production.SESSION_COOKIE_SECURE)
        self.assertTrue(production.CSRF_COOKIE_SECURE)
        self.assertTrue(production.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertEqual(production.SECURE_REFERRER_POLICY, "strict-origin-when-cross-origin")
        self.assertEqual(production.SECURE_CROSS_ORIGIN_OPENER_POLICY, "same-origin")
        self.assertEqual(production.SECURE_HSTS_SECONDS, 31536000)
        self.assertTrue(production.SECURE_HSTS_INCLUDE_SUBDOMAINS)
        self.assertFalse(production.SECURE_HSTS_PRELOAD)
        self.assertFalse(production.ENABLE_REMOTE_URL_TOOLS)

    def test_production_remote_tools_require_explicit_enablement(self):
        module_name = "pi_development.settings.production"
        sys.modules.pop(module_name, None)

        with patch.dict(
            os.environ,
            {
                "SECRET_KEY": "audit-only-placeholder",
                "SITE_URL": "https://example.com",
                "ALLOWED_HOSTS": "example.com",
                "CSRF_TRUSTED_ORIGINS": "https://example.com",
                "ENABLE_REMOTE_URL_TOOLS": "true",
            },
            clear=True,
        ):
            production = importlib.import_module(module_name)

        self.assertTrue(production.ENABLE_REMOTE_URL_TOOLS)
