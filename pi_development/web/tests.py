from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from pi_development.web.services.tools.adtech_debug import build_insight as build_adtech_insight
from pi_development.web.services.tools.ai_auditor import build_insight as build_ai_auditor_insight
from pi_development.web.services.tools.creative_preview_lab import run_creative_preview_lab
from pi_development.web.services.tools.creative_qa import run_creative_qa
from pi_development.web.services.tools.landing_snapshot import build_insight as build_landing_snapshot_insight


class PublicPagesTests(TestCase):
    def test_primary_pages_respond(self):
        page_names = [
            "index",
            "systems",
            "tools",
            "tool_detail",
            "work",
            "approach",
            "about",
            "contact",
            "blog",
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

    def test_home_prioritizes_tools_and_clear_positioning(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, "Analiza. Valida. Optimiza.")
        self.assertContains(response, "Herramientas técnicas para AdTech, creatividades y rendimiento web")
        self.assertContains(response, 'href="/tools/"', html=False)
        self.assertContains(response, "El foco principal del sitio está aquí.")

    def test_navigation_is_available_on_primary_pages(self):
        for name in ["systems", "tools", "work", "approach", "about", "contact"]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertContains(response, "Inicio")
                self.assertContains(response, "Herramientas")
                self.assertContains(response, "Contacto")

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
        self.assertContains(response, "Observaciones técnicas")
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
        self.assertContains(response, "Estructura básica")
        self.assertContains(response, "Señales rápidas")
        self.assertContains(response, "Siguiente paso recomendado")
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
