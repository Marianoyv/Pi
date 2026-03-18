from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .views import SERVICE_PAGES


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'index',
            'services',
            'about',
            'contact',
            'policies',
            'portfolio',
            'blog',
            'process_page',
            'resources_page',
        ]

    def location(self, item):
        return reverse(item)


class ServicePageSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return list(SERVICE_PAGES.keys())

    def location(self, item):
        return reverse('service_page', kwargs={'slug': item})
