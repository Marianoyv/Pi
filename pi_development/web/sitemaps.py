from dataclasses import dataclass
from datetime import date, datetime
from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.template.response import TemplateResponse
from django.urls import reverse

from pi_development.web.knowledge_pages import (
    get_knowledge_page,
    get_public_knowledge_slugs,
    get_recent_news_articles,
)
from pi_development.web.finance_catalog import get_finance_routes
from pi_development.web.seo_pages import get_public_seo_page_slugs
from pi_development.web.tool_catalog import get_public_tool_slugs
from pi_development.web.work_content import get_indexable_work_case_slugs


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
            "business_solutions",
            "web_plans",
            "solutions",
            "adtech",
            "insights",
            "products",
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
        return reverse("product_detail", kwargs={"slug": item})


class WorkCaseSitemap(BaseContentSitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return get_indexable_work_case_slugs()

    def location(self, item):
        return reverse("work_case", kwargs={"slug": item})


class FinancePageSitemap(BaseContentSitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return get_finance_routes()

    def location(self, item):
        return item


class SeoPageSitemap(BaseContentSitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return get_public_seo_page_slugs()

    def location(self, item):
        return reverse("seo_page", kwargs={"slug": item})


class KnowledgePageSitemap(BaseContentSitemap):
    priority = 0.7
    changefreq = "daily"

    def items(self):
        return [get_knowledge_page(slug) for slug in get_public_knowledge_slugs()]

    def location(self, item):
        return reverse("knowledge_page", kwargs={"slug": item["slug"]})

    def lastmod(self, item):
        value = item.get("updated_at") or item.get("published_at")
        return date.fromisoformat(value) if value else None


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

    news_articles = get_recent_news_articles()
    news_lastmod = None
    if news_articles:
        latest = news_articles[0].get("updated_datetime") or news_articles[0]["published_datetime"]
        news_lastmod = datetime.fromisoformat(latest)
    sitemap_items.append(SitemapIndexItem(f"{base_url}{reverse('sitemap_news')}", news_lastmod))

    return TemplateResponse(
        request,
        "sitemap_index.xml",
        {"sitemaps": sitemap_items},
        content_type="application/xml",
    )


def news_sitemap(request):
    site_url = getattr(settings, "SITE_URL", "").rstrip("/")
    return TemplateResponse(
        request,
        "news_sitemap.xml",
        {"articles": get_recent_news_articles(), "site_url": site_url},
        content_type="application/xml",
    )
