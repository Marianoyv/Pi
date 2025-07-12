from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('policies/', views.policies, name='policies'),
    path('portfolio/', views.portfolio, name='portfolio'),

    # path('projects/', views.projects, name='projects'),  # Enable when template is ready
]

from django.contrib.sitemaps.views import sitemap
from pi_development.web.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
path('robots.txt', views.robots_txt, name='robots_txt'),
