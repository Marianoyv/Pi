from django.contrib.sitemaps.views import sitemap
from django.urls import path

from pi_development.web.sitemaps import (
    CorePageSitemap,
    KnowledgePageSitemap,
    SeoPageSitemap,
    ToolPageSitemap,
    sitemap_index,
)

from . import views

sitemaps = {
    "pages": CorePageSitemap,
    "tools": ToolPageSitemap,
    "seo": SeoPageSitemap,
    "content": KnowledgePageSitemap,
}

urlpatterns = [
    path("", views.index, name="index"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("solutions/", views.solutions, name="solutions"),
    path("products/", views.products, name="products"),
    path("adtech/", views.adtech, name="adtech"),
    path("labs/", views.labs, name="labs"),
    path("insights/", views.insights, name="insights"),
    path("systems/", views.systems, name="systems"),
    path("tools/", views.tools, name="tools"),
    path("tools/<slug:slug>/", views.tool_detail, name="tool_detail"),
    path("work/", views.work, name="work"),
    path("case-studies/", views.case_studies, name="case_studies"),
    path("approach/", views.approach, name="approach"),
    path("company/", views.company, name="company"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("rebuild/", views.rebuild_home, name="rebuild_home"),
    path("rebuild/<slug:slug>/", views.rebuild_page, name="rebuild_page"),
    path("blog/<slug:slug>/", views.knowledge_page, name="knowledge_page"),
    path("blog/", views.blog, name="blog"),
    path("policies/", views.policies, name="policies"),
    path("services/", views.legacy_services, name="services"),
    path("services/<slug:slug>/", views.legacy_service_page, name="service_page"),
    path("portfolio/", views.legacy_portfolio, name="portfolio"),
    path("process/", views.legacy_process, name="process_page"),
    path("resources/", views.legacy_resources, name="resources_page"),
    path("<slug:slug>/", views.seo_page, name="seo_page"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_index, {"sitemaps": sitemaps}, name="sitemap"),
    path("sitemap-<section>.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap_section"),
]
