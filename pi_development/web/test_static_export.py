import json
from datetime import date, datetime, timezone
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, override_settings

from pi_development.web.management.commands.export_static import (
    STATIC_REDIRECTS,
    get_public_html_routes,
)
from pi_development.web.management.commands.import_analytics import Command as ImportAnalyticsCommand
from pi_development.web.knowledge_pages import (
    get_latest_knowledge_pages,
    get_public_knowledge_slugs,
    get_recent_news_articles,
)


class StaticExportConfigurationTests(SimpleTestCase):
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
        self.assertContains(response, "Índices Argentinos")
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
        self.assertContains(response, 'data-preview-src="https://indices-argentinos.web.app/"')
        self.assertContains(response, 'data-preview-src="https://arcade-world.web.app/"')
        self.assertContains(response, 'data-preview-src="https://recetasdelsapi.web.app/"')
        self.assertContains(response, 'data-preview-src="https://taitet.com/"')
        self.assertContains(response, 'data-preview-image="desktop"', count=5)
        self.assertContains(response, 'data-preview-image="mobile"', count=5)
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
