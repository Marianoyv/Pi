from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from pi_development.web.knowledge_pages import get_public_knowledge_slugs
from pi_development.web.seo_pages import get_public_seo_page_slugs
from pi_development.web.tool_catalog import get_public_tool_slugs


class BaseContentSitemap(Sitemap):
    protocol = "https"


class CorePageSitemap(BaseContentSitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return [
            "index",
            "systems",
            "tools",
            "blog",
            "work",
            "approach",
            "about",
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
