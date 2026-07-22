from dataclasses import dataclass
from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.template.response import TemplateResponse
from django.urls import reverse

from pi_development.web.knowledge_pages import get_public_knowledge_slugs
from pi_development.web.seo_pages import get_public_seo_page_slugs
from pi_development.web.tool_catalog import get_public_tool_slugs


@dataclass
class SitemapIndexItem:
    location: str
    last_mod: object = None


class BaseContentSitemap(Sitemap):
    protocol = "https"

    def get_protocol(self, protocol=None):
        parsed_site_url = urlsplit(getattr(settings, "SITE_URL", ""))
        return parsed_site_url.scheme or super().get_protocol(protocol)

    def get_domain(self, site=None):
        parsed_site_url = urlsplit(getattr(settings, "SITE_URL", ""))
        return parsed_site_url.netloc or super().get_domain(site)


class CorePageSitemap(BaseContentSitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return [
            "index",
            "solutions",
            "products",
            "adtech",
            "insights",
            "tools",
            "work",
            "company",
            "contact",
        ]

    def location(self, item):
        return reverse(item)


class ToolPageSitemap(BaseContentSitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return get_public_tool_slugs()

    def location(self, item):
        return reverse("tool_detail", kwargs={"slug": item})


class SeoPageSitemap(BaseContentSitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return get_public_seo_page_slugs()

    def location(self, item):
        return reverse("seo_page", kwargs={"slug": item})


class KnowledgePageSitemap(BaseContentSitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return get_public_knowledge_slugs()

    def location(self, item):
        return reverse("knowledge_page", kwargs={"slug": item})


def sitemap_index(request, sitemaps):
    base_url = getattr(settings, "SITE_URL", "").rstrip("/")
    sitemap_items = []

    for section, site in sitemaps.items():
        if callable(site):
            site = site()

        sitemap_url = f"{base_url}{reverse('sitemap_section', kwargs={'section': section})}"
        site_lastmod = site.get_latest_lastmod()
        sitemap_items.append(SitemapIndexItem(sitemap_url, site_lastmod))

        for page in range(2, site.paginator.num_pages + 1):
            sitemap_items.append(SitemapIndexItem(f"{sitemap_url}?p={page}", site_lastmod))

    return TemplateResponse(
        request,
        "sitemap_index.xml",
        {"sitemaps": sitemap_items},
        content_type="application/xml",
    )
