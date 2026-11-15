from django.conf import settings

from pi_development.web.schema_utils import (
    build_breadcrumb_schema_json,
    build_organization_schema_json,
    build_person_schema_json,
    build_website_schema_json,
)

from pi_development.web.topic_clusters import get_discovery_seo_hub_pages


def site_settings(request):
    site_url = getattr(settings, "SITE_URL", "").rstrip("/")
    canonical_url = f"{site_url}{request.path}" if site_url else request.build_absolute_uri(request.path)

    route_name = getattr(getattr(request, "resolver_match", None), "url_name", "") or ""
    route_labels = {
        "business_solutions": "Business solutions",
        "web_plans": "Website plans",
        "solutions": "Solutions",
        "products": "Products",
        "adtech": "AdTech",
        "insights": "Insights",
        "product_detail": "Product",
        "work_case": "Case study",
        "work": "Work",
        "company": "Company",
        "contact": "Contact",
        "knowledge_page": "Insight",
        "seo_page": "Technical guide",
        "policies": "Policies",
    }
    breadcrumbs = [{"name": "Home", "url": f"{site_url}/"}]
    if request.path != "/" and route_name in route_labels:
        if route_name in {"product_detail"}:
            breadcrumbs.append({"name": "Products", "url": f"{site_url}/products/"})
        elif route_name == "work_case":
            breadcrumbs.append({"name": "Work", "url": f"{site_url}/work/"})
        elif route_name in {"knowledge_page", "seo_page"}:
            breadcrumbs.append({"name": "Insights", "url": f"{site_url}/insights/"})
        breadcrumbs.append({"name": route_labels[route_name], "url": canonical_url})

    logo_url = f"{site_url}{settings.STATIC_URL}web/img/pi.png"
    global_structured_data_json = [
        build_organization_schema_json(
            site_url=site_url,
            logo_url=logo_url,
            email=getattr(settings, "CONTACT_EMAIL", ""),
            telephone="",
        ),
        build_person_schema_json(site_url),
        build_website_schema_json(site_url),
    ]
    breadcrumb_schema = build_breadcrumb_schema_json(breadcrumbs)
    if breadcrumb_schema:
        global_structured_data_json.append(breadcrumb_schema)

    page_language = "es" if route_name == "knowledge_page" else "en"

    return {
        "site_url": site_url,
        "canonical_url": canonical_url,
        "contact_email": getattr(settings, "CONTACT_EMAIL", ""),
        "contact_location": getattr(settings, "CONTACT_LOCATION", ""),
        "google_analytics_id": getattr(settings, "GOOGLE_ANALYTICS_ID", ""),
        "analytics_allowed_hosts": getattr(settings, "ANALYTICS_ALLOWED_HOSTS", ""),
        "google_site_verification": getattr(settings, "GOOGLE_SITE_VERIFICATION", ""),
        "analytics_page_type": route_name or "not_found",
        "static_export": bool(getattr(settings, "STATIC_EXPORT", False)),
        "footer_seo_hubs": get_discovery_seo_hub_pages(),
        "page_language": page_language,
        "og_locale": "es_AR" if page_language == "es" else "en_US",
        "hreflang_links": [{"code": page_language, "url": canonical_url}],
        "x_default_url": canonical_url,
        "global_structured_data_json": global_structured_data_json,
    }
