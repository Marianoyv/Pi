from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        # Routes that exist in templates
        return ['index', 'about', 'contact', 'policies', 'portfolio']

    def location(self, item):
        return reverse(item)
