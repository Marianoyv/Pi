from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from pi_development.web.tool_catalog import get_public_tool_slugs


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return [
            "index",
            "systems",
            "tools",
            *[("tool_detail", slug) for slug in get_public_tool_slugs()],
            "work",
            "approach",
            "about",
            "contact",
            "blog",
            "policies",
        ]

    def location(self, item):
        if isinstance(item, tuple):
            name, slug = item
            return reverse(name, kwargs={"slug": slug})
        return reverse(item)
