from django.contrib.sitemaps.views import sitemap
from django.urls import path

from pi_development.web.sitemaps import StaticViewSitemap

from . import views

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", views.index, name="index"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("systems/", views.systems, name="systems"),
    path("tools/", views.tools, name="tools"),
    path("tools/<slug:slug>/", views.tool_detail, name="tool_detail"),
    path("work/", views.work, name="work"),
    path("approach/", views.approach, name="approach"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("blog/", views.blog, name="blog"),
    path("policies/", views.policies, name="policies"),
    path("services/", views.legacy_services, name="services"),
    path("services/<slug:slug>/", views.legacy_service_page, name="service_page"),
    path("portfolio/", views.legacy_portfolio, name="portfolio"),
    path("process/", views.legacy_process, name="process_page"),
    path("resources/", views.legacy_resources, name="resources_page"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]
