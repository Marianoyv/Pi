"""Views used only while rendering the static site."""

from urllib.parse import quote

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .company_pages import CONTACT_PAGE, get_company_page, get_home_page
from .forms import CreativePreviewLabForm, CreativeQAChecklistForm, UTMBuilderForm
from .knowledge_pages import (
    get_latest_knowledge_pages,
    get_knowledge_listing_groups,
    get_knowledge_page,
    get_related_knowledge_pages,
)
from .schema_utils import (
    build_article_schema_json,
    build_case_study_schema_json,
    build_faq_schema_json,
    build_item_list_schema_json,
    build_software_application_schema_json,
)
from .seo_pages import get_related_seo_pages, get_seo_page
from .tool_catalog import (
    get_featured_tool,
    get_public_tool_slugs,
    get_related_tools,
    get_tool,
    get_tool_groups,
    get_tools,
    get_tools_index_page,
)
from .tool_examples import get_tool_example
from .topic_clusters import (
    get_related_seo_pages_for_tool,
    get_topic_cluster_context_for_seo_page,
    get_topic_cluster_context_for_tool,
    get_topic_clusters_for_keys,
)
from .work_content import get_related_work_items, get_work_case, get_work_items, get_work_page


STATIC_TOOL_PAGES = {
    "utm-builder": (UTMBuilderForm, "web/utm_builder_page.html"),
    "creative-qa-checklist": (CreativeQAChecklistForm, "web/creative_qa_page.html"),
    "creative-preview-lab": (CreativePreviewLabForm, "web/creative_preview_lab_page.html"),
}


def index(request):
    return render(
        request,
        "web/company_home.html",
        {"home_page": get_home_page(), "latest_articles": get_latest_knowledge_pages(limit=3)},
    )


def favicon(request):
    return redirect(staticfiles_storage.url("web/img/pi.ico"), permanent=True)


def solutions(request):
    page = get_company_page("solutions")
    return render(
        request,
        "web/company_page.html",
        {
            "page": page,
            "structured_data_json": [item for item in [build_faq_schema_json(page.get("faqs"))] if item],
        },
    )


def business_solutions(request):
    page = get_company_page("business-solutions")
    phone = settings.CONTACT_PHONE_WA
    message = quote(
        "Hi Mariano, I would like to discuss a website or digital catalog for my business."
    )
    return render(
        request,
        "web/business_solutions_page.html",
        {
            "page": page,
            "page_language": "en",
            "og_locale": "en_US",
            "primary_cta_href": f"https://wa.me/{phone}?text={message}" if phone else reverse("contact"),
            "business_cases": [get_work_case("juno-metales"), get_work_case("taitet")],
            "structured_data_json": [item for item in [build_faq_schema_json(page.get("faqs"))] if item],
        },
    )


def web_plans(request):
    page = get_company_page("web-plans")
    phone = settings.CONTACT_PHONE_WA
    for plan in page["plans"]:
        message = quote(
            f"Hi Mariano, I would like to ask about the {plan['name']} plan for my business."
        )
        plan["cta_href"] = f"https://wa.me/{phone}?text={message}" if phone else reverse("contact")
    return render(
        request,
        "web/business_plans_page.html",
        {
            "page": page,
            "page_language": "en",
            "og_locale": "en_US",
            "structured_data_json": [item for item in [build_faq_schema_json(page.get("faqs"))] if item],
        },
    )


def adtech(request):
    page = get_company_page("adtech")
    public_slugs = set(get_public_tool_slugs())
    return render(
        request,
        "web/company_page.html",
        {
            "page": page,
            "tools_catalog": [tool for tool in get_tools() if tool["slug"] in public_slugs],
            "structured_data_json": [item for item in [build_faq_schema_json(page.get("faqs"))] if item],
        },
    )


def insights(request):
    knowledge_groups = _build_knowledge_listing_groups()
    site_url = settings.SITE_URL.rstrip("/")
    return render(
        request,
        "web/company_page.html",
        {
            "page": get_company_page("insights"),
            "knowledge_groups": knowledge_groups,
            "structured_data_json": [
                build_item_list_schema_json(
                    "Published technical insights",
                    [
                        {
                            "name": article["h1"],
                            "url": f"{site_url}{reverse('knowledge_page', kwargs={'slug': article['slug']})}",
                        }
                        for group in knowledge_groups
                        for article in group["pages"]
                    ],
                )
            ],
        },
    )


def tools(request):
    tools_page = get_tools_index_page()
    tools_catalog = get_tools()
    site_url = settings.SITE_URL.rstrip("/")
    return render(
        request,
        "web/tools_page.html",
        {
            "tools_page": tools_page,
            "featured_tool": get_featured_tool(),
            "tools_catalog": tools_catalog,
            "tool_groups": get_tool_groups(),
            "topic_clusters": [],
            "structured_data_json": [
                build_item_list_schema_json(
                    tools_page["catalog_title"],
                    [
                        {
                            "name": tool["name"],
                            "url": f"{site_url}{reverse('product_detail', kwargs={'slug': tool['slug']})}",
                        }
                        for tool in tools_catalog
                    ],
                )
            ],
        },
    )


def tool_detail(request, slug):
    if slug not in STATIC_TOOL_PAGES:
        raise Http404("Tool not found.")

    tool = get_tool(slug)
    if not tool or slug not in get_public_tool_slugs():
        raise Http404("Tool not found.")

    form_class, template_name = STATIC_TOOL_PAGES[slug]
    related_seo_pages = get_related_seo_pages_for_tool(slug)
    topic_cluster = get_topic_cluster_context_for_tool(slug)
    if tool.get("public_visibility"):
        related_seo_pages = []
        topic_cluster = None

    return render(
        request,
        template_name,
        {
            "tool": tool,
            "related_tools": get_related_tools(slug),
            "related_seo_pages": related_seo_pages,
            "topic_cluster": topic_cluster,
            "tool_example": get_tool_example(slug),
            "tool_example_used": False,
            "structured_data_json": _build_tool_structured_data(tool),
            "form": form_class(),
        },
    )


def legacy_tools(request):
    return redirect("products", permanent=True)


def legacy_tool_detail(request, slug):
    return redirect("product_detail", slug=slug, permanent=True)


def work(request):
    work_items = get_work_items()
    site_url = settings.SITE_URL.rstrip("/")
    return render(
        request,
        "web/work_page.html",
        {
            "work_page": get_work_page(),
            "work_items": work_items,
            "structured_data_json": [
                build_item_list_schema_json(
                    "Pi Development product and software case studies",
                    [{"name": item["name"], "url": f"{site_url}{item['internal_url']}"} for item in work_items],
                )
            ],
        },
    )


def work_case(request, slug):
    case = get_work_case(slug)
    if not case:
        raise Http404("Case study not found.")
    site_url = settings.SITE_URL.rstrip("/")
    case_url = f"{site_url}{reverse('work_case', kwargs={'slug': slug})}"
    return render(
        request,
        "web/work_case_page.html",
        {
            "case": case,
            "related_work": get_related_work_items(
                case["supported_commercial_pillar"],
                exclude_slug=case["slug"],
            ),
            "structured_data_json": [build_case_study_schema_json(case, case_url, site_url)],
        },
    )


def company(request):
    return render(request, "web/company_page.html", {"page": get_company_page("company")})


def contact(request):
    phone = settings.CONTACT_PHONE_WA
    message = quote("Hello Mariano, I would like to ask about a possible Pi Development project.")
    return render(
        request,
        "web/company_page.html",
        {
            "page": CONTACT_PAGE,
            "contact_form_enabled": False,
            "contact_whatsapp_base_url": f"https://wa.me/{phone}" if phone else "",
            "contact_whatsapp_url": f"https://wa.me/{phone}?text={message}" if phone else "",
            "contact_phone": settings.CONTACT_PHONE,
        },
    )


def knowledge_page(request, slug):
    page = get_knowledge_page(slug)
    if not page:
        raise Http404("Page not found.")
    page_language = page.get("language", "es")
    related_tools = [tool for tool in (get_tool(item) for item in page.get("related_tool_slugs", [])) if tool]
    topic_clusters = get_topic_clusters_for_keys([page["cluster_key"]])
    site_url = settings.SITE_URL.rstrip("/")
    page_url = f"{site_url}{reverse('knowledge_page', kwargs={'slug': slug})}"
    return render(
        request,
        "web/knowledge_article_page.html",
        {
            "knowledge_page": page,
            "page_language": page_language,
            "og_locale": "en_US" if page_language == "en" else "es_AR",
            "hreflang_links": [{"code": page_language, "url": page_url}],
            "related_tools": related_tools,
            "related_seo_pages": get_related_seo_pages(page.get("related_seo_page_slugs", [])),
            "related_knowledge_pages": get_related_knowledge_pages(page.get("related_knowledge_slugs", [])),
            "topic_cluster": topic_clusters[0] if topic_clusters else None,
            "structured_data_json": [
                item
                for item in [
                    build_article_schema_json(page, page_url, site_url),
                    build_faq_schema_json(page.get("faqs")),
                ]
                if item
            ],
        },
    )


def seo_page(request, slug):
    page = get_seo_page(slug)
    if not page:
        raise Http404("Page not found.")
    return render(
        request,
        "web/seo_landing_page.html",
        {
            "seo_page": page,
            "primary_tool": get_tool(page["primary_tool_slug"]),
            "related_tools": [
                tool for tool in (get_tool(item) for item in page.get("related_tool_slugs", [])) if tool
            ],
            "related_pages": get_related_seo_pages(page.get("related_page_slugs", [])),
            "topic_cluster": get_topic_cluster_context_for_seo_page(slug),
            "hub_sections": _build_seo_page_hub_sections(page),
            "hub_use_cases": page.get("hub_use_cases", []),
            "structured_data_json": [item for item in [build_faq_schema_json(page.get("faqs"))] if item],
        },
    )


def policies(request):
    return render(request, "web/policies.html")


def robots_txt(request):
    sitemap_url = f"{settings.SITE_URL.rstrip('/')}{reverse('sitemap')}"
    return HttpResponse(
        "\n".join(["User-agent: *", "Allow: /", f"Sitemap: {sitemap_url}"]),
        content_type="text/plain",
    )


def _build_tool_structured_data(tool):
    faq_schema = build_faq_schema_json(((tool.get("editorial") or {}).get("faqs") or []))
    tool_url = f"{settings.SITE_URL.rstrip('/')}{reverse('product_detail', kwargs={'slug': tool['slug']})}"
    software_schema = build_software_application_schema_json(tool, tool_url)
    return [item for item in [software_schema, faq_schema] if item]


def _build_seo_page_hub_sections(page):
    sections = []
    for section in page.get("hub_sections", []):
        clusters = get_topic_clusters_for_keys([section["cluster_key"]], current_seo_slug=page["slug"])
        section_context = dict(section)
        section_context["cluster"] = clusters[0] if clusters else None
        sections.append(section_context)
    return sections


def _build_knowledge_listing_groups():
    groups = []
    for group in get_knowledge_listing_groups():
        clusters = get_topic_clusters_for_keys([group["cluster_key"]])
        group_context = dict(group)
        group_context["cluster"] = clusters[0] if clusters else None
        groups.append(group_context)
    return groups
