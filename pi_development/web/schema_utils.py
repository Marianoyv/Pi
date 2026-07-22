import json


def _json(data):
    return json.dumps(data, ensure_ascii=False)


def build_organization_schema_json(site_url, logo_url, email="", telephone=""):
    organization = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{site_url}/#organization",
        "name": "Pi Development",
        "url": site_url,
        "logo": logo_url,
        "description": "Independent custom software and AdTech company based in Buenos Aires, Argentina.",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Buenos Aires",
            "addressCountry": "AR",
        },
        "areaServed": "Worldwide",
    }
    if email:
        organization["email"] = email
    if telephone:
        organization["telephone"] = telephone
    return _json(organization)


def build_website_schema_json(site_url):
    return _json(
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "@id": f"{site_url}/#website",
            "url": site_url,
            "name": "Pi Development",
            "description": "Custom software development, AI automation and AdTech engineering.",
            "publisher": {"@id": f"{site_url}/#organization"},
            "inLanguage": "en",
        }
    )


def build_breadcrumb_schema_json(items):
    if len(items) < 2:
        return None
    return _json(
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": position,
                    "name": item["name"],
                    "item": item["url"],
                }
                for position, item in enumerate(items, start=1)
            ],
        }
    )


def build_article_schema_json(page, url, site_url):
    if not page:
        return None
    return _json(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": page["h1"],
            "description": page["meta_description"],
            "url": url,
            "mainEntityOfPage": url,
            "author": {"@id": f"{site_url}/#organization"},
            "publisher": {"@id": f"{site_url}/#organization"},
            "inLanguage": "es",
        }
    )


def build_software_application_schema_json(tool, url):
    if not tool or not tool.get("is_live"):
        return None
    return _json(
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": tool["name"],
            "description": tool["meta_description"],
            "url": url,
            "applicationCategory": "WebApplication",
            "operatingSystem": "Web browser",
            "isAccessibleForFree": True,
        }
    )


def build_faq_schema_json(faqs):
    if not faqs:
        return None

    return _json(
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["answer"],
                    },
                }
                for item in faqs
            ],
        },
    )


def build_item_list_schema_json(name, items):
    if not items:
        return None

    return _json(
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": name,
            "mainEntity": {
                "@type": "ItemList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index,
                        "url": item["url"],
                        "name": item["name"],
                    }
                    for index, item in enumerate(items, start=1)
                ],
            },
        },
    )
