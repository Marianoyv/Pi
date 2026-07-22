from unittest.mock import patch
from pathlib import Path
import re
from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.test import TestCase, override_settings
from django.urls import reverse

from pi_development.web.knowledge_pages import get_knowledge_page, get_public_knowledge_slugs
from pi_development.web.seo_pages import get_public_seo_page_slugs, get_seo_page
from pi_development.web.services.tools.adtech_debug import build_insight as build_adtech_insight
from pi_development.web.services.tools.ai_auditor import build_insight as build_ai_auditor_insight
from pi_development.web.services.tools.creative_preview_lab import run_creative_preview_lab
from pi_development.web.services.tools.creative_qa import run_creative_qa
from pi_development.web.services.tools.landing_snapshot import build_insight as build_landing_snapshot_insight
from pi_development.web.tool_catalog import get_public_tool_slugs, get_tool
from pi_development.web.tool_examples import get_tool_example
from pi_development.web.topic_clusters import get_discovery_seo_hub_pages, get_topic_cluster_context_for_seo_page


@override_settings(ENABLE_REMOTE_URL_TOOLS=True)
class PublicPagesTests(TestCase):
    def test_rebuild_preview_pages_render_in_isolation(self):
        routes = [
            ("rebuild_home", {}, "Think clearly. Build what matters."),
            ("rebuild_page", {"slug": "studio"}, "Independent by design."),
            ("rebuild_page", {"slug": "capabilities"}, "Technology shaped around the problem."),
            ("rebuild_page", {"slug": "ad-products"}, "Advertising should be engineered."),
            ("rebuild_page", {"slug": "research"}, "Research before certainty."),
            ("rebuild_page", {"slug": "insights"}, "Ideas become useful when they can be examined."),
            ("rebuild_page", {"slug": "about"}, "Built to become larger than its founder."),
            ("rebuild_page", {"slug": "contact"}, "Bring a problem"),
        ]

        for name, kwargs, expected_title in routes:
            with self.subTest(name=name, kwargs=kwargs):
                response = self.client.get(reverse(name, kwargs=kwargs))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "web/rebuild/page.html")
                self.assertTemplateUsed(response, "web/rebuild/base.html")
                self.assertContains(response, expected_title)
                self.assertContains(response, '<html lang="en">', html=False)
                self.assertContains(response, 'class="pi-site"', html=False)
                self.assertContains(response, 'web/rebuild/site.css', html=False)
                self.assertContains(response, 'web/rebuild/site.js', html=False)
                self.assertContains(response, 'href="#main-content"', html=False)
                self.assertContains(response, '<main class="pi-site-main', html=False)
                self.assertContains(response, "Bring a problem")
                self.assertNotContains(response, 'web/css/tools.css', html=False)
                self.assertNotContains(response, 'web/js/main.js', html=False)

    def test_rebuild_navigation_uses_institutional_route_map_only(self):
        response = self.client.get(reverse("rebuild_home"))
        self.assertContains(response, 'href="/rebuild/"', html=False)
        for path in [
            "/rebuild/studio/",
            "/rebuild/capabilities/",
            "/rebuild/ad-products/",
            "/rebuild/research/",
            "/rebuild/insights/",
            "/rebuild/about/",
            "/rebuild/contact/",
        ]:
            self.assertContains(response, f'href="{path}"', html=False)

        for legacy_nav_path in ["/tools/", "/work/", "/portfolio/", "/systems/", "/approach/", "/blog/"]:
            self.assertNotContains(response, f'href="{legacy_nav_path}"', html=False)

    def test_rebuild_navigation_has_accessible_mobile_controls(self):
        response = self.client.get(reverse("rebuild_page", kwargs={"slug": "studio"}))
        self.assertContains(response, 'aria-label="Institutional navigation"', html=False)
        self.assertContains(response, 'aria-controls="pi-mobile-navigation"', html=False)
        self.assertContains(response, 'aria-expanded="false"', html=False)
        self.assertContains(response, 'data-pi-menu-toggle', html=False)
        self.assertContains(response, 'aria-current="page"', html=False)
        self.assertContains(response, 'data-pi-event="nav_click"', html=False)

    def test_rebuild_home_renders_requested_sections_without_unsupported_proof(self):
        response = self.client.get(reverse("rebuild_home"))
        for heading in [
            "Start with the problem.",
            "What we work on.",
            "A disciplined way to build.",
            "Advertising should be engineered.",
            "Research before certainty.",
            "What we are learning.",
            "What needs to work better?",
        ]:
            self.assertContains(response, heading)

        for unsupported_content in ["Juno", "Testimonials", "client logos", "metrics"]:
            self.assertNotContains(response, unsupported_content)

    def test_rebuild_contact_form_validates_server_side(self):
        response = self.client.get(reverse("rebuild_page", kwargs={"slug": "contact"}))
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, 'data-pi-event="contact_form"', html=False)
        self.assertContains(response, 'data-pi-event="contact_submit"', html=False)
        for label in [
            "Name",
            "Email",
            "Company or organization",
            "Role",
            "Problem or opportunity",
            "Current situation",
            "Desired outcome",
            "Timeline",
            "Budget range",
            "Relevant links",
        ]:
            self.assertContains(response, label)

        response = self.client.post(reverse("rebuild_page", kwargs={"slug": "contact"}), data={})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertContains(response, 'aria-invalid="true"', html=False)

    @override_settings(CONTACT_EMAIL="contact@example.com")
    @patch("pi_development.web.views.send_mail")
    def test_rebuild_contact_form_success_uses_existing_email_channel(self, mock_send_mail):
        response = self.client.post(
            reverse("rebuild_page", kwargs={"slug": "contact"}),
            data={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "company": "Analytical Engine",
                "role": "Research lead",
                "project_type": "ai-or-automation",
                "problem": "Repeated analysis needs a clearer system.",
                "current_situation": "Work is handled manually across documents.",
                "desired_outcome": "A reviewed workflow with better visibility.",
                "timeline": "This quarter",
                "budget_range": "To be discussed",
                "relevant_links": "https://example.com/context",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Thank you. Your message has been received and will be reviewed with the problem, context, and desired outcome in mind.",
        )
        self.assertContains(response, "Send a copy by email")
        mock_send_mail.assert_called_once()
        self.assertEqual(mock_send_mail.call_args.kwargs["recipient_list"], ["contact@example.com"])

    def test_rebuild_css_remains_scoped_to_rebuild_layer(self):
        css = (Path(settings.BASE_DIR) / "static" / "web" / "rebuild" / "site.css").read_text()
        self.assertIn(".pi-site", css)
        self.assertIn("--pi-accent", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        for forbidden_selector in ["\nbody {", "\n.card", "\n.button", "\n.container", "\n.hero", "\n.nav"]:
            self.assertNotIn(forbidden_selector, css)

    def test_rebuild_javascript_is_isolated_and_lightweight(self):
        script_path = Path(settings.BASE_DIR) / "static" / "web" / "rebuild" / "site.js"
        script = script_path.read_text()
        self.assertLess(script_path.stat().st_size, 30 * 1024)
        self.assertIn("Escape", script)
        self.assertIn("aria-expanded", script)
        self.assertNotIn("fetch(", script)
        self.assertNotIn("gtag(", script)

    def test_unknown_rebuild_page_returns_404(self):
        response = self.client.get(reverse("rebuild_page", kwargs={"slug": "unknown"}))
        self.assertEqual(response.status_code, 404)

    def test_rebuild_assets_resolve_and_are_not_loaded_by_existing_pages(self):
        rebuild_css_url = staticfiles_storage.url("web/rebuild/site.css")
        rebuild_js_url = staticfiles_storage.url("web/rebuild/site.js")
        self.assertTrue(rebuild_css_url.endswith("web/rebuild/site.css"))
        self.assertTrue(rebuild_js_url.endswith("web/rebuild/site.js"))

        existing_routes = [
            reverse("index"),
            reverse("tools"),
            reverse("tool_detail", kwargs={"slug": "ai-auditor"}),
            reverse("seo_page", kwargs={"slug": "herramientas-adtech"}),
            reverse("insights"),
        ]

        for path in existing_routes:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, "web/rebuild/site.css", html=False)
                self.assertNotContains(response, "web/rebuild/site.js", html=False)

    def test_rebuild_routes_are_excluded_from_sitemaps(self):
        sitemap_routes = [
            reverse("sitemap"),
            reverse("sitemap_section", kwargs={"section": "pages"}),
            reverse("sitemap_section", kwargs={"section": "tools"}),
            reverse("sitemap_section", kwargs={"section": "seo"}),
            reverse("sitemap_section", kwargs={"section": "content"}),
        ]

        for path in sitemap_routes:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, "/rebuild/", html=False)

    def test_documented_public_routes_continue_to_resolve(self):
        route_cases = [
            (reverse("index"), 200),
            (reverse("solutions"), 200),
            (reverse("products"), 200),
            (reverse("adtech"), 200),
            (reverse("labs"), 301),
            (reverse("insights"), 200),
            (reverse("systems"), 301),
            (reverse("tools"), 200),
            (reverse("work"), 200),
            (reverse("case_studies"), 301),
            (reverse("approach"), 301),
            (reverse("company"), 200),
            (reverse("about"), 301),
            (reverse("contact"), 200),
            (reverse("blog"), 301),
            (reverse("policies"), 200),
            (reverse("robots_txt"), 200),
            (reverse("sitemap"), 200),
            (reverse("health"), 200),
            (reverse("healthz"), 200),
        ]

        for path, expected_status in route_cases:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, expected_status)

    def test_all_live_tool_pages_still_resolve(self):
        for slug in [
            "ai-auditor",
            "landing-performance-snapshot",
            "adtech-debug-tool",
            "utm-builder",
            "creative-qa-checklist",
            "creative-preview-lab",
        ]:
            with self.subTest(slug=slug):
                response = self.client.get(reverse("tool_detail", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'web/css/tools.css', html=False)
                self.assertNotContains(response, "web/rebuild/site.css", html=False)
                self.assertNotContains(response, "web/rebuild/site.js", html=False)

    def test_all_seo_and_knowledge_routes_still_resolve(self):
        for slug in get_public_seo_page_slugs():
            with self.subTest(seo_slug=slug):
                response = self.client.get(reverse("seo_page", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 200)

        for slug in get_public_knowledge_slugs():
            with self.subTest(knowledge_slug=slug):
                response = self.client.get(reverse("knowledge_page", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 200)

    def test_health_returns_plain_ok(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_healthz_alias_returns_plain_ok(self):
        response = self.client.get(reverse("healthz"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_primary_pages_respond(self):
        page_names = [
            "index",
            "solutions",
            "products",
            "adtech",
            "insights",
            "tools",
            "tool_detail",
            "work",
            "company",
            "contact",
            "policies",
            "sitemap",
        ]

        for name in page_names:
            with self.subTest(name=name):
                if name == "tool_detail":
                    response = self.client.get(reverse(name, kwargs={"slug": "ai-auditor"}))
                else:
                    response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_home_uses_the_master_commercial_positioning(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, "We build software for problems worth solving.")
        self.assertContains(response, "Custom software development · AI automation · AdTech")
        self.assertContains(response, "Different problems. The same standard.")
        self.assertContains(response, "AdTech is not an add-on here.")
        self.assertContains(response, "Based in Buenos Aires. Working globally.")
        self.assertContains(response, 'href="/products/"', html=False)
        self.assertNotContains(response, "Operations Copilot")
        self.assertNotContains(response, "placeholder", status_code=200)
        self.assertEqual(response.content.decode("utf-8").count("<h1"), 1)

    def test_navigation_is_available_on_primary_pages(self):
        for name in ["solutions", "products", "adtech", "work", "insights", "company", "contact"]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertContains(response, "Solutions")
                self.assertContains(response, "AdTech")
                self.assertContains(response, "Products")
                self.assertContains(response, "Work")
                self.assertContains(response, "Insights")
                self.assertContains(response, "Company")
                self.assertContains(response, "Contact")
                self.assertNotContains(response, ">Home</a>", html=False)
                self.assertNotContains(response, ">Labs</a>", html=False)

    def test_tools_index_shows_live_tools_and_grouping(self):
        response = self.client.get(reverse("tools"))
        self.assertContains(response, "Suite técnica lista para uso real")
        self.assertContains(response, "Diagnóstico técnico")
        self.assertContains(response, "Operación y etiquetado")
        self.assertContains(response, "QA y vista previa")
        self.assertContains(response, "AI Auditor")
        self.assertContains(response, "AdTech Debug Tool")
        self.assertContains(response, "UTM Builder")
        self.assertContains(response, "Creative QA Checklist")
        self.assertContains(response, "Creative Preview Lab")
        self.assertContains(response, "Landing Performance Snapshot")
        self.assertContains(response, "Grupos tematicos")
        self.assertContains(response, "Grupo Creatividades")
        self.assertContains(response, "Grupo AdTech")
        self.assertContains(response, "Grupo SEO / Performance")
        self.assertContains(response, "Grupo Tracking")
        self.assertContains(response, reverse("seo_page", kwargs={"slug": "validar-creatividad-html"}), html=False)
        self.assertContains(response, reverse("seo_page", kwargs={"slug": "debug-gpt-ads"}), html=False)
        self.assertContains(response, 'href="/tools/#qa_preview"', html=False)
        self.assertContains(response, 'href="/tools/#diagnostics"', html=False)
        self.assertContains(response, 'href="/tools/#operations"', html=False)

    def test_live_tool_pages_render_new_editorial_content(self):
        expected_content = {
            "ai-auditor": "Qué analiza AI Auditor",
            "landing-performance-snapshot": "Qué analiza Landing Performance Snapshot",
            "adtech-debug-tool": "Qué analiza AdTech Debug Tool",
            "utm-builder": "Qué hace UTM Builder",
            "creative-qa-checklist": "Qué analiza Creative QA Checklist",
            "creative-preview-lab": "Qué analiza Creative Preview Lab",
        }

        for slug, expected_text in expected_content.items():
            with self.subTest(slug=slug):
                response = self.client.get(reverse("tool_detail", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected_text)
                self.assertContains(response, "Preguntas frecuentes")

    def test_tools_index_uses_collection_schema_and_unique_h1(self):
        response = self.client.get(reverse("tools"))

        self.assertContains(response, "<title>Tools de AdTech, creatividades, SEO tecnico y tracking | Pi Development</title>", html=False)
        self.assertContains(
            response,
            f'<link rel="canonical" href="{settings.SITE_URL}{reverse("tools")}">',
            html=False,
        )
        self.assertContains(response, '"@type": "CollectionPage"', html=False)
        self.assertContains(response, '"@type": "ItemList"', html=False)
        self.assertEqual(response.content.decode("utf-8").count("<h1"), 1)

    def test_seo_pages_include_faq_schema_canonical_and_single_h1(self):
        for slug in get_public_seo_page_slugs():
            with self.subTest(slug=slug):
                page = get_seo_page(slug)
                response = self.client.get(reverse("seo_page", kwargs={"slug": slug}))

                self.assertContains(
                    response,
                    f'<link rel="canonical" href="{settings.SITE_URL}{reverse("seo_page", kwargs={"slug": slug})}">',
                    html=False,
                )
                self.assertContains(response, '"@type": "FAQPage"', html=False)
                self.assertContains(response, page["faqs"][0]["question"])
                self.assertContains(response, page["faqs"][0]["answer"])
                self.assertEqual(response.content.decode("utf-8").count("<h1"), 1)

    def test_live_tool_pages_include_faq_schema_canonical_and_single_h1(self):
        for slug in [
            "ai-auditor",
            "adtech-debug-tool",
            "landing-performance-snapshot",
            "utm-builder",
            "creative-qa-checklist",
            "creative-preview-lab",
        ]:
            with self.subTest(slug=slug):
                tool = get_tool(slug)
                response = self.client.get(reverse("tool_detail", kwargs={"slug": slug}))

                self.assertContains(
                    response,
                    f'<link rel="canonical" href="{settings.SITE_URL}{reverse("tool_detail", kwargs={"slug": slug})}">',
                    html=False,
                )
                self.assertContains(response, '"@type": "FAQPage"', html=False)
                self.assertContains(response, tool["editorial"]["faqs"][0]["question"])
                self.assertContains(response, tool["editorial"]["faqs"][0]["answer"])
                self.assertEqual(response.content.decode("utf-8").count("<h1"), 1)

    def test_social_meta_tags_render_on_key_public_pages(self):
        expected_og_image = f'{settings.SITE_URL}/static/web/img/pi.png'
        knowledge_slug = "como-validar-una-creatividad-html-antes-de-publicarla"
        knowledge_page = get_knowledge_page(knowledge_slug)
        hub_page = get_seo_page("herramientas-adtech")
        ai_tool = get_tool("ai-auditor")

        cases = [
            (
                reverse("index"),
                "Custom Software &amp; AdTech Development | Pi Development",
                "Pi Development builds custom software, MVPs, AI automation and AdTech products for companies and digital publishers. Based in Buenos Aires, working globally.",
            ),
            (
                reverse("solutions"),
                "Custom Software Development Services | Pi Development",
                "Custom software development, MVP development, internal tools, integrations and AI automation from Pi Development in Buenos Aires, working globally.",
            ),
            (
                reverse("tools"),
                "Tools de AdTech, creatividades, SEO tecnico y tracking | Pi Development",
                "La suite de Pi Development reÃºne utilidades reales para detectar problemas, validar implementaciones y acelerar decisiones tÃ©cnicas sin ruido visual ni promesas vacÃ­as.",
            ),
            (
                reverse("seo_page", kwargs={"slug": "herramientas-adtech"}),
                hub_page["title"],
                hub_page["meta_description"],
            ),
            (
                reverse("insights"),
                "Software &amp; AdTech Insights | Pi Development",
                "Technical insights from Pi Development on AdTech, Google Publisher Tag, creative QA, publisher technology, tracking, technical SEO and web performance.",
            ),
            (
                reverse("knowledge_page", kwargs={"slug": knowledge_slug}),
                knowledge_page["title"],
                knowledge_page["meta_description"],
            ),
            (
                reverse("tool_detail", kwargs={"slug": "ai-auditor"}),
                ai_tool["seo_title"],
                ai_tool["meta_description"],
            ),
        ]

        for path, expected_title, expected_description in cases:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f'<meta property="og:title" content="{expected_title}">', html=False)
                self.assertContains(response, f'<meta name="twitter:title" content="{expected_title}">', html=False)
                self.assertContains(response, '<meta property="og:description" content="', html=False)
                self.assertContains(response, '<meta name="twitter:description" content="', html=False)
                self.assertContains(response, '<meta name="twitter:card" content="summary_large_image">', html=False)
                self.assertContains(response, f'<meta property="og:image" content="{expected_og_image}">', html=False)
                self.assertContains(response, f'<meta name="twitter:image" content="{expected_og_image}">', html=False)

        article_response = self.client.get(reverse("knowledge_page", kwargs={"slug": knowledge_slug}))
        self.assertContains(article_response, '<meta property="og:type" content="article">', html=False)

    def test_seo_pages_render_titles_tools_and_interlinking(self):
        for slug in get_public_seo_page_slugs():
            with self.subTest(slug=slug):
                page = get_seo_page(slug)
                cluster = get_topic_cluster_context_for_seo_page(slug)
                response = self.client.get(reverse("seo_page", kwargs={"slug": slug}))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, page["title"])
                self.assertContains(response, page["h1"])
                self.assertContains(response, page["meta_description"])
                self.assertContains(response, reverse("tool_detail", kwargs={"slug": page["primary_tool_slug"]}), html=False)
                self.assertContains(response, "Preguntas frecuentes")
                self.assertContains(response, "Grupo tematico")
                self.assertContains(response, f'/tools/#{cluster["catalog_anchor"]}', html=False)

                if page.get("hub_sections"):
                    self.assertContains(response, "Herramientas agrupadas por categoria")
                    self.assertContains(response, "Casos de uso reales")
                else:
                    self.assertContains(response, "Herramientas relacionadas")
                    self.assertContains(response, "Guias relacionadas")

                for related_slug in page["related_page_slugs"][:2]:
                    self.assertContains(response, reverse("seo_page", kwargs={"slug": related_slug}), html=False)

    def test_herramientas_adtech_page_behaves_as_suite_hub(self):
        response = self.client.get(reverse("seo_page", kwargs={"slug": "herramientas-adtech"}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Herramientas agrupadas por categoria")
        self.assertContains(response, "Casos de uso reales")
        self.assertContains(response, "Diagnostico")
        self.assertContains(response, "QA y preview")
        self.assertContains(response, "Tracking y operaciones")
        self.assertContains(response, "Rendimiento y validacion tecnica")
        self.assertContains(response, "Que herramientas incluye esta pagina hub de Pi Development?")

        for tool_slug in [
            "adtech-debug-tool",
            "creative-preview-lab",
            "creative-qa-checklist",
            "utm-builder",
            "ai-auditor",
            "landing-performance-snapshot",
        ]:
            with self.subTest(tool_slug=tool_slug):
                self.assertContains(response, reverse("tool_detail", kwargs={"slug": tool_slug}), html=False)

        for seo_slug in [
            "debug-anuncios-web",
            "debug-gpt-ads",
            "validar-creatividad-html",
            "preview-anuncios-html",
            "errores-creatividades-display",
            "como-validar-tags-publicitarios",
            "como-crear-utms",
            "auditoria-tecnica-web",
            "analizar-seo-pagina",
        ]:
            with self.subTest(seo_slug=seo_slug):
                self.assertContains(response, reverse("seo_page", kwargs={"slug": seo_slug}), html=False)

    def test_tool_pages_link_back_to_related_guides_and_catalog_groups(self):
        expected_links = {
            "creative-preview-lab": ("preview-anuncios-html", "qa_preview"),
            "creative-qa-checklist": ("validar-creatividad-html", "qa_preview"),
            "adtech-debug-tool": ("debug-anuncios-web", "diagnostics"),
            "ai-auditor": ("auditoria-tecnica-web", "diagnostics"),
            "landing-performance-snapshot": ("analizar-seo-pagina", "diagnostics"),
            "utm-builder": ("como-crear-utms", "operations"),
        }

        for tool_slug, (seo_slug, anchor) in expected_links.items():
            with self.subTest(tool_slug=tool_slug):
                response = self.client.get(reverse("tool_detail", kwargs={"slug": tool_slug}))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Guias relacionadas")
                self.assertContains(response, "Grupo tematico")
                self.assertContains(response, reverse("seo_page", kwargs={"slug": seo_slug}), html=False)
                self.assertContains(response, f'/tools/#{anchor}', html=False)

    def test_live_tool_pages_expose_example_cta(self):
        for slug in [
            "ai-auditor",
            "adtech-debug-tool",
            "landing-performance-snapshot",
            "utm-builder",
            "creative-qa-checklist",
            "creative-preview-lab",
        ]:
            with self.subTest(slug=slug):
                response = self.client.get(reverse("tool_detail", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Probar con ejemplo")
                self.assertContains(response, "Prueba rapida")

    def test_simple_tools_expose_clear_placeholders_and_input_guidance(self):
        ai_response = self.client.get(reverse("tool_detail", kwargs={"slug": "ai-auditor"}))
        self.assertContains(ai_response, 'placeholder="https://www.tusitio.com/landing"', html=False)
        self.assertContains(ai_response, "Usa una URL accesible sin login", html=False)

        landing_response = self.client.get(reverse("tool_detail", kwargs={"slug": "landing-performance-snapshot"}))
        self.assertContains(landing_response, 'placeholder="https://www.tusitio.com/campana"', html=False)
        self.assertContains(landing_response, "Ideal para una landing o pagina de campana", html=False)

        utm_response = self.client.get(reverse("tool_detail", kwargs={"slug": "utm-builder"}))
        self.assertContains(utm_response, 'placeholder="google"', html=False)
        self.assertContains(utm_response, 'placeholder="cpc"', html=False)
        self.assertContains(utm_response, 'placeholder="lanzamiento_q2"', html=False)
        self.assertContains(utm_response, "source, medium y campaign", html=False)

    @patch("pi_development.web.views.run_landing_performance_snapshot")
    @patch("pi_development.web.views.run_adtech_debug")
    @patch("pi_development.web.views.run_ai_auditor")
    def test_url_based_example_button_runs_with_centralized_payloads(
        self,
        mock_run_ai_auditor,
        mock_run_adtech_debug,
        mock_run_landing_snapshot,
    ):
        mock_run_ai_auditor.return_value = {
            "target_url": "https://pidevelopment.web.app/",
            "insight": {
                "score": 80,
                "status_label": "Saludable",
                "tone": "good",
                "impact": "Medio",
                "risk": "Bajo",
                "priority": "Monitorear",
                "affected_areas": ["SEO"],
                "summary": "Base tecnica legible.",
                "issue_count": 0,
                "highlights": ["Title y meta visibles."],
            },
            "diagnosis": {
                "overview": {"label": "Base saludable", "tone": "good", "summary": "Ejemplo renderizado."},
                "technical_observations": ["HTTP 200."],
                "performance": {"label": "Correcto", "tone": "good", "items": [], "note": "Ok."},
                "seo": {"label": "Correcto", "tone": "good", "items": [], "note": "Ok."},
                "opportunities": ["Sin prioridad critica."],
                "recommendation": "Mantener monitoreo.",
            },
            "ai_summary": {"available": False, "status": "unconfigured", "text": "", "message": "No configurado."},
            "sources": [{"label": "Snapshot HTTP", "status": "ok", "detail": "HTTP 200."}],
            "exports": [],
        }
        mock_run_adtech_debug.return_value = {
            "target_url": "https://edition.cnn.com/",
            "insight": {
                "score": 70,
                "status_label": "Visible",
                "tone": "warn",
                "impact": "Medio",
                "risk": "Medio",
                "priority": "Revisar pronto",
                "affected_areas": ["Monetizacion"],
                "summary": "Senales visibles.",
                "issue_count": 1,
                "highlights": ["GPT visible."],
            },
            "analysis": {
                "slot_count_estimate": 1,
                "matched_script_sources": [],
                "matched_iframe_sources": [],
                "vendor_hits": [],
            },
            "diagnosis": {
                "overview": {"label": "Stack visible", "tone": "good", "summary": "Ejemplo renderizado."},
                "monetization_signals": [],
                "technical_findings": ["Scripts visibles."],
                "opportunities": ["Revisar slots."],
                "recommendation": "Abrir DevTools.",
                "limitations": ["Lectura backend."],
            },
            "sources": [{"label": "Snapshot HTTP", "status": "ok", "detail": "HTTP 200."}],
            "exports": [],
        }
        mock_run_landing_snapshot.return_value = {
            "target_url": "https://pidevelopment.web.app/tools/",
            "insight": {
                "score": 76,
                "status_label": "Correcto",
                "tone": "good",
                "impact": "Medio",
                "risk": "Bajo",
                "priority": "Monitorear",
                "affected_areas": ["SEO"],
                "summary": "Metadata visible.",
                "issue_count": 0,
                "highlights": ["Snapshot listo."],
            },
            "diagnosis": {
                "overview": {"label": "Snapshot limpio", "tone": "good", "summary": "Ejemplo renderizado."},
                "status_items": [],
                "structure_items": [],
                "quick_signals": [],
                "summary": "Base correcta.",
                "recommendation": "Escalar solo si hace falta.",
            },
            "sources": [{"label": "Snapshot HTTP", "status": "ok", "detail": "HTTP 200."}],
            "exports": [],
        }

        for slug, mocked_service in [
            ("ai-auditor", mock_run_ai_auditor),
            ("adtech-debug-tool", mock_run_adtech_debug),
            ("landing-performance-snapshot", mock_run_landing_snapshot),
        ]:
            with self.subTest(slug=slug):
                response = self.client.post(reverse("tool_detail", kwargs={"slug": slug}), data={"_use_example": "1"})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Ejemplo cargado")
                mocked_service.assert_called_with(get_tool_example(slug)["form_data"]["url"])

    def test_local_example_button_prefills_and_runs_tools(self):
        response = self.client.post(reverse("tool_detail", kwargs={"slug": "utm-builder"}), data={"_use_example": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ejemplo cargado")
        self.assertContains(response, "utm_source=newsletter")
        self.assertContains(response, "utm_medium=email")
        self.assertContains(response, "utm_campaign=seo_examples")

        response = self.client.post(reverse("tool_detail", kwargs={"slug": "creative-qa-checklist"}), data={"_use_example": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ejemplo cargado")
        self.assertContains(response, "Lanzamiento display 300x250")
        self.assertContains(response, "Checklist")

        response = self.client.post(reverse("tool_detail", kwargs={"slug": "creative-preview-lab"}), data={"_use_example": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ejemplo cargado")
        self.assertContains(response, "Demo CTA 300x250")
        self.assertContains(response, "Vista previa de creatividad")

    def test_unknown_seo_page_returns_404(self):
        response = self.client.get(reverse("seo_page", kwargs={"slug": "pagina-inexistente"}))
        self.assertEqual(response.status_code, 404)

    def test_sitemap_index_exposes_content_sections(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{settings.SITE_URL}/sitemap-pages.xml", html=False)
        self.assertContains(response, f"{settings.SITE_URL}/sitemap-tools.xml", html=False)
        self.assertContains(response, f"{settings.SITE_URL}/sitemap-seo.xml", html=False)
        self.assertContains(response, f"{settings.SITE_URL}/sitemap-content.xml", html=False)
        self.assertContains(response, "/sitemap-pages.xml", html=False)
        self.assertContains(response, "/sitemap-tools.xml", html=False)
        self.assertContains(response, "/sitemap-seo.xml", html=False)
        self.assertContains(response, "/sitemap-content.xml", html=False)

    def test_sitemap_sections_include_public_urls_and_exclude_low_value_pages(self):
        pages_response = self.client.get(reverse("sitemap_section", kwargs={"section": "pages"}))
        self.assertEqual(pages_response.status_code, 200)
        self.assertContains(pages_response, reverse("index"), html=False)
        self.assertContains(pages_response, reverse("solutions"), html=False)
        self.assertContains(pages_response, reverse("products"), html=False)
        self.assertContains(pages_response, reverse("adtech"), html=False)
        self.assertContains(pages_response, reverse("insights"), html=False)
        self.assertContains(pages_response, reverse("tools"), html=False)
        self.assertContains(pages_response, reverse("work"), html=False)
        self.assertContains(pages_response, reverse("company"), html=False)
        self.assertContains(pages_response, reverse("contact"), html=False)
        self.assertNotContains(pages_response, reverse("labs"), html=False)
        self.assertNotContains(pages_response, reverse("systems"), html=False)
        self.assertNotContains(pages_response, reverse("about"), html=False)
        self.assertNotContains(pages_response, reverse("blog"), html=False)
        self.assertNotContains(pages_response, reverse("policies"), html=False)
        self.assertNotContains(pages_response, reverse("health"), html=False)

        tools_response = self.client.get(reverse("sitemap_section", kwargs={"section": "tools"}))
        self.assertEqual(tools_response.status_code, 200)
        self.assertContains(tools_response, reverse("tool_detail", kwargs={"slug": "ai-auditor"}), html=False)
        self.assertContains(tools_response, reverse("tool_detail", kwargs={"slug": "creative-preview-lab"}), html=False)

        seo_response = self.client.get(reverse("sitemap_section", kwargs={"section": "seo"}))
        self.assertEqual(seo_response.status_code, 200)
        for slug in get_public_seo_page_slugs():
            with self.subTest(slug=slug):
                self.assertContains(seo_response, f"/{slug}/", html=False)

        content_response = self.client.get(reverse("sitemap_section", kwargs={"section": "content"}))
        self.assertEqual(content_response.status_code, 200)
        for slug in get_public_knowledge_slugs():
            with self.subTest(slug=slug):
                self.assertContains(content_response, reverse("knowledge_page", kwargs={"slug": slug}), html=False)

    def test_robots_txt_allows_public_content_and_references_sitemap(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User-agent: *")
        self.assertContains(response, "Allow: /")
        self.assertContains(response, "Disallow: /rebuild/")
        self.assertContains(response, f"Sitemap: {settings.SITE_URL}{reverse('sitemap')}")
        self.assertEqual(
            response.content.decode("utf-8"),
            f"User-agent: *\nAllow: /\nDisallow: /rebuild/\nSitemap: {settings.SITE_URL}{reverse('sitemap')}",
        )

    @override_settings(GOOGLE_ANALYTICS_ID="G-TEST123456", GOOGLE_SITE_VERIFICATION="verify-token-123")
    def test_base_template_renders_ga4_and_search_console_when_configured(self):
        response = self.client.get(reverse("index"))
        self.assertContains(
            response,
            '<script async src="https://www.googletagmanager.com/gtag/js?id=G-TEST123456"></script>',
            html=False,
        )
        self.assertContains(response, "gtag('config', 'G-TEST123456');", html=False)
        self.assertContains(
            response,
            '<meta name="google-site-verification" content="verify-token-123">',
            html=False,
        )
        self.assertEqual(response.content.decode("utf-8").count("gtag/js?id=G-TEST123456"), 1)

    @override_settings(GOOGLE_ANALYTICS_ID="", GOOGLE_SITE_VERIFICATION="")
    def test_base_template_omits_google_tags_when_not_configured(self):
        response = self.client.get(reverse("index"))
        self.assertNotContains(response, "googletagmanager.com/gtag/js", html=False)
        self.assertNotContains(response, "google-site-verification", html=False)

    def test_insights_listing_is_indexable_and_lists_knowledge_pages(self):
        response = self.client.get(reverse("insights"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<link rel="canonical" href="https://pidevelopment.web.app/insights/">', html=False)
        self.assertNotContains(response, 'noindex, follow', html=False)
        self.assertContains(response, "Technical writing connected to real products and services.")
        for slug in get_public_knowledge_slugs():
            with self.subTest(slug=slug):
                page = get_knowledge_page(slug)
                self.assertContains(response, reverse("knowledge_page", kwargs={"slug": slug}), html=False)
                self.assertContains(response, page["h1"])

    def test_insights_listing_surfaces_the_three_strategic_articles(self):
        response = self.client.get(reverse("insights"))

        expected_articles = {
            "como-validar-una-creatividad-html-antes-de-publicarla": "Creative Preview Lab",
            "errores-comunes-en-implementaciones-con-google-publisher-tag": "AdTech Debug Tool",
            "como-crear-urls-con-parametros-utm-correctamente": "UTM Builder",
        }

        for slug, tool_name in expected_articles.items():
            with self.subTest(slug=slug):
                page = get_knowledge_page(slug)
                self.assertContains(response, reverse("knowledge_page", kwargs={"slug": slug}), html=False)
                self.assertContains(response, page["h1"])
                self.assertTrue(tool_name)

    def test_knowledge_pages_render_with_faq_schema_and_related_links(self):
        for slug in get_public_knowledge_slugs():
            with self.subTest(slug=slug):
                page = get_knowledge_page(slug)
                response = self.client.get(reverse("knowledge_page", kwargs={"slug": slug}))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, page["title"])
                self.assertContains(response, page["h1"])
                self.assertContains(response, page["meta_description"])
                self.assertContains(
                    response,
                    f'<link rel="canonical" href="{settings.SITE_URL}{reverse("knowledge_page", kwargs={"slug": slug})}">',
                    html=False,
                )
                self.assertContains(response, '"@type": "FAQPage"', html=False)
                self.assertContains(response, "Herramientas relacionadas")
                self.assertContains(response, "Guias tecnicas relacionadas")
                self.assertContains(response, "Lecturas relacionadas")
                self.assertContains(response, reverse("insights"), html=False)
                self.assertContains(response, '"@type": "Article"', html=False)

                for tool_slug in page["related_tool_slugs"][:1]:
                    self.assertContains(response, reverse("tool_detail", kwargs={"slug": tool_slug}), html=False)

                for seo_slug in page["related_seo_page_slugs"][:1]:
                    self.assertContains(response, reverse("seo_page", kwargs={"slug": seo_slug}), html=False)

                for related_slug in page["related_knowledge_slugs"][:1]:
                    self.assertContains(response, reverse("knowledge_page", kwargs={"slug": related_slug}), html=False)

                self.assertContains(response, page["faqs"][0]["question"])
                self.assertContains(response, page["faqs"][0]["answer"])

    def test_unknown_knowledge_page_returns_404(self):
        response = self.client.get(reverse("knowledge_page", kwargs={"slug": "articulo-inexistente"}))
        self.assertEqual(response.status_code, 404)

    def test_content_navigation_links_are_visible(self):
        response = self.client.get(reverse("insights"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/insights/"', html=False)
        self.assertContains(response, reverse("seo_page", kwargs={"slug": "herramientas-adtech"}), html=False)

        article_response = self.client.get(reverse("knowledge_page", kwargs={"slug": get_public_knowledge_slugs()[0]}))
        self.assertContains(article_response, 'href="/insights/"', html=False)
        self.assertContains(
            article_response,
            reverse("seo_page", kwargs={"slug": "herramientas-adtech"}),
            html=False,
        )

    def test_footer_exposes_discovery_hubs_for_seo_clusters(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Technical guides")
        for page in get_discovery_seo_hub_pages():
            with self.subTest(slug=page["slug"]):
                self.assertContains(response, reverse("seo_page", kwargs={"slug": page["slug"]}), html=False)

    def test_url_based_tools_reject_invalid_url(self):
        for slug, field_name in [
            ("ai-auditor", "url"),
            ("adtech-debug-tool", "url"),
            ("landing-performance-snapshot", "url"),
        ]:
            with self.subTest(slug=slug):
                response = self.client.post(
                    reverse("tool_detail", kwargs={"slug": slug}),
                    data={field_name: "nota url"},
                )
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Ingresa una URL válida con dominio público.")

    def test_creative_preview_lab_rejects_invalid_click_url(self):
        response = self.client.post(
            reverse("tool_detail", kwargs={"slug": "creative-preview-lab"}),
            data={
                "creative_name": "Preview test",
                "creative_type": "display",
                "width": 300,
                "height": 250,
                "input_mode": "html",
                "code": "<div>Creative</div>",
                "click_url": "nota url",
                "notes": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ingresa una URL válida con dominio público.")

    def test_utm_builder_rejects_invalid_destination_url(self):
        response = self.client.post(
            reverse("tool_detail", kwargs={"slug": "utm-builder"}),
            data={
                "destination_url": "nota url",
                "utm_source": "newsletter",
                "utm_medium": "email",
                "utm_campaign": "launch",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ingresa una URL válida con dominio público.")

    def test_creative_qa_rejects_invalid_dimensions(self):
        response = self.client.post(
            reverse("tool_detail", kwargs={"slug": "creative-qa-checklist"}),
            data={
                "creative_name": "Promo hero",
                "format_type": "html5",
                "dimensions": "wide",
                "destination_url": "https://example.com",
                "click_tag_present": "yes",
                "tracking_urls_included": "yes",
                "weight_kb": 120,
                "device_target": "both",
                "sound_behavior": "none",
                "autoplay_behavior": "none",
                "serving_context": "safeframe",
                "extra_notes": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usa un formato de dimensiones válido, por ejemplo 300x250.")

    @patch("pi_development.web.views.run_ai_auditor")
    def test_ai_auditor_renders_structured_result(self, mock_run_ai_auditor):
        mock_run_ai_auditor.return_value = {
            "target_url": "https://example.com",
            "insight": {
                "score": 72,
                "status_label": "Aceptable",
                "tone": "warn",
                "impact": "Medio",
                "risk": "Medio",
                "priority": "Revisar pronto",
                "affected_areas": ["Rendimiento", "SEO"],
                "summary": "Rendimiento y SEO siguen utilizables, pero la base necesita una ronda de ajustes.",
                "issue_count": 2,
                "highlights": [
                    "Falta metadata central y eso reduce la claridad para buscadores.",
                    "La base de rendimiento sigue usable, pero no es sólida.",
                ],
            },
            "diagnosis": {
                "overview": {
                    "label": "Base saludable",
                    "tone": "good",
                    "summary": "La URL responde y la base técnica es legible.",
                },
                "technical_observations": [
                    "HTTP 200 y respuesta inicial en 400 ms.",
                ],
                "performance": {
                    "label": "Rendimiento saludable",
                    "tone": "good",
                    "items": [{"label": "PageSpeed mobile", "value": "88/100"}],
                    "note": "Sin observaciones críticas.",
                },
                "seo": {
                    "label": "SEO básico consistente",
                    "tone": "good",
                    "items": [{"label": "Title", "value": "Detectado"}],
                    "note": "Lectura SEO básica disponible.",
                },
                "opportunities": ["Revisar caché de recursos estáticos."],
                "recommendation": "Mantener monitoreo y profundizar mejoras en rendimiento.",
            },
            "ai_summary": {
                "available": False,
                "status": "unconfigured",
                "text": "",
                "message": "OpenAI no está configurado para enriquecer este análisis todavía.",
            },
            "sources": [
                {"label": "Snapshot HTTP", "status": "ok", "detail": "HTTP 200 en 400 ms."},
                {"label": "PageSpeed Insights", "status": "ok", "detail": "PageSpeed devolvió datos."},
                {"label": "Capa de OpenAI", "status": "limited", "detail": "No configurado."},
            ],
            "exports": [
                {"key": "summary", "label": "Copiar resumen", "success_message": "Resumen copiado.", "text": "summary"},
                {"key": "findings", "label": "Copiar hallazgos", "success_message": "Hallazgos copiados.", "text": "findings"},
                {"key": "markdown", "label": "Copiar resumen en Markdown", "success_message": "Markdown copiado.", "text": "markdown"},
            ],
        }

        response = self.client.post(
            reverse("tool_detail", kwargs={"slug": "ai-auditor"}),
            data={"url": "https://example.com"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Base saludable")
        self.assertContains(response, "Observaciones tecnicas")
        self.assertContains(response, "Rendimiento saludable")
        self.assertContains(response, "SEO básico consistente")
        self.assertContains(response, "Copiar resumen")
        self.assertContains(response, "Copiar hallazgos")
        self.assertContains(response, "Áreas afectadas")
        self.assertContains(response, "Revisar pronto")
        self.assertContains(response, "Landing Performance Snapshot")

    @patch("pi_development.web.views.run_landing_performance_snapshot")
    def test_landing_snapshot_renders_structured_result(self, mock_run_landing_snapshot):
        mock_run_landing_snapshot.return_value = {
            "target_url": "https://example.com/landing",
            "insight": {
                "score": 58,
                "status_label": "Riesgoso",
                "tone": "warn",
                "impact": "Alto",
                "risk": "Alto",
                "priority": "Corregir ahora",
                "affected_areas": ["SEO", "Rendimiento"],
                "summary": "Faltan metadatos centrales y la respuesta base es lenta para esta primera lectura.",
                "issue_count": 3,
                "highlights": [
                    "Falta meta description en la respuesta inicial.",
                    "Falta canonical en la respuesta inicial.",
                ],
            },
            "diagnosis": {
                "overview": {
                    "label": "Base legible con ajustes puntuales",
                    "tone": "warn",
                    "summary": "La landing responde y deja algunos puntos rápidos para revisar.",
                },
                "status_items": [
                    {"label": "Estado HTTP", "value": "200"},
                    {"label": "Tiempo de respuesta", "value": "840 ms"},
                    {"label": "URL final", "value": "Sin redirect visible"},
                ],
                "structure_items": [
                    {"label": "Title", "value": "Example Landing"},
                    {"label": "Meta description", "value": "No detectada"},
                    {"label": "Canonical", "value": "No detectada"},
                    {"label": "Robots", "value": "index,follow"},
                    {"label": "Cantidad de H1", "value": "2"},
                ],
                "quick_signals": [
                    {"label": "Meta description", "status": "warn", "detail": "Falta meta description en la respuesta inicial."},
                    {"label": "Jerarquía H1", "status": "warn", "detail": "Se detectaron 2 H1; conviene revisar la jerarquía."},
                ],
                "summary": "Snapshot rápido: faltan metadatos base y la jerarquía H1 necesita ajuste.",
                "recommendation": "Prioridad sugerida: resolver falta meta description en la respuesta inicial.",
            },
            "sources": [
                {"label": "Snapshot HTTP", "status": "ok", "detail": "HTTP 200 en 840 ms."},
                {"label": "Reglas rápidas", "status": "ok", "detail": "Chequeos simples sobre metadata y tiempo de respuesta."},
            ],
            "exports": [
                {"key": "summary", "label": "Copiar resumen", "success_message": "Resumen copiado.", "text": "summary"},
                {"key": "findings", "label": "Copiar hallazgos", "success_message": "Hallazgos copiados.", "text": "findings"},
                {"key": "markdown", "label": "Copiar resumen en Markdown", "success_message": "Markdown copiado.", "text": "markdown"},
            ],
        }

        response = self.client.post(
            reverse("tool_detail", kwargs={"slug": "landing-performance-snapshot"}),
            data={"url": "https://example.com/landing"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Base legible con ajustes puntuales")
        self.assertContains(response, "Estado de respuesta")
        self.assertContains(response, "Estructura basica")
        self.assertContains(response, "Senales rapidas")
        self.assertContains(response, "Que revisar primero")
        self.assertContains(response, "Copiar resumen en Markdown")
        self.assertContains(response, "Áreas afectadas")
        self.assertContains(response, "Corregir ahora")

    def test_creative_preview_lab_renders_preview_and_findings(self):
        response = self.client.post(
            reverse("tool_detail", kwargs={"slug": "creative-preview-lab"}),
            data={
                "creative_name": "Tag preview",
                "creative_type": "third_party",
                "width": 300,
                "height": 250,
                "input_mode": "third_party",
                "code": '<script src="https://cdn.example.com/tag.js"></script><iframe src="https://ads.example.com/frame"></iframe>%%CLICK_URL%%',
                "click_url": "",
                "notes": "Initial QA pass",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Parcial")
        self.assertContains(response, "Elementos detectados")
        self.assertContains(response, "Scripts")
        self.assertContains(response, "Iframes")
        self.assertContains(response, "Macros / placeholders")
        self.assertContains(response, "Áreas afectadas")
        self.assertContains(response, "Factores prioritarios")
        self.assertContains(response, "La ejecución de tags de terceros puede depender de entornos externos")
        self.assertContains(response, "Vista previa parcial")
        self.assertContains(response, "Copiar resumen")
        self.assertContains(response, "Creative QA Checklist")

    @patch("pi_development.web.views.run_adtech_debug")
    def test_adtech_debug_renders_structured_result(self, mock_run_adtech_debug):
        mock_run_adtech_debug.return_value = {
            "target_url": "https://example.com",
            "insight": {
                "score": 61,
                "status_label": "Riesgoso",
                "tone": "warn",
                "impact": "Alto",
                "risk": "Alto",
                "priority": "Revisar pronto",
                "affected_areas": ["Monetización", "Entrega"],
                "summary": "Las señales visibles necesitan una estructura de slots más clara antes de confiar en la implementación.",
                "issue_count": 2,
                "highlights": [
                    "Hay señales AdTech fuertes sin una estructura clara de slots en el HTML inicial.",
                    "La carga del lado del cliente puede ocultar parte del stack al análisis backend.",
                ],
            },
            "analysis": {
                "slot_count_estimate": 2,
                "matched_script_sources": [
                    "https://securepubads.g.doubleclick.net/tag/js/gpt.js",
                ],
                "matched_iframe_sources": [
                    "https://googleads.g.doubleclick.net/pagead/ads",
                ],
                "vendor_hits": ["amazon-adsystem"],
            },
            "diagnosis": {
                "overview": {
                    "label": "Stack visible en respuesta inicial",
                    "tone": "good",
                    "summary": "La URL respondió y expone señales AdTech legibles desde backend.",
                },
                "monetization_signals": [
                    {
                        "label": "Google Publisher Tag / googletag",
                        "status": "detected",
                        "detail": "Se detectaron señales compatibles con GPT.",
                        "matched_patterns": ["googletag", "gpt.js"],
                    },
                    {
                        "label": "AdSense",
                        "status": "not-detected",
                        "detail": "No aparecieron señales visibles de AdSense.",
                        "matched_patterns": [],
                    },
                ],
                "technical_findings": [
                    "Scripts publicitarios detectados: https://securepubads.g.doubleclick.net/tag/js/gpt.js",
                ],
                "opportunities": [
                    "Hay señales de GPT sin slots claros en el HTML inicial.",
                ],
                "recommendation": "Validar en navegador el stack que el backend alcanza a insinuar.",
                "limitations": [
                    "La detección ocurre sobre HTML descargado desde backend y no ejecuta JavaScript.",
                ],
            },
            "sources": [
                {"label": "Snapshot HTTP", "status": "ok", "detail": "HTTP 200 en 320 ms."},
                {"label": "Escaneo por patrones", "status": "ok", "detail": "Se detectaron 2 señales positivas."},
                {"label": "Alcance del render", "status": "limited", "detail": "La detección es parcial."},
            ],
            "exports": [
                {"key": "summary", "label": "Copiar resumen", "success_message": "Resumen copiado.", "text": "summary"},
                {"key": "findings", "label": "Copiar hallazgos", "success_message": "Hallazgos copiados.", "text": "findings"},
                {"key": "markdown", "label": "Copiar resumen en Markdown", "success_message": "Markdown copiado.", "text": "markdown"},
            ],
        }

        response = self.client.post(
            reverse("tool_detail", kwargs={"slug": "adtech-debug-tool"}),
            data={"url": "https://example.com"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stack visible en respuesta inicial")
        self.assertContains(response, "Señales detectadas de monetización")
        self.assertContains(response, "Hallazgos técnicos")
        self.assertContains(response, "Siguiente paso recomendado")
        self.assertContains(response, "Copiar hallazgos")
        self.assertContains(response, "Áreas afectadas")
        self.assertContains(response, "Revisar pronto")
        self.assertContains(response, "Creative Preview Lab")

    def test_utm_builder_builds_url_and_preserves_query_params(self):
        response = self.client.post(
            reverse("tool_detail", kwargs={"slug": "utm-builder"}),
            data={
                "destination_url": "https://example.com/path?ref=internal",
                "utm_source": "Newsletter",
                "utm_medium": "Email",
                "utm_campaign": "Q2 Launch",
                "utm_term": "",
                "utm_content": "Hero Variant A",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "URL lista para usar")
        self.assertContains(response, "ref=internal")
        self.assertContains(response, "utm_source=newsletter")
        self.assertContains(response, "utm_medium=email")
        self.assertContains(response, "utm_campaign=q2-launch")
        self.assertContains(response, "utm_content=hero-variant-a")
        self.assertContains(response, "Abrir URL")

    def test_creative_qa_returns_blocked_for_autoplay_with_sound(self):
        response = self.client.post(
            reverse("tool_detail", kwargs={"slug": "creative-qa-checklist"}),
            data={
                "creative_name": "Video takeover",
                "format_type": "video",
                "dimensions": "1920x1080",
                "destination_url": "https://example.com/promo",
                "click_tag_present": "yes",
                "tracking_urls_included": "no",
                "weight_kb": 6500,
                "device_target": "both",
                "sound_behavior": "load",
                "autoplay_behavior": "sound_on",
                "serving_context": "unknown",
                "extra_notes": "Test creative",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bloqueada")
        self.assertContains(response, "reproducción automática con sonido")
        self.assertContains(response, "No se declararon URLs de tracking")
        self.assertContains(response, "Peso de 6500 KB")
        self.assertContains(response, "Copiar resumen en Markdown")
        self.assertContains(response, "Factores prioritarios")
        self.assertContains(response, "Corregir ahora")
        self.assertContains(response, "Creative Preview Lab")

    def test_legacy_routes_redirect(self):
        for name in ["services", "portfolio", "process_page", "resources_page"]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 301)

    def test_legacy_service_pages_redirect(self):
        for slug in ["web-development", "ux-ui", "marketing", "seo"]:
            with self.subTest(slug=slug):
                response = self.client.get(reverse("service_page", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 301)

    def test_unknown_service_returns_404(self):
        response = self.client.get(reverse("service_page", kwargs={"slug": "unknown"}))
        self.assertEqual(response.status_code, 404)

    def test_favicon_redirects(self):
        response = self.client.get("/favicon.ico")
        self.assertEqual(response.status_code, 301)

    def test_home_has_no_bom_artifacts(self):
        response = self.client.get(reverse("index"))
        self.assertNotIn(b"\xef\xbb\xbf", response.content)
        self.assertNotIn(b"&#xFEFF;", response.content)
        self.assertNotIn(b"&#65279;", response.content)


@override_settings(ENABLE_REMOTE_URL_TOOLS=False)
class RemoteToolContainmentTests(TestCase):
    remote_tool_slugs = (
        "ai-auditor",
        "landing-performance-snapshot",
        "adtech-debug-tool",
    )

    @patch("pi_development.web.views.run_landing_performance_snapshot")
    @patch("pi_development.web.views.run_adtech_debug")
    @patch("pi_development.web.views.run_ai_auditor")
    def test_disabled_remote_routes_and_examples_never_call_services(
        self,
        mock_run_ai_auditor,
        mock_run_adtech_debug,
        mock_run_landing_snapshot,
    ):
        services = {
            "ai-auditor": mock_run_ai_auditor,
            "adtech-debug-tool": mock_run_adtech_debug,
            "landing-performance-snapshot": mock_run_landing_snapshot,
        }

        for slug, service in services.items():
            path = reverse("tool_detail", kwargs={"slug": slug})
            for method, payload in (
                ("get", None),
                ("post", {"url": "https://example.com"}),
                ("post", {"_use_example": "1"}),
            ):
                with self.subTest(slug=slug, method=method, payload=payload):
                    response = getattr(self.client, method)(path, data=payload)
                    self.assertEqual(response.status_code, 503)
                    self.assertContains(response, "temporalmente deshabilitado", status_code=503)
                    self.assertContains(response, "no analiza URLs ni genera puntajes", status_code=503)
                    self.assertEqual(response["Cache-Control"], "no-store")
            service.assert_not_called()

    def test_disabled_remote_tools_are_not_promoted_or_sitemapped(self):
        responses = {
            "home": self.client.get(reverse("index")),
            "products": self.client.get(reverse("products")),
            "adtech": self.client.get(reverse("adtech")),
            "tools": self.client.get(reverse("tools")),
            "sitemap": self.client.get(reverse("sitemap_section", kwargs={"section": "tools"})),
        }

        for slug in self.remote_tool_slugs:
            tool_path = reverse("tool_detail", kwargs={"slug": slug})
            for placement, response in responses.items():
                with self.subTest(slug=slug, placement=placement):
                    self.assertNotContains(response, tool_path, html=False)

        for slug in ("utm-builder", "creative-qa-checklist", "creative-preview-lab"):
            tool_path = reverse("tool_detail", kwargs={"slug": slug})
            self.assertContains(responses["products"], tool_path, html=False)
            self.assertContains(responses["tools"], tool_path, html=False)
            self.assertContains(responses["sitemap"], tool_path, html=False)

    def test_deterministic_tools_still_execute_examples(self):
        expectations = {
            "utm-builder": "utm_campaign=seo_examples",
            "creative-qa-checklist": "Checklist",
            "creative-preview-lab": "Vista previa de creatividad",
        }

        for slug, expected in expectations.items():
            with self.subTest(slug=slug):
                response = self.client.post(
                    reverse("tool_detail", kwargs={"slug": slug}),
                    data={"_use_example": "1"},
                )
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected)

    @patch("pi_development.web.services.tools.openai_summary.requests.post")
    @patch("pi_development.web.services.tools.pagespeed.requests.get")
    @patch("pi_development.web.services.tools.http_snapshot.requests.get")
    def test_outbound_helpers_are_guarded_when_remote_tools_are_disabled(
        self,
        mock_snapshot_get,
        mock_pagespeed_get,
        mock_openai_post,
    ):
        from pi_development.web.services.tools.http_snapshot import fetch_site_snapshot
        from pi_development.web.services.tools.openai_summary import generate_ai_summary
        from pi_development.web.services.tools.pagespeed import run_pagespeed_audit
        from pi_development.web.tool_availability import RemoteUrlToolsDisabled

        guarded_calls = (
            lambda: fetch_site_snapshot("https://example.com"),
            lambda: run_pagespeed_audit("https://example.com"),
            lambda: generate_ai_summary({"target_url": "https://example.com"}),
        )
        for guarded_call in guarded_calls:
            with self.subTest(call=guarded_call):
                with self.assertRaises(RemoteUrlToolsDisabled):
                    guarded_call()

        mock_snapshot_get.assert_not_called()
        mock_pagespeed_get.assert_not_called()
        mock_openai_post.assert_not_called()


class CommercialArchitectureTests(TestCase):
    def test_commercial_pages_have_unique_metadata_single_h1_and_no_meta_keywords(self):
        cases = [
            (
                reverse("index"),
                "Custom Software &amp; AdTech Development | Pi Development",
                "Pi Development builds custom software, MVPs, AI automation and AdTech products for companies and digital publishers. Based in Buenos Aires, working globally.",
            ),
            (
                reverse("solutions"),
                "Custom Software Development Services | Pi Development",
                "Custom software development, MVP development, internal tools, integrations and AI automation from Pi Development in Buenos Aires, working globally.",
            ),
            (
                reverse("products"),
                "Software Products &amp; Public Tools | Pi Development",
                "Explore live software products and public tools from Pi Development for technical audits, AdTech diagnostics, creative QA, campaign tracking and web performance.",
            ),
            (
                reverse("adtech"),
                "AdTech Development &amp; Publisher Technology | Pi Development",
                "AdTech development, Google Ad Manager and GPT implementation, creative QA, publisher tools and monetization diagnostics from Pi Development.",
            ),
            (
                reverse("work"),
                "Selected Software Work | Pi Development",
                "Selected software work from Pi Development across discovery platforms, editorial systems, financial data interfaces and custom web platforms.",
            ),
            (
                reverse("insights"),
                "Software &amp; AdTech Insights | Pi Development",
                "Technical insights from Pi Development on AdTech, Google Publisher Tag, creative QA, publisher technology, tracking, technical SEO and web performance.",
            ),
            (
                reverse("company"),
                "Company | Pi Development",
                "Pi Development is an independent custom software and AdTech company based in Buenos Aires, Argentina, working globally.",
            ),
            (
                reverse("contact"),
                "Contact Pi Development | Discuss a Software Project",
                "Contact Pi Development to discuss an MVP, custom software, internal tool, AI automation, platform improvement or AdTech solution.",
            ),
        ]

        titles = []
        descriptions = []
        for path, title, description in cases:
            with self.subTest(path=path):
                response = self.client.get(path)
                content = response.content.decode("utf-8")
                self.assertEqual(response.status_code, 200)
                self.assertIn(f"<title>{title}</title>", content)
                self.assertIn(f'<meta name="description" content="{description}">', content)
                self.assertIn(f'<link rel="canonical" href="{settings.SITE_URL}{path}">', content)
                self.assertEqual(content.count("<h1"), 1)
                self.assertNotIn('<meta name="keywords"', content)
                titles.append(title)
                descriptions.append(description)

        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_navigation_order_and_canonical_redirects(self):
        response = self.client.get(reverse("index"))
        content = response.content.decode("utf-8")
        labels = ["Solutions", "AdTech", "Products", "Work", "Insights", "Company", "Contact"]
        positions = [content.index(f">{label}</a>") for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn(">Home</a>", content)
        self.assertNotIn(">Labs</a>", content)

        redirects = [
            (reverse("labs"), reverse("products")),
            (reverse("about"), reverse("company")),
            (reverse("case_studies"), reverse("work")),
            (reverse("systems"), reverse("solutions")),
            (reverse("approach"), f"{reverse('solutions')}#process"),
            (reverse("blog"), reverse("insights")),
            (reverse("services"), reverse("solutions")),
        ]
        for source, destination in redirects:
            with self.subTest(source=source):
                self.assertRedirects(
                    self.client.get(source),
                    destination,
                    status_code=301,
                    fetch_redirect_response=False,
                )

    def test_products_only_publish_live_tools(self):
        response = self.client.get(reverse("products"))
        for slug in get_public_tool_slugs():
            self.assertContains(response, reverse("tool_detail", kwargs={"slug": slug}), html=False)
        for hidden_copy in ["Operations Copilot", "Publisher Systems Console", "Coming soon", "Placeholder"]:
            self.assertNotContains(response, hidden_copy)

        home_response = self.client.get(reverse("index"))
        self.assertNotContains(home_response, reverse("tool_detail", kwargs={"slug": "ai-auditor"}), html=False)
        self.assertNotContains(home_response, reverse("tool_detail", kwargs={"slug": "adtech-debug-tool"}), html=False)
        self.assertNotContains(home_response, "Operations Copilot")

    def test_contact_form_is_short_intent_aware_and_server_validated(self):
        response = self.client.get(reverse("contact"))
        for label in [
            "Build an MVP",
            "Develop custom software",
            "Automate an operation",
            "Discuss an AdTech solution",
            "Improve an existing platform",
            "Other",
        ]:
            self.assertContains(response, label)
        for field_name in ["name", "email", "company", "project_intent", "problem", "relevant_link"]:
            self.assertContains(response, f'name="{field_name}"', html=False)

        invalid_response = self.client.post(reverse("contact"), data={})
        self.assertEqual(invalid_response.status_code, 200)
        self.assertContains(invalid_response, "This field is required.")
        self.assertContains(invalid_response, 'aria-invalid="true"', html=False)

    @override_settings(CONTACT_EMAIL="contact@example.com")
    @patch("pi_development.web.views.send_mail")
    def test_contact_form_success_uses_existing_email_channel(self, mock_send_mail):
        response = self.client.post(
            reverse("contact"),
            data={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "company": "Analytical Engine",
                "project_intent": "build-mvp",
                "problem": "A product idea needs a reliable first implementation.",
                "relevant_link": "https://example.com/context",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank you. Your project context was received.")
        mock_send_mail.assert_called_once()
        self.assertEqual(mock_send_mail.call_args.kwargs["recipient_list"], ["contact@example.com"])

    @override_settings(ENABLE_REMOTE_URL_TOOLS=True)
    def test_schema_language_and_hreflang_match_the_rendered_page(self):
        home = self.client.get(reverse("index"))
        self.assertContains(home, '<html lang="en">', html=False)
        self.assertContains(home, 'hreflang="en"', html=False)
        self.assertContains(home, 'hreflang="x-default"', html=False)
        self.assertContains(home, '"@type": "Organization"', html=False)
        self.assertContains(home, '"@type": "WebSite"', html=False)

        solutions = self.client.get(reverse("solutions"))
        self.assertContains(solutions, '"@type": "BreadcrumbList"', html=False)
        self.assertContains(solutions, '"@type": "FAQPage"', html=False)

        article = self.client.get(
            reverse(
                "knowledge_page",
                kwargs={"slug": "errores-comunes-en-implementaciones-con-google-publisher-tag"},
            )
        )
        self.assertContains(article, '<html lang="es">', html=False)
        self.assertContains(article, 'hreflang="es"', html=False)
        self.assertContains(article, '"@type": "Article"', html=False)

        tool = self.client.get(reverse("tool_detail", kwargs={"slug": "ai-auditor"}))
        self.assertContains(tool, '<html lang="es">', html=False)
        self.assertContains(tool, '"@type": "SoftwareApplication"', html=False)

    def test_internal_html_links_on_canonical_pages_resolve_without_redirects(self):
        canonical_paths = [
            reverse("index"),
            reverse("solutions"),
            reverse("products"),
            reverse("adtech"),
            reverse("work"),
            reverse("insights"),
            reverse("company"),
            reverse("contact"),
            reverse("tools"),
            reverse("policies"),
            *[
                reverse("tool_detail", kwargs={"slug": slug})
                for slug in get_public_tool_slugs()
            ],
            *[
                reverse("seo_page", kwargs={"slug": slug})
                for slug in get_public_seo_page_slugs()
            ],
            *[
                reverse("knowledge_page", kwargs={"slug": slug})
                for slug in get_public_knowledge_slugs()
            ],
        ]

        checked_links = set()
        for source_path in canonical_paths:
            source_response = self.client.get(source_path)
            self.assertEqual(source_response.status_code, 200)
            hrefs = re.findall(r'<a\b[^>]*\bhref="([^"]+)"', source_response.content.decode("utf-8"))
            for href in hrefs:
                parsed = urlsplit(href)
                if parsed.scheme or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                    continue
                target = parsed.path or "/"
                if target.startswith("/static/") or target in checked_links:
                    continue
                checked_links.add(target)
                with self.subTest(source=source_path, target=target):
                    self.assertEqual(self.client.get(target).status_code, 200)

    def test_sitewide_indexable_pages_have_self_canonicals_unique_metadata_and_accessible_images(self):
        paths = [
            reverse("index"),
            reverse("solutions"),
            reverse("products"),
            reverse("adtech"),
            reverse("work"),
            reverse("insights"),
            reverse("company"),
            reverse("contact"),
            reverse("tools"),
            reverse("policies"),
            *[reverse("tool_detail", kwargs={"slug": slug}) for slug in get_public_tool_slugs()],
            *[reverse("seo_page", kwargs={"slug": slug}) for slug in get_public_seo_page_slugs()],
            *[reverse("knowledge_page", kwargs={"slug": slug}) for slug in get_public_knowledge_slugs()],
        ]

        titles = {}
        descriptions = {}
        for path in paths:
            response = self.client.get(path)
            content = response.content.decode("utf-8")
            title_match = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
            description_match = re.search(r'<meta name="description" content="([^"]+)">', content)

            with self.subTest(path=path):
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(title_match)
                self.assertIsNotNone(description_match)
                self.assertEqual(content.count("<h1"), 1)
                self.assertIn(f'<link rel="canonical" href="{settings.SITE_URL}{path}">', content)
                self.assertNotIn('<meta name="keywords"', content)

                for image_tag in re.findall(r"<img\b[^>]*>", content):
                    self.assertRegex(image_tag, r'\balt="[^"]*"')
                    self.assertRegex(image_tag, r'\bwidth="\d+"')
                    self.assertRegex(image_tag, r'\bheight="\d+"')

                titles.setdefault(title_match.group(1), []).append(path)
                descriptions.setdefault(description_match.group(1), []).append(path)

        duplicate_titles = {title: urls for title, urls in titles.items() if len(urls) > 1}
        duplicate_descriptions = {
            description: urls for description, urls in descriptions.items() if len(urls) > 1
        }
        self.assertEqual(duplicate_titles, {})
        self.assertEqual(duplicate_descriptions, {})


class ToolInsightRulesTests(TestCase):
    def test_ai_auditor_insight_marks_unavailable_snapshot_as_blocking(self):
        insight = build_ai_auditor_insight({"available": False}, {"available": False})

        self.assertEqual(insight["status_label"], "Bloqueado")
        self.assertEqual(insight["risk"], "Bloqueante")
        self.assertEqual(insight["priority"], "Corregir ahora")
        self.assertIn("Entrega", insight["affected_areas"])

    def test_landing_snapshot_insight_prioritizes_slow_and_incomplete_metadata(self):
        insight = build_landing_snapshot_insight(
            {
                "available": True,
                "status_code": 200,
                "response_time_ms": 2800,
                "title": "",
                "meta_description": "",
                "canonical": "",
                "robots": "noindex,nofollow",
                "h1_count": 2,
            }
        )

        self.assertEqual(insight["status_label"], "Bloqueado")
        self.assertEqual(insight["priority"], "Corregir ahora")
        self.assertIn("Rendimiento", insight["affected_areas"])
        self.assertIn("SEO", insight["affected_areas"])

    def test_adtech_debug_insight_flags_partial_stack_structure(self):
        insight = build_adtech_insight(
            {
                "available": True,
                "status_code": 200,
                "response_time_ms": 420,
                "html_excerpt": "<html></html>",
                "script_sources": ["https://securepubads.g.doubleclick.net/tag/js/gpt.js"],
                "slot_hints": [],
            },
            {
                "slot_count_estimate": 0,
                "matched_script_sources": ["https://securepubads.g.doubleclick.net/tag/js/gpt.js"],
                "matched_iframe_sources": [],
                "vendor_hits": ["amazon-adsystem"],
                "raw_matches": ["googletag", "securepubads", "amazon-adsystem"],
                "client_side_likely": True,
                "monetization_signals": [
                    {"key": "googletag", "status": "detected"},
                    {"key": "google_ad_manager", "status": "detected"},
                    {"key": "known_wrappers", "status": "detected"},
                ],
            },
        )

        self.assertEqual(insight["status_label"], "Riesgoso")
        self.assertEqual(insight["priority"], "Revisar pronto")
        self.assertIn("Monetización", insight["affected_areas"])

    def test_creative_qa_insight_blocks_missing_click_and_autoplay_sound(self):
        result = run_creative_qa(
            {
                "creative_name": "Video takeover",
                "format_type": "video",
                "dimensions": "",
                "destination_url": "",
                "click_tag_present": "no",
                "tracking_urls_included": "no",
                "weight_kb": 6500,
                "device_target": "both",
                "sound_behavior": "load",
                "autoplay_behavior": "sound_on",
                "serving_context": "unknown",
                "extra_notes": "",
            }
        )

        self.assertEqual(result["insight"]["status_label"], "Bloqueado")
        self.assertEqual(result["insight"]["risk"], "Bloqueante")
        self.assertEqual(result["insight"]["priority"], "Corregir ahora")
        self.assertIn("Tracking", result["insight"]["affected_areas"])
        self.assertIn("Estado: Bloqueado", result["exports"][0]["text"])
        self.assertIn("Puntaje:", result["exports"][0]["text"])

    def test_creative_preview_insight_flags_blocked_preview(self):
        result = run_creative_preview_lab(
            {
                "creative_name": "Frame escape",
                "creative_type": "display",
                "width": 300,
                "height": 250,
                "input_mode": "html",
                "code": "<script>window.top.location='https://example.com';</script>",
                "click_url": "",
                "notes": "",
            }
        )

        self.assertEqual(result["insight"]["status_label"], "Bloqueado")
        self.assertEqual(result["insight"]["risk"], "Bloqueante")
        self.assertEqual(result["insight"]["priority"], "Corregir ahora")
        self.assertIn("Entrega", result["insight"]["affected_areas"])
