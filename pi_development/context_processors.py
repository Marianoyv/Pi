from django.conf import settings


def site_settings(request):
    """
    Exponer valores de configuración que se usan en plantillas base.
    """
    return {
        "site_url": getattr(settings, "SITE_URL", ""),
    }
