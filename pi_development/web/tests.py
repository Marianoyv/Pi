from django.test import TestCase
from django.urls import reverse


class PublicPagesTests(TestCase):
    def test_static_pages_respond(self):
        for name in [
            'index',
            'services',
            'about',
            'contact',
            'policies',
            'portfolio',
            'blog',
            'process_page',
            'resources_page',
            'sitemap',
        ]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_service_pages_respond(self):
        for slug in ['web-development', 'ux-ui', 'marketing', 'seo']:
            with self.subTest(slug=slug):
                response = self.client.get(reverse('service_page', kwargs={'slug': slug}))
                self.assertEqual(response.status_code, 200)

    def test_unknown_service_returns_404(self):
        response = self.client.get(reverse('service_page', kwargs={'slug': 'unknown'}))
        self.assertEqual(response.status_code, 404)
