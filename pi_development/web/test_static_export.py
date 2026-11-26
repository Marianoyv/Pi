import json
from datetime import date, datetime, timezone
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, override_settings

from pi_development.web.management.commands.export_static import (
    GOOGLE_SITE_VERIFICATION_FILE,
    STATIC_REDIRECTS,
    get_public_html_routes,
)
from pi_development.web.management.commands.import_analytics import Command as ImportAnalyticsCommand
from pi_development.web.management.commands.validate_editorial import Command as EditorialValidationCommand
from pi_development.web.knowledge_pages import (
    get_latest_knowledge_pages,
    get_public_knowledge_slugs,
    get_recent_news_articles,
)
from pi_development.web.finance_catalog import get_finance_routes


class StaticExportConfigurationTests(SimpleTestCase):
    def test_google_search_console_verification_file_is_pinned(self):
        verification_file = Path(settings.BASE_DIR) / GOOGLE_SITE_VERIFICATION_FILE

        self.assertEqual(
            verification_file.read_text(encoding="utf-8").strip(),
            f"google-site-verification: {GOOGLE_SITE_VERIFICATION_FILE}",
        )

    def test_public_route_inventory_is_unique_and_excludes_preview_routes(self):
        routes = get_public_html_routes()

        self.assertEqual(len(routes), len(set(routes)))
        self.assertIn("/soluciones-para-negocios/", routes)
        self.assertIn("/planes-web/", routes)
        self.assertIn("/products/utm-builder/", routes)
        self.assertIn("/work/juno-metales/", routes)
        self.assertIn("/work/indices-argentinos/", routes)
        self.assertIn("/work/arcade-world/", routes)
        self.assertIn("/work/recetas-del-sapi/", routes)
        self.assertIn("/work/taitet/", routes)
        self.assertNotIn("/rebuild/", routes)
        self.assertNotIn("/design-lab/", routes)

    def test_pi_finance_inventory_absorbs_the_complete_financial_suite(self):
        routes = get_finance_routes()

        self.assertEqual(len(routes), 22)
        self.assertEqual(len(routes), len(set(routes)))
        self.assertIn("/finance/", routes)
        self.assertIn("/finance/ipc/", routes)
        self.assertIn("/finance/icl/", routes)
        self.assertIn("/finance/cuotas-o-contado/", routes)
        self.assertIn("/finance/cancelar-deudas/", routes)
        self.assertIn("/finance/comparador-plazos-fijos/", routes)
        self.assertIn("/finance/credito-uva/", routes)
        self.assertIn("/finance/monotributo/", routes)

    def test_business_solutions_page_is_english_and_has_a_clear_offer(self):
        response = self.client.get("/soluciones-para-negocios/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lang="en"')
        self.assertContains(response, "A website that explains your business")
        self.assertContains(response, "A complete service")
        self.assertContains(response, "The web also needs a marketing base")
        self.assertContains(response, "Juno Metales")
        self.assertContains(response, "Taitet")
        self.assertContains(response, "AI can create a page")
        self.assertGreaterEqual(response.content.count(b'href="/planes-web/"'), 5)
        self.assertContains(response, '"@type": "FAQPage"')

    def test_web_plans_page_compares_three_scoped_packages(self):
        response = self.client.get("/planes-web/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lang="en"')
        self.assertContains(response, "Presence")
        self.assertContains(response, "Catalog")
        self.assertContains(response, "Assisted sale")
        self.assertContains(response, "USD 550")
        self.assertContains(response, "USD 1,100")
        self.assertContains(response, "USD 2,200")
        self.assertContains(response, "Recommended starting point")
        self.assertContains(response, "30 days to correct delivery errors")
        self.assertContains(response, '"@type": "FAQPage"')

    def test_homepage_and_navigation_link_to_business_solutions(self):
        response = self.client.get("/")

        self.assertContains(response, 'href="/soluciones-para-negocios/"', count=3)
        self.assertNotContains(response, 'id="business-entry-title"')

    def test_editorial_example_is_loaded_from_json_with_sources_and_metadata(self):
        response = self.client.get("/blog/google-publisher-tag-fetch-priority-refresh-bfcache/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google Publisher Tag prioriza su carga")
        self.assertContains(response, "Published 2026-09-06")
        self.assertContains(response, "5 min read")
        self.assertContains(response, "Google Publisher Tag release notes")
        self.assertContains(response, '"@type": "NewsArticle"')
        self.assertContains(response, '"datePublished": "2026-09-06T23:40:14-03:00"')
        self.assertContains(response, '"width": 1536')
        self.assertContains(response, 'name="robots" content="index, follow, max-image-preview:large"')
        self.assertContains(response, "web/img/insights/google-publisher-tag-bfcache.webp")
        self.assertContains(response, '>Mariano Tami</a>')
        self.assertContains(response, 'lang="es"')
        self.assertContains(response, 'data-editorial-article')
        self.assertContains(response, 'data-article-slug="google-publisher-tag-fetch-priority-refresh-bfcache"')
        self.assertContains(response, 'data-article-cluster="adtech"')

    def test_news_sitemap_selects_only_news_from_the_last_two_days(self):
        reference = datetime(2026, 9, 11, tzinfo=timezone.utc)
        articles = get_recent_news_articles(reference_datetime=reference)
        slugs = {article["slug"] for article in articles}

        self.assertEqual(
            slugs,
            {
                "google-ad-manager-begin-to-render-impresiones",
                "ia-extincion-humanidad-diez-anos",
            },
        )
        response = self.client.get("/sitemap-news.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"')
        self.assertContains(self.client.get("/sitemap.xml"), "/sitemap-news.xml")

    def test_insights_lists_every_public_editorial_article(self):
        response = self.client.get("/insights/")

        self.assertEqual(response.status_code, 200)
        for slug in get_public_knowledge_slugs():
            self.assertContains(response, f'href="/blog/{slug}/"')

    def test_editorial_quality_gate_accepts_the_example_article(self):
        from django.core.management import call_command

        call_command("validate_editorial", verbosity=0)

    def test_measured_editorial_contract_requires_independent_evidence_and_ai_disclosure(self):
        article_path = Path(settings.BASE_DIR) / "content" / "articles" / "2026-10-23-google-flexibiliza-video-sticky.json"
        article = json.loads(article_path.read_text(encoding="utf-8"))
        article.update(
            {
                "published_at": "2026-11-24",
                "updated_at": "2026-11-24",
                "published_datetime": "2026-11-24T08:00:00-03:00",
                "updated_datetime": "2026-11-24T08:00:00-03:00",
                "human_question": "¿Qué cambia para una persona cuando una regla técnica modifica el video que ve?",
                "editorial_hypothesis": "Una consecuencia concreta sostendrá mejor la lectura que una lista de cambios.",
                "distribution_hypothesis": "La pieza se probará con lectores de producto y operaciones en el canal propio.",
                "image_record": {
                    "creator": "Pi Editorial",
                    "created_at": "2026-11-24",
                    "method": "ai-assisted-editorial-illustration",
                    "source_files": [],
                    "disclosure": "Ilustración editorial generada con IA. No es una fotografía documental del hecho.",
                },
            }
        )
        article["sources"][1]["source_type"] = "independent"

        self.assertEqual(EditorialValidationCommand._validate_article(article), [])

        article["image_record"]["disclosure"] = "Imagen editorial realista."
        errors = EditorialValidationCommand._validate_article(article)
        self.assertIn("AI-assisted images must disclose the use of IA or inteligencia artificial", errors)
        self.assertIn("AI-assisted images must state that they are not documentary photography", errors)

    def test_article_template_exposes_image_disclosure_below_the_hero(self):
        template = (
            Path(settings.BASE_DIR) / "pi_development" / "web" / "templates" / "web" / "knowledge_article_page.html"
        ).read_text(encoding="utf-8")

        self.assertIn("knowledge_page.image_record.disclosure", template)
        self.assertIn("<figcaption>", template)

    def test_trend_driven_news_requires_current_signals_and_separate_layers(self):
        article_path = Path(settings.BASE_DIR) / "content" / "articles" / "2026-10-23-google-flexibiliza-video-sticky.json"
        article = json.loads(article_path.read_text(encoding="utf-8"))
        article.update(
            {
                "published_at": "2026-11-25",
                "updated_at": "2026-11-25",
                "published_datetime": "2026-11-25T08:00:00-03:00",
                "updated_datetime": "2026-11-25T08:00:00-03:00",
                "human_question": "¿Qué cambia para una persona cuando una tendencia tecnológica llega a un producto cotidiano?",
                "editorial_hypothesis": "La explicación de una consecuencia concreta será más útil que repetir el anuncio.",
                "distribution_hypothesis": "La pieza se probará en canales propios y búsqueda durante siete días.",
                "image_record": {
                    "creator": "Pi Editorial",
                    "created_at": "2026-11-25",
                    "method": "ai-assisted-editorial-illustration",
                    "source_files": [],
                    "disclosure": "Ilustración editorial generada con IA. No es una fotografía documental del hecho.",
                },
                "trend_evidence": {
                    "query": "cambio tecnológico de interés actual",
                    "captured_at": "2026-11-23T20:00:00-03:00",
                    "rechecked_at": "2026-11-25T07:30:00-03:00",
                    "window_hours": 72,
                    "market": "AR + internacional",
                    "status": "rising",
                    "saturation": "medium",
                    "editorial_opportunity": "La cobertura no explica todavía la consecuencia para usuarios.",
                    "signals": [
                        {
                            "signal_type": "google-trends",
                            "source": "Google Trends",
                            "url": "https://trends.google.com/trending",
                            "observed_at": "2026-11-25T07:20:00-03:00",
                            "evidence": "La consulta aparece entre los temas tecnológicos en crecimiento.",
                        },
                        {
                            "signal_type": "news-cluster",
                            "source": "Google News",
                            "url": "https://news.google.com/",
                            "observed_at": "2026-11-25T07:25:00-03:00",
                            "evidence": "Varios medios independientes publicaron cobertura reciente.",
                        },
                    ],
                },
                "news_layers": {
                    "official_announcement": ["La fuente primaria confirmó el cambio y su fecha de aplicación."],
                    "independent_verification": ["Una fuente independiente confirmó el alcance y señaló límites."],
                    "pi_editorial": ["Pi interpreta la consecuencia sin presentarla como un hecho anunciado."],
                    "quality_evidence": [
                        "Fuente primaria comprobada.",
                        "Contraste independiente comprobado.",
                        "Tendencia revalidada antes de publicar.",
                    ],
                },
            }
        )
        article["sources"][1]["source_type"] = "independent"

        self.assertEqual(EditorialValidationCommand._validate_article(article), [])

        article["trend_evidence"]["rechecked_at"] = "2026-11-21T07:30:00-03:00"
        errors = EditorialValidationCommand._validate_article(article)
        self.assertIn("trend evidence must be rechecked within 72 hours before publication", errors)

        article["trend_evidence"]["rechecked_at"] = "2026-11-25T07:30:00-03:00"
        article.pop("news_layers")
        errors = EditorialValidationCommand._validate_article(article)
        self.assertIn("news articles require separate official, verification, editorial and quality layers", errors)

    def test_news_template_separates_facts_verification_editorial_and_quality(self):
        template = (
            Path(settings.BASE_DIR) / "pi_development" / "web" / "templates" / "web" / "knowledge_article_page.html"
        ).read_text(encoding="utf-8")

        self.assertIn("Qué se anunció", template)
        self.assertIn("Qué pudimos verificar", template)
        self.assertIn("Lectura editorial de Pi", template)
        self.assertIn("Cómo verificamos esta noticia", template)
        self.assertIn("knowledge_page.trend_evidence.signals", template)

    def test_editorial_index_is_compact_and_uses_real_internal_routes(self):
        from django.core.management import call_command

        call_command("build_editorial_index", verbosity=0)
        index_path = Path(settings.BASE_DIR) / "content" / "editorial" / "index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))

        self.assertLessEqual(len(index["recent_articles"]), 120)
        published_dates = [article["published_at"] for article in index["recent_articles"]]
        self.assertEqual(published_dates, sorted(published_dates, reverse=True))
        self.assertIn(
            "gaming-hardware-2026-pc-vs-handheld",
            {article["slug"] for article in index["recent_articles"]},
        )
        self.assertIn(
            "google-publisher-tag-fetch-priority-refresh-bfcache",
            {article["slug"] for article in index["recent_articles"]},
        )
        self.assertIn(
            {"slug": "debug-gpt-ads", "title": "How to debug GPT Ads on a web page", "url": "/debug-gpt-ads/"},
            index["internal_links"]["guides"],
        )

    def test_static_redirect_fallbacks_preserve_legacy_entry_points(self):
        self.assertEqual(STATIC_REDIRECTS["/indices-argentinos/"], "/finance/")
        self.assertEqual(STATIC_REDIRECTS["/finance/calculadoras/"], "/finance/")
        self.assertEqual(STATIC_REDIRECTS["/systems/"], "/solutions/")
        self.assertEqual(STATIC_REDIRECTS["/approach/"], "/solutions/#process")
        self.assertEqual(STATIC_REDIRECTS["/blog/"], "/insights/")
        self.assertEqual(STATIC_REDIRECTS["/tools/utm-builder/"], "/products/utm-builder/")

    def test_firebase_hosting_no_longer_rewrites_all_traffic_to_cloud_run(self):
        config = json.loads((Path(settings.BASE_DIR) / "firebase.json").read_text(encoding="utf-8"))
        hosting = config["hosting"]

        self.assertEqual(hosting["public"], "dist")
        self.assertNotIn("rewrites", hosting)
        self.assertTrue(hosting["redirects"])
        finance_redirect = next(
            item for item in hosting["redirects"] if item.get("destination") == "/finance/" and "regex" in item
        )
        self.assertEqual(finance_redirect["regex"], "^/finance/calculadoras/?$")

    def test_firebase_headers_keep_html_fresh_and_protect_every_response(self):
        config = json.loads((Path(settings.BASE_DIR) / "firebase.json").read_text(encoding="utf-8"))
        headers = config["hosting"]["headers"]
        global_rule = headers[0]
        static_rule = headers[1]
        global_values = {item["key"]: item["value"] for item in global_rule["headers"]}

        self.assertEqual(global_rule["source"], "**")
        self.assertEqual(global_values["Cache-Control"], "no-cache")
        self.assertEqual(global_values["X-Content-Type-Options"], "nosniff")
        self.assertEqual(global_values["X-Frame-Options"], "SAMEORIGIN")
        self.assertEqual(global_values["Referrer-Policy"], "strict-origin-when-cross-origin")
        self.assertIn("frame-ancestors", global_values["Content-Security-Policy"])
        self.assertEqual(static_rule["source"], "/static/**")
        self.assertIn("max-age", static_rule["headers"][0]["value"])

    @override_settings(STATIC_EXPORT=True, CONTACT_FORM_ENABLED=False)
    def test_static_contact_page_prepares_a_local_brief_without_a_backend(self):
        response = self.client.get("/contact/")
        contact_script = (Path(settings.BASE_DIR) / "static" / "web" / "js" / "contact-brief.js").read_text(
            encoding="utf-8"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-contact-brief")
        self.assertContains(response, "Prepare project brief")
        self.assertContains(response, "Nothing is sent or stored")
        self.assertContains(response, "contact-brief.js?v=20261114-1")
        self.assertContains(response, 'data-whatsapp-url="https://wa.me/5491170619703"')
        self.assertNotContains(response, 'method="post"')
        self.assertNotContains(response, "csrfmiddlewaretoken")
        self.assertNotIn("fetch(", contact_script)

    @override_settings(STATIC_EXPORT=True, CONTACT_FORM_ENABLED=False)
    def test_static_tool_page_uses_browser_runtime_without_csrf_or_network_fetch(self):
        response = self.client.get("/products/utm-builder/")
        browser_script = (Path(settings.BASE_DIR) / "static" / "web" / "js" / "browser-tools.js").read_text(
            encoding="utf-8"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-browser-tool="utm-builder"')
        self.assertContains(response, "browser-tools.js")
        self.assertNotContains(response, "csrfmiddlewaretoken")
        self.assertNotIn("fetch(", browser_script)

    def test_homepage_includes_live_capability_engine_and_public_calculator_case(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "PI / CAPABILITY ENGINE")
        self.assertContains(response, "Pi Finance")
        self.assertContains(response, "web/img/indices-desktop.webp")
        self.assertContains(response, "web/img/indices-mobile.webp")
        self.assertContains(response, 'data-metric-board')
        self.assertNotContains(response, 'data-motion-toggle')
        self.assertContains(response, 'motion-effects.js')
        self.assertContains(response, "Latest publications")
        for article in get_latest_knowledge_pages(limit=3):
            self.assertContains(response, f'/blog/{article["slug"]}/')
            self.assertContains(response, article["image"])
        self.assertNotContains(response, "PI BUENOS AIRES")

    def test_homepage_leads_from_clear_offer_to_products_and_product_journey(self):
        response = self.client.get("/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I build software that helps businesses find new revenue opportunities")
        self.assertContains(response, 'fetchpriority="high"')
        self.assertContains(response, 'data-home-products')
        self.assertEqual(html.count('data-home-product href='), 3)
        self.assertContains(response, "UTM Builder")
        self.assertContains(response, "Creative QA Checklist")
        self.assertContains(response, "Creative Preview Lab")
        self.assertContains(response, 'data-section-name="product-journey"')
        self.assertContains(response, 'id="business-value"')
        self.assertLess(html.index('class="pi-home-hero"'), html.index('data-home-products'))
        self.assertLess(html.index('data-home-products'), html.index('data-product-stage'))
        self.assertLess(html.index('data-product-stage'), html.index('id="business-value"'))

    def test_base_template_loads_first_party_analytics_events(self):
        response = self.client.get("/")
        analytics_script = (Path(settings.BASE_DIR) / "static" / "web" / "js" / "main.js").read_text(
            encoding="utf-8"
        )

        self.assertContains(response, "G-6XVTWEY4LW")
        self.assertRegex(response.content.decode(), r"/static/web/js/main\.js\?v=\d{8}-\d+")
        self.assertContains(response, 'web/js/analytics.js')
        self.assertContains(response, 'data-measurement-id="G-6XVTWEY4LW"')
        self.assertNotContains(response, '<script async src="https://www.googletagmanager.com/gtag/js')
        self.assertNotContains(response, 'data-analytics-banner')
        self.assertContains(response, 'data-analytics-preferences')
        self.assertContains(response, 'data-analytics-consent="denied"')
        self.assertContains(response, 'data-analytics-consent="disabled"')
        self.assertIn("contact_cta_click", analytics_script)
        self.assertIn("contact_start", analytics_script)
        self.assertIn("contact_method", analytics_script)
        self.assertIn("tool_use", analytics_script)
        self.assertIn("tool_error", analytics_script)
        self.assertIn("tool_result_copy", analytics_script)
        self.assertIn("outbound_click", analytics_script)
        self.assertIn("project_preview_open", analytics_script)
        self.assertIn("utm_preset_select", analytics_script)
        self.assertIn("editorial_article_view", analytics_script)
        self.assertIn("editorial_read_progress", analytics_script)
        self.assertIn("editorial_engaged_time", analytics_script)
        self.assertIn("editorial_to_pi", analytics_script)
        self.assertIn("origin_article_slug", analytics_script)
        self.assertIn("pi:tool-complete", analytics_script)
        self.assertNotIn("document.addEventListener('submit'", analytics_script)
        self.assertNotIn("destination.href", analytics_script)

    @override_settings(STATIC_EXPORT=True, CONTACT_FORM_ENABLED=False)
    def test_tool_tracking_is_emitted_after_result_generation(self):
        response = self.client.get("/products/utm-builder/")
        browser_script = (Path(settings.BASE_DIR) / "static" / "web" / "js" / "browser-tools.js").read_text(
            encoding="utf-8"
        )

        self.assertContains(response, "browser-tools.js?v=20261009-2")
        self.assertContains(response, 'data-utm-preset=', count=4)
        self.assertContains(response, 'data-utm-preset-feedback')
        self.assertIn("const UTM_PRESETS", browser_script)
        self.assertIn("pi:utm-preset", browser_script)
        self.assertIn("normalize('NFD')", browser_script)
        self.assertIn("handler(form);", browser_script)
        self.assertIn("emitToolEvent(form, 'pi:tool-complete')", browser_script)
        self.assertIn("emitToolEvent(form, 'pi:tool-error'", browser_script)
        self.assertLess(
            browser_script.index("handler(form);"),
            browser_script.index("emitToolEvent(form, 'pi:tool-complete')"),
        )

    def test_work_page_uses_lazy_interactive_project_previews(self):
        response = self.client.get("/work/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-project-preview', count=5)
        self.assertContains(response, 'data-project-name=', count=5)
        self.assertContains(response, 'data-preview-size-button="mobile"', count=5)
        self.assertContains(response, 'data-preview-src="https://junometales.com/"')
        self.assertContains(response, 'data-preview-src="/finance/"')
        self.assertContains(response, 'data-preview-src="https://arcade-world.web.app/"')
        self.assertContains(response, 'data-preview-src="https://recetasdelsapi.web.app/"')
        self.assertContains(response, 'data-preview-src="https://taitet.com/"')
        self.assertContains(response, 'data-preview-image="desktop"', count=5)
        self.assertContains(response, 'data-preview-image="mobile"', count=5)
        self.assertContains(response, 'preload="none"')
        self.assertContains(response, "controls")
        self.assertNotContains(response, "autoplay")
        self.assertNotContains(response, "pi-indices-mock")

    def test_english_gaming_article_localizes_article_chrome_and_metadata(self):
        response = self.client.get("/blog/generative-ai-npcs-conversations/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lang="en"')
        self.assertContains(response, "Introduction")
        self.assertContains(response, "Key takeaways")
        self.assertContains(response, "Frequently asked questions")
        self.assertContains(response, "Published 2026-09-15")
        self.assertNotContains(response, "Introduccion")

    def test_legacy_tool_routes_redirect_to_products(self):
        self.assertRedirects(
            self.client.get("/tools/utm-builder/"),
            "/products/utm-builder/",
            status_code=301,
            fetch_redirect_response=False,
        )


class AnalyticsImportTests(SimpleTestCase):
    def test_comparison_periods_are_equal_and_non_overlapping(self):
        periods = ImportAnalyticsCommand._periods(date(2026, 10, 6), 28)

        self.assertEqual(periods["current"]["start"], date(2026, 9, 9))
        self.assertEqual(periods["current"]["end"], date(2026, 10, 6))
        self.assertEqual(periods["previous"]["start"], date(2026, 8, 12))
        self.assertEqual(periods["previous"]["end"], date(2026, 9, 8))

    def test_ga4_rows_are_normalized_without_losing_period(self):
        response = {
            "dimensionHeaders": [{"name": "date"}],
            "metricHeaders": [{"name": "sessions"}],
            "rows": [{"dimensionValues": [{"value": "20261006"}], "metricValues": [{"value": "12"}]}],
        }

        rows = ImportAnalyticsCommand._normalize_ga4(response, "current")

        self.assertEqual(rows, [{"period": "current", "date": "20261006", "sessions": "12"}])

    def test_summary_compares_current_and_previous_totals(self):
        periods = ImportAnalyticsCommand._periods(date(2026, 10, 6), 1)
        summary = ImportAnalyticsCommand._build_summary(
            {
                "ga4_overview": [
                    {"period": "current", "sessions": "15"},
                    {"period": "previous", "sessions": "10"},
                ]
            },
            periods,
        )

        self.assertIn("sessions: 15 (+50.0%)", summary)

    def test_summary_separates_editorial_performance(self):
        periods = ImportAnalyticsCommand._periods(date(2026, 10, 22), 1)
        summary = ImportAnalyticsCommand._build_summary(
            {
                "ga4_pages": [
                    {
                        "period": "current",
                        "pagePathPlusQueryString": "/blog/historia-humana/",
                        "pageTitle": "Una historia humana | Pi",
                        "screenPageViews": "8",
                        "userEngagementDuration": "240",
                        "eventCount": "18",
                        "keyEvents": "0",
                    },
                    {
                        "period": "current",
                        "pagePathPlusQueryString": "/solutions/",
                        "pageTitle": "Solutions | Pi",
                        "screenPageViews": "20",
                        "userEngagementDuration": "60",
                        "eventCount": "25",
                        "keyEvents": "0",
                    },
                ]
            },
            periods,
        )

        self.assertIn("## Editorial", summary)
        self.assertIn("screenPageViews: 8", summary)
        self.assertIn("Una historia humana", summary)
        self.assertNotIn("Solutions | Pi", summary)
