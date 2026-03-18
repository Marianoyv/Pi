from django.conf import settings


def site_settings(request):
    """
    Exponer valores de configuracion que se usan en plantillas base.
    """
    return {
        "site_url": getattr(settings, "SITE_URL", ""),
        "contact_email": getattr(settings, "CONTACT_EMAIL", ""),
        "contact_phone": getattr(settings, "CONTACT_PHONE", ""),
        "contact_phone_wa": getattr(settings, "CONTACT_PHONE_WA", ""),
        "contact_location": getattr(settings, "CONTACT_LOCATION", ""),
    }
