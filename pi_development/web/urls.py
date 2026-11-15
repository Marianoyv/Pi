from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import (
    CorePageSitemap,
    KnowledgePageSitemap,
    SeoPageSitemap,
    ToolPageSitemap,
    WorkCaseSitemap,
    news_sitemap,
    sitemap_index,
)


sitemaps = {
    "pages": CorePageSitemap,
    "tools": ToolPageSitemap,
    "work": WorkCaseSitemap,
    "seo": SeoPageSitemap,
    "content": KnowledgePageSitemap,
}

urlpatterns = [
    path("", views.index, name="index"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("soluciones-para-negocios/", views.business_solutions, name="business_solutions"),
    path("planes-web/", views.web_plans, name="web_plans"),
    path("solutions/", views.solutions, name="solutions"),
    path("adtech/", views.adtech, name="adtech"),
    path("insights/", views.insights, name="insights"),
    path("products/", views.tools, name="products"),
    path("products/<slug:slug>/", views.tool_detail, name="product_detail"),
    path("tools/", views.legacy_tools, name="legacy_tools"),
    path("tools/<slug:slug>/", views.legacy_tool_detail, name="legacy_tool_detail"),
    path("work/", views.work, name="work"),
    path("work/<slug:slug>/", views.work_case, name="work_case"),
    path("company/", views.company, name="company"),
    path("contact/", views.contact, name="contact"),
    path("blog/<slug:slug>/", views.knowledge_page, name="knowledge_page"),
    path("policies/", views.policies, name="policies"),
    path("<slug:slug>/", views.seo_page, name="seo_page"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_index, {"sitemaps": sitemaps}, name="sitemap"),
    path("sitemap-news.xml", news_sitemap, name="sitemap_news"),
    path("sitemap-<section>.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap_section"),
]
