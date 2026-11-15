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
        "description": "Founder-led product development, operational software and AdTech engineering studio based in Buenos Aires, Argentina.",
        "founder": {"@id": f"{site_url}/#mariano-tami"},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Buenos Aires",
            "addressCountry": "AR",
        },
    }
    if email:
        organization["email"] = email
    if telephone:
        organization["telephone"] = telephone
    return _json(organization)


def build_person_schema_json(site_url):
    return _json(
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "@id": f"{site_url}/#mariano-tami",
            "name": "Mariano Tami",
            "url": f"{site_url}/company/",
            "jobTitle": "Founder · AdTech, Web Monetization & Product Development",
            "description": (
                "Founder of Pi Development, a self-taught software developer and AdTech practitioner based in Buenos Aires."
            ),
            "homeLocation": {
                "@type": "Place",
                "name": "Buenos Aires, Argentina",
            },
            "knowsLanguage": ["Spanish", "English"],
            "knowsAbout": [
                "AdTech engineering",
                "Publisher monetization",
                "Product development",
                "Operational software",
                "Digital analytics",
                "SEO and web measurement",
            ],
            "worksFor": {"@id": f"{site_url}/#organization"},
        }
    )


def build_website_schema_json(site_url):
    return _json(
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "@id": f"{site_url}/#website",
            "url": site_url,
            "name": "Pi Development",
            "description": "Product development, operational software and AdTech engineering.",
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
    image_url = ""
    if page.get("image"):
        image_url = f"{site_url}/static/{page['image'].lstrip('/')}"
    article = {
        "@context": "https://schema.org",
        "@type": "NewsArticle" if page.get("article_type") == "news" else "Article",
        "headline": page["h1"],
        "description": page["meta_description"],
        "url": url,
        "mainEntityOfPage": url,
        "author": {"@id": f"{site_url}/#mariano-tami"},
        "publisher": {"@id": f"{site_url}/#organization"},
        "inLanguage": page.get("language", "es"),
        "isAccessibleForFree": True,
    }
    if image_url:
        article["image"] = {
            "@type": "ImageObject",
            "url": image_url,
            "width": 1536,
            "height": 864,
            "caption": page.get("image_alt", page["h1"]),
        }
    published = page.get("published_datetime") or page.get("published_at")
    updated = page.get("updated_datetime") or page.get("updated_at")
    if published:
        article["datePublished"] = published
    if updated:
        article["dateModified"] = updated
    if page.get("eyebrow"):
        article["articleSection"] = page["eyebrow"]
    if page.get("sources"):
        article["citation"] = [source["url"] for source in page["sources"]]
    return _json(article)


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


def build_case_study_schema_json(case, url, site_url):
    if not case or not case.get("public_visibility"):
        return None

    return _json(
        {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "@id": f"{url}#case-study",
            "name": case["name"],
            "headline": f"{case['name']} case study",
            "description": case["summary"],
            "url": url,
            "sameAs": case["external_url"] if case.get("external_link_available") else None,
            "datePublished": case.get("date_published"),
            "creator": {"@id": f"{site_url}/#mariano-tami"},
            "publisher": {"@id": f"{site_url}/#organization"},
            "inLanguage": "en",
            "keywords": case["technologies"],
        }
    )
