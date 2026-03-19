from django.conf import settings

from pi_development.web.topic_clusters import get_discovery_seo_hub_pages


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
        "footer_seo_hubs": get_discovery_seo_hub_pages(),
    }
