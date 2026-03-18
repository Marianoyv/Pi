from django.contrib.sitemaps.views import sitemap
from django.urls import path

from pi_development.web.sitemaps import ServicePageSitemap, StaticViewSitemap

from . import views

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServicePageSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.content_page, {'section': 'services'}, name='service_page'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('policies/', views.policies, name='policies'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('blog/', views.blog, name='blog'),
    path('process/', views.content_page, {'section': 'sections', 'slug': 'process'}, name='process_page'),
    path('resources/', views.content_page, {'section': 'sections', 'slug': 'resources'}, name='resources_page'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
