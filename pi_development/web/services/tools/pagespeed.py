from django.conf import settings
import requests

from pi_development.web.tool_availability import require_remote_url_tools_enabled


PAGESPEED_CATEGORIES = ("performance", "seo", "best-practices")
METRIC_AUDITS = (
    ("first-contentful-paint", "FCP"),
    ("largest-contentful-paint", "LCP"),
    ("speed-index", "Speed Index"),
    ("total-blocking-time", "TBT"),
    ("cumulative-layout-shift", "CLS"),
)
SEO_AUDITS = (
    "document-title",
    "meta-description",
    "robots-txt",
    "is-crawlable",
    "crawlable-anchors",
    "http-status-code",
)
OPPORTUNITY_AUDITS = (
    "server-response-time",
    "render-blocking-resources",
    "uses-text-compression",
    "uses-optimized-images",
    "unused-css-rules",
    "unused-javascript",
)


def run_pagespeed_audit(url):
    require_remote_url_tools_enabled()
    params = [("url", url), ("strategy", "mobile")]
    params.extend(("category", category) for category in PAGESPEED_CATEGORIES)

    if settings.PAGESPEED_API_KEY:
        params.append(("key", settings.PAGESPEED_API_KEY))

    try:
        response = requests.get(
            settings.PAGESPEED_API_ENDPOINT,
            params=params,
            timeout=settings.TOOLS_HTTP_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return {
            "available": False,
            "status": "unavailable",
            "message": "PageSpeed Insights no respondio o no estuvo disponible para esta URL.",
            "error": str(exc),
        }
    except ValueError as exc:
        return {
            "available": False,
            "status": "invalid",
            "message": "PageSpeed devolvio una respuesta no valida.",
            "error": str(exc),
        }

    lighthouse = payload.get("lighthouseResult") or {}
    categories = lighthouse.get("categories") or {}
    audits = lighthouse.get("audits") or {}
    analysis = payload.get("analysisUTCTimestamp")

    if not categories or not audits:
        return {
            "available": False,
            "status": "empty",
            "message": "PageSpeed no devolvio categorias utiles para construir el diagnostico.",
            "error": "",
        }

    return {
        "available": True,
        "status": "ok",
        "analysis_timestamp": analysis,
        "categories": {
            "performance": _score(categories.get("performance")),
            "seo": _score(categories.get("seo")),
            "best_practices": _score(categories.get("best-practices")),
        },
        "metrics": _collect_metrics(audits),
        "seo_checks": _collect_seo_checks(audits),
        "opportunities": _collect_opportunities(audits),
    }


def _score(category):
    score = (category or {}).get("score")
    if score is None:
        return None
    return int(round(score * 100))


def _collect_metrics(audits):
    metrics = []
    for audit_key, label in METRIC_AUDITS:
        audit = audits.get(audit_key) or {}
        if not audit:
            continue
        metrics.append(
            {
                "label": label,
                "value": audit.get("displayValue") or "No disponible",
            }
        )
    return metrics


def _collect_seo_checks(audits):
    checks = []
    for audit_key in SEO_AUDITS:
        audit = audits.get(audit_key) or {}
        if not audit:
            continue
        checks.append(
            {
                "label": audit.get("title") or audit_key.replace("-", " ").title(),
                "status": audit.get("scoreDisplayMode") or "unknown",
                "value": _seo_status_value(audit),
            }
        )
    return checks


def _collect_opportunities(audits):
    opportunities = []
    for audit_key in OPPORTUNITY_AUDITS:
        audit = audits.get(audit_key) or {}
        value = audit.get("displayValue")
        score = audit.get("score")
        if value or (score is not None and score < 1):
            opportunities.append(
                {
                    "label": audit.get("title") or audit_key.replace("-", " ").title(),
                    "value": value or "Revision recomendada",
                }
            )
    return opportunities[:4]


def _seo_status_value(audit):
    if audit.get("score") == 1:
        return "OK"
    if audit.get("score") == 0:
        return "Revisar"
    return audit.get("displayValue") or "Sin dato"
