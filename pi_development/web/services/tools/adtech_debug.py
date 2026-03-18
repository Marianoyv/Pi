import re

from .export_utils import build_copy_exports
from .http_snapshot import fetch_site_snapshot
from .insight_utils import build_insight_issue, summarize_insight


SIGNAL_DEFINITIONS = [
    {
        "key": "googletag",
        "label": "Google Publisher Tag / googletag",
        "patterns": ("googletag", "gpt.js", "securepubads", "googletag.pubads"),
        "positive": "Se detectaron señales compatibles con Google Publisher Tag en la respuesta inicial.",
        "negative": "No aparecieron señales visibles de GPT en el HTML inicial.",
    },
    {
        "key": "google_ad_manager",
        "label": "Google Ad Manager",
        "patterns": ("securepubads.g.doubleclick.net", "googletag.defineSlot", "googletag.display"),
        "positive": "La respuesta incluye referencias compatibles con Google Ad Manager.",
        "negative": "No aparecieron referencias directas a Google Ad Manager en esta lectura básica.",
    },
    {
        "key": "adsense",
        "label": "AdSense",
        "patterns": ("adsbygoogle", "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js", "google_ad_client"),
        "positive": "Se detectaron scripts o marcas compatibles con AdSense.",
        "negative": "No aparecieron señales visibles de AdSense en la respuesta inicial.",
    },
    {
        "key": "prebid",
        "label": "Prebid o bidder libraries",
        "patterns": ("prebid", "prebid.js", "pbjs", "hb_pb", "hb_bidder"),
        "positive": "Se detectaron señales de header bidding o bidder libraries.",
        "negative": "No se detectaron señales claras de Prebid o bidder libraries en el HTML inicial.",
    },
    {
        "key": "known_wrappers",
        "label": "Wrappers o vendors conocidos",
        "patterns": (
            "amazon-adsystem",
            "criteo",
            "pubmatic",
            "openx",
            "rubicon",
            "appnexus",
            "adnxs",
            "indexww",
            "triplelift",
        ),
        "positive": "Se detectaron vendors o wrappers publicitarios conocidos en la respuesta inicial.",
        "negative": "No aparecieron wrappers o vendors conocidos en esta lectura básica.",
    },
    {
        "key": "iframes",
        "label": "Iframes relacionados con publicidad",
        "patterns": (
            "doubleclick",
            "googlesyndication",
            "adnxs",
            "criteo",
            "amazon-adsystem",
            "pubmatic",
        ),
        "positive": "Se detectaron iframes con fuentes compatibles con publicidad.",
        "negative": "No se detectaron iframes publicitarios claros en la respuesta inicial.",
    },
    {
        "key": "advanced_behaviors",
        "label": "Refresh / lazy load / targeting",
        "patterns": (
            "pubads().refresh",
            "googletag.pubads().refresh",
            "enableLazyLoad",
            ".setTargeting(",
            "cust_params",
            "setTargeting",
        ),
        "positive": "Hay señales parciales de refresh, lazy load o targeting en el HTML recibido.",
        "negative": "No aparecieron señales claras de refresh, lazy load o targeting en la respuesta inicial.",
    },
]

SLOT_PATTERNS = (
    r"div-gpt-ad-[a-z0-9\-_]+",
    r"data-ad-slot\s*=\s*[\"'][^\"']+[\"']",
    r"data-ad-unit\s*=\s*[\"'][^\"']+[\"']",
    r"id\s*=\s*[\"'][^\"']*adslot[^\"']*[\"']",
    r"class\s*=\s*[\"'][^\"']*adslot[^\"']*[\"']",
)

SCRIPT_VENDOR_PATTERNS = (
    "googletag",
    "securepubads",
    "doubleclick",
    "adsbygoogle",
    "prebid",
    "amazon-adsystem",
    "criteo",
    "pubmatic",
    "openx",
    "rubicon",
    "adnxs",
    "appnexus",
)


def run_adtech_debug(url):
    snapshot = fetch_site_snapshot(url)
    analysis = analyze_adtech_signals(snapshot)
    diagnosis = build_diagnosis(url, snapshot, analysis)
    insight = build_insight(snapshot, analysis)
    sources = build_sources(snapshot, analysis)

    return {
        "target_url": url,
        "snapshot": snapshot,
        "analysis": analysis,
        "diagnosis": diagnosis,
        "insight": insight,
        "sources": sources,
        "exports": build_exports(diagnosis, analysis, insight),
    }


def analyze_adtech_signals(snapshot):
    html = (snapshot.get("html_excerpt") or "").lower()
    script_sources = [item.lower() for item in snapshot.get("script_sources") or []]
    iframe_sources = [item.lower() for item in snapshot.get("iframe_sources") or []]
    slot_hints = list(snapshot.get("slot_hints") or [])
    joined_scripts = "\n".join(script_sources)
    joined_iframes = "\n".join(iframe_sources)
    combined_text = "\n".join([html, joined_scripts, joined_iframes, "\n".join(item.lower() for item in slot_hints)])

    monetization_signals = []
    raw_matches = []

    for definition in SIGNAL_DEFINITIONS:
        hits = [pattern for pattern in definition["patterns"] if pattern.lower() in combined_text]
        raw_matches.extend(hits)
        status = "detected" if hits else "not-detected"
        monetization_signals.append(
            {
                "key": definition["key"],
                "label": definition["label"],
                "status": status,
                "matched_patterns": sorted(set(hits)),
                "detail": definition["positive"] if hits else definition["negative"],
            }
        )

    slot_matches = []
    for pattern in SLOT_PATTERNS:
        slot_matches.extend(re.findall(pattern, html, flags=re.IGNORECASE))

    iframe_matches = [src for src in iframe_sources if any(token in src for token in SIGNAL_DEFINITIONS[5]["patterns"])]
    script_matches = [src for src in script_sources if any(token in src for token in SCRIPT_VENDOR_PATTERNS)]
    vendor_hits = sorted(
        {
            vendor
            for vendor in SCRIPT_VENDOR_PATTERNS
            if vendor in combined_text and vendor not in {"googletag", "securepubads", "doubleclick", "adsbygoogle", "prebid"}
        }
    )

    unique_slots = _unique_preserve_order(slot_hints + slot_matches)

    return {
        "monetization_signals": monetization_signals,
        "matched_script_sources": script_matches[:8],
        "matched_iframe_sources": iframe_matches[:6],
        "slot_matches": unique_slots,
        "slot_count_estimate": len(unique_slots),
        "vendor_hits": vendor_hits,
        "raw_matches": _unique_preserve_order(raw_matches)[:10],
        "client_side_likely": infer_client_side_limitation(snapshot, monetization_signals),
    }


def build_diagnosis(url, snapshot, analysis):
    overview = build_overview(snapshot, analysis)
    findings = build_findings(snapshot, analysis)
    opportunities = build_opportunities(snapshot, analysis)
    recommendation = build_recommendation(snapshot, analysis, opportunities)
    limitations = build_limitations(snapshot, analysis)

    return {
        "target_url": url,
        "overview": overview,
        "monetization_signals": analysis["monetization_signals"],
        "technical_findings": findings,
        "opportunities": opportunities,
        "recommendation": recommendation,
        "limitations": limitations,
    }


def build_sources(snapshot, analysis):
    return [
        {
            "label": "Snapshot HTTP",
            "status": "ok" if snapshot.get("available") else "limited",
            "detail": _http_source_detail(snapshot),
        },
        {
            "label": "Escaneo por patrones",
            "status": "ok" if snapshot.get("available") else "limited",
            "detail": _pattern_source_detail(analysis),
        },
        {
            "label": "Alcance del render",
            "status": "limited",
            "detail": "La detección ocurre sobre la respuesta inicial y el HTML descargado; una parte del stack puede vivir solo en cliente.",
        },
    ]


def build_overview(snapshot, analysis):
    if not snapshot.get("available"):
        return {
            "label": "Lectura parcial",
            "tone": "critical",
            "summary": "No se pudo obtener la URL desde backend. La herramienta no pudo inspeccionar HTML ni detectar señales publicitarias visibles.",
        }

    signal_count = sum(1 for item in analysis["monetization_signals"] if item["status"] == "detected")
    slot_count = analysis["slot_count_estimate"]

    if signal_count >= 3 or (signal_count >= 2 and slot_count >= 1):
        return {
            "label": "Stack visible en respuesta inicial",
            "tone": "good",
            "summary": "La URL respondió y expone señales AdTech legibles desde backend. Hay evidencia visible de stack publicitario o monetización en el HTML descargado.",
        }

    if signal_count >= 1:
        return {
            "label": "Señales parciales detectadas",
            "tone": "warn",
            "summary": "La URL respondió y muestra algunas señales de monetización, pero la implementación visible desde backend parece parcial o incompleta.",
        }

    return {
        "label": "Sin stack visible en respuesta inicial",
        "tone": "warn",
        "summary": "La URL respondió y fue posible inspeccionar el HTML, pero no aparecieron señales AdTech claras en la respuesta inicial. Si los anuncios cargan client-side, esta lectura es necesariamente limitada.",
    }


def build_findings(snapshot, analysis):
    findings = []

    if snapshot.get("available"):
        findings.append(f"HTTP {snapshot.get('status_code')} y HTML inspeccionable: {'sí' if bool(snapshot.get('html_excerpt')) else 'no'}.")
        findings.append(f"Tiempo de respuesta inicial: {snapshot.get('response_time_ms')} ms.")

    if analysis["matched_script_sources"]:
        findings.append("Scripts publicitarios detectados: " + ", ".join(analysis["matched_script_sources"]))
    else:
        findings.append("No se detectaron scripts publicitarios conocidos en los src visibles del HTML inicial.")

    findings.append(f"Cantidad estimada de slots o contenedores: {analysis['slot_count_estimate']}.")

    if analysis["slot_matches"]:
        findings.append("Patrones de slot visibles: " + ", ".join(analysis["slot_matches"][:4]))

    if analysis["matched_iframe_sources"]:
        findings.append("Iframes compatibles con publicidad: " + ", ".join(analysis["matched_iframe_sources"][:4]))

    if analysis["vendor_hits"]:
        findings.append("Vendors o wrappers detectados: " + ", ".join(analysis["vendor_hits"]))

    if analysis["raw_matches"]:
        findings.append("Patrones relevantes encontrados: " + ", ".join(analysis["raw_matches"][:6]))

    return findings[:7]


def build_opportunities(snapshot, analysis):
    opportunities = []
    detected_keys = {item["key"] for item in analysis["monetization_signals"] if item["status"] == "detected"}

    if not snapshot.get("available"):
        opportunities.append("Primero hace falta una lectura HTTP estable para inspeccionar el stack publicitario visible.")
        return opportunities

    if not detected_keys:
        opportunities.append("No se detecta un stack publicitario visible en la respuesta inicial.")
        opportunities.append("Si la página renderiza anuncios solo client-side, conviene una v2 con navegador o headless para validar la implementación real.")
    else:
        if "googletag" in detected_keys and analysis["slot_count_estimate"] == 0:
            opportunities.append("Hay señales de GPT sin slots claros en el HTML inicial; parte del stack podría montarse después del render.")
        if "prebid" in detected_keys and "googletag" not in detected_keys:
            opportunities.append("Se detectan bidder libraries sin GPT visible; conviene revisar si falta lectura del wrapper principal o si la carga es client-side.")
        if "advanced_behaviors" not in detected_keys and "googletag" in detected_keys:
            opportunities.append("No aparecieron señales visibles de refresh, lazy load o targeting en el HTML inicial.")
        if analysis["matched_script_sources"] and not analysis["matched_iframe_sources"]:
            opportunities.append("Hay scripts AdTech visibles pero no iframes detectables; eso puede indicar carga diferida o slots no resueltos en servidor.")

    if analysis["client_side_likely"]:
        opportunities.append("La implementación probablemente depende de render client-side para completar parte del stack publicitario.")

    return opportunities[:5] or ["La respuesta inicial no deja observaciones claras adicionales en esta versión."]


def build_recommendation(snapshot, analysis, opportunities):
    if not snapshot.get("available"):
        return "Hace falta estabilizar la URL y repetir el análisis. Sin una respuesta HTTP válida no hay forma de leer la capa AdTech inicial."

    detected_keys = {item["key"] for item in analysis["monetization_signals"] if item["status"] == "detected"}
    if detected_keys:
        return (
            f"La recomendación inicial es validar en navegador lo que el backend ya insinúa, empezando por {opportunities[0].lower()} "
            "Si esta capa sostiene monetización real, una v2 con render client-side y lectura de network requests va a dar una imagen más confiable."
        )

    return (
        "No hay stack publicitario visible en la respuesta inicial. Si la monetización existe, la siguiente capa técnica razonable es una inspección con navegador o headless para confirmar carga client-side."
    )


def build_limitations(snapshot, analysis):
    limitations = [
        "La detección ocurre sobre HTML descargado desde backend y no ejecuta JavaScript del lado del navegador.",
        "Una parte del stack publicitario puede montarse después del render o depender de eventos, consentimiento o viewport.",
    ]
    if analysis["client_side_likely"]:
        limitations.append("Las señales actuales sugieren que parte de la implementación podría completarse solo client-side.")
    if not snapshot.get("html_excerpt"):
        limitations.append("No hubo HTML útil para inspeccionar el DOM bruto con más detalle.")
    return limitations


def infer_client_side_limitation(snapshot, monetization_signals):
    if not snapshot.get("available"):
        return False

    has_script_sources = bool(snapshot.get("script_sources"))
    slot_count_detected = any(item["key"] == "googletag" and item["status"] == "detected" for item in monetization_signals)
    slot_hints = bool(snapshot.get("slot_hints"))

    return has_script_sources and slot_count_detected and not slot_hints


def _http_source_detail(snapshot):
    if snapshot.get("available"):
        return f"HTTP {snapshot.get('status_code')} en {snapshot.get('response_time_ms')} ms; content-type {snapshot.get('content_type')}."
    return "No se pudo obtener una respuesta válida desde backend."


def _pattern_source_detail(analysis):
    detected_count = sum(1 for item in analysis["monetization_signals"] if item["status"] == "detected")
    return f"Se detectaron {detected_count} señales positivas y {analysis['slot_count_estimate']} slots o hints estimados."


def _unique_preserve_order(items):
    seen = set()
    result = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def build_insight(snapshot, analysis):
    issues = []

    if not snapshot.get("available"):
        issues.append(
            build_insight_issue(
                "La URL no devolvió suficiente HTML como para inspeccionar señales de monetización.",
                penalty=70,
                impact="Alto",
                risk="Bloqueante",
                priority="Corregir ahora",
                areas=["Entrega"],
            )
        )
        return summarize_insight(
            issues,
            positive_summary="Todavía no hay una base AdTech visible para revisar.",
            context_label="entrega de monetización",
        )

    status_code = snapshot.get("status_code") or 0
    detected_keys = {item["key"] for item in analysis["monetization_signals"] if item["status"] == "detected"}
    signal_count = len(detected_keys)
    slot_count = analysis["slot_count_estimate"]
    script_count = len(analysis["matched_script_sources"])
    iframe_count = len(analysis["matched_iframe_sources"])

    if status_code >= 400:
        issues.append(
            build_insight_issue(
                f"HTTP {status_code} debilita la lectura AdTech en la capa de entrega.",
                penalty=55,
                impact="Alto",
                risk="Bloqueante",
                priority="Corregir ahora",
                areas=["Entrega"],
            )
        )

    if signal_count >= 2 and slot_count == 0:
        issues.append(
            build_insight_issue(
                "Hay señales AdTech fuertes sin una estructura clara de slots en el HTML inicial.",
                penalty=22,
                impact="Alto",
                risk="Alto",
                priority="Revisar pronto",
                areas=["Monetización", "Entrega"],
            )
        )

    if "prebid" in detected_keys and "googletag" not in detected_keys:
        issues.append(
            build_insight_issue(
                "Prebid es visible sin una estructura clara de GPT, así que el wrapper puede estar incompleto o existir solo del lado del cliente.",
                penalty=16,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["Monetización"],
            )
        )

    if script_count and not slot_count and not iframe_count:
        issues.append(
            build_insight_issue(
                "Hay scripts visibles, pero poca evidencia de slots en el HTML inicial.",
                penalty=12,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["Monetización", "Entrega"],
            )
        )

    if analysis["client_side_likely"]:
        issues.append(
            build_insight_issue(
                "El stack visible parece depender del lado del cliente, así que la evidencia desde backend sigue siendo parcial.",
                penalty=14,
                impact="Medio",
                risk="Medio",
                priority="Monitorear",
                areas=["Entrega", "Monetización"],
            )
        )

    if not signal_count:
        issues.append(
            build_insight_issue(
                "No hay señales de monetización visibles desde backend, así que esta lectura queda como informativa hasta confirmarla por otra vía.",
                penalty=5,
                impact="Bajo",
                risk="Bajo",
                priority="Monitorear",
                areas=["Monetización"],
            )
        )

    return summarize_insight(
        issues,
        positive_summary="La capa de monetización se ve estructuralmente legible desde la respuesta inicial del backend.",
        context_label="entrega de monetización",
    )


def build_exports(diagnosis, analysis, insight):
    finding_blocks = diagnosis["technical_findings"] + diagnosis["opportunities"] + diagnosis["limitations"]
    signal_lines = [
        f"{item['label']}: {'Detectado' if item['status'] == 'detected' else 'No visible'}"
        for item in diagnosis["monetization_signals"]
    ]
    evidence_lines = [
        f"Slots estimados: {analysis['slot_count_estimate']}",
        f"Scripts publicitarios: {len(analysis['matched_script_sources'])}",
        f"Iframes detectados: {len(analysis['matched_iframe_sources'])}",
        f"Vendors detectados: {len(analysis['vendor_hits'])}",
    ]

    return build_copy_exports(
        title="AdTech Debug Tool",
        summary=diagnosis["overview"]["summary"],
        findings=finding_blocks,
        recommendation=diagnosis["recommendation"],
        sections=[
            ("Señales de monetización", signal_lines),
            ("Hallazgos técnicos", diagnosis["technical_findings"]),
            ("Evidencia", evidence_lines),
            ("Observaciones", diagnosis["opportunities"]),
            ("Limitaciones", diagnosis["limitations"]),
        ],
        insight=insight,
    )
