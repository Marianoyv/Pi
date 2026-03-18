from .export_utils import build_copy_exports
from .http_snapshot import fetch_site_snapshot
from .insight_utils import build_insight_issue, summarize_insight
from .openai_summary import generate_ai_summary
from .pagespeed import run_pagespeed_audit


def run_ai_auditor(url):
    snapshot = fetch_site_snapshot(url)
    pagespeed = run_pagespeed_audit(url)
    diagnosis = build_diagnosis(url, snapshot, pagespeed)
    insight = build_insight(snapshot, pagespeed)
    ai_summary = generate_ai_summary(diagnosis)
    sources = build_sources(snapshot, pagespeed, ai_summary)

    return {
        "target_url": url,
        "snapshot": snapshot,
        "pagespeed": pagespeed,
        "diagnosis": diagnosis,
        "insight": insight,
        "ai_summary": ai_summary,
        "sources": sources,
        "exports": build_exports(diagnosis, ai_summary, insight),
    }


def build_diagnosis(url, snapshot, pagespeed):
    overview = build_overview(snapshot, pagespeed)
    technical_observations = build_technical_observations(snapshot, pagespeed)
    performance = build_performance_section(snapshot, pagespeed)
    seo = build_seo_section(snapshot, pagespeed)
    opportunities = build_opportunities(snapshot, pagespeed)
    recommendation = build_recommendation(snapshot, pagespeed, opportunities)

    return {
        "target_url": url,
        "overview": overview,
        "technical_observations": technical_observations,
        "performance": performance,
        "seo": seo,
        "opportunities": opportunities,
        "recommendation": recommendation,
    }


def build_sources(snapshot, pagespeed, ai_summary):
    return [
        {
            "label": "Snapshot HTTP",
            "status": "ok" if snapshot.get("available") else "limited",
            "detail": _snapshot_source_detail(snapshot),
        },
        {
            "label": "PageSpeed Insights",
            "status": "ok" if pagespeed.get("available") else "limited",
            "detail": pagespeed.get("message") or "PageSpeed devolvió datos de rendimiento y SEO.",
        },
        {
            "label": "Capa de OpenAI",
            "status": "ok" if ai_summary.get("available") else "limited",
            "detail": ai_summary.get("message"),
        },
    ]


def build_overview(snapshot, pagespeed):
    if not snapshot.get("available"):
        return {
            "label": "Análisis parcial",
            "tone": "critical",
            "summary": "No se pudo leer la URL desde backend. La estructura del auditor queda lista, pero el sitio no respondió para una lectura técnica inicial.",
        }

    performance_score = (pagespeed.get("categories") or {}).get("performance")
    seo_score = (pagespeed.get("categories") or {}).get("seo")
    has_core_seo_gaps = not snapshot.get("title") or not snapshot.get("meta_description")

    if performance_score is not None and seo_score is not None and performance_score >= 80 and seo_score >= 80 and not has_core_seo_gaps:
        return {
            "label": "Base saludable",
            "tone": "good",
            "summary": "La URL responde, la base técnica es legible y las señales principales no muestran fricciones severas en esta primera lectura.",
        }

    if snapshot.get("status_code") and snapshot["status_code"] >= 400:
        return {
            "label": "Base inestable",
            "tone": "critical",
            "summary": "La URL devolvió un estado HTTP problemático. Antes de optimizar, conviene estabilizar la respuesta y revisar acceso, redirects o contenido publicado.",
        }

    return {
        "label": "Base útil con mejoras claras",
        "tone": "warn",
        "summary": "La URL se pudo leer y la herramienta encontró una base operativa, pero hay señales técnicas o SEO que conviene corregir para mejorar calidad y control.",
    }


def build_technical_observations(snapshot, pagespeed):
    observations = []

    if snapshot.get("available"):
        observations.append(f"HTTP {snapshot.get('status_code')} y respuesta inicial en {snapshot.get('response_time_ms')} ms.")
        observations.append(
            "La URL final coincide con la enviada."
            if not snapshot.get("redirected")
            else f"La URL termina resolviendo en {snapshot.get('final_url')}."
        )
        observations.append(
            "El sitio responde sobre HTTPS."
            if snapshot.get("https")
            else "La URL no usa HTTPS, lo que conviene corregir."
        )
        observations.append(
            "Se detectó una etiqueta title."
            if snapshot.get("title")
            else "No se detectó una etiqueta title clara en el HTML recibido."
        )
        observations.append(
            "Se detectó meta description."
            if snapshot.get("meta_description")
            else "No se detectó meta description en el HTML recibido."
        )
        if not snapshot.get("canonical"):
            observations.append("No se detectó canonical link en esta lectura básica.")
        if snapshot.get("h1_count") == 0:
            observations.append("No se detectó ningún H1 en la página analizada.")
        elif snapshot.get("h1_count") > 1:
            observations.append(f"Se detectaron {snapshot.get('h1_count')} H1; conviene revisar la jerarquía.")
    else:
        observations.append("No fue posible obtener una lectura básica del sitio desde backend.")

    if pagespeed.get("available"):
        performance_score = (pagespeed.get("categories") or {}).get("performance")
        seo_score = (pagespeed.get("categories") or {}).get("seo")
        if performance_score is not None:
            observations.append(f"PageSpeed reportó rendimiento mobile de {performance_score}/100.")
        if seo_score is not None:
            observations.append(f"PageSpeed reportó SEO básico de {seo_score}/100.")
    else:
        observations.append("PageSpeed Insights no estuvo disponible; el diagnóstico usa snapshot técnico y deja la estructura lista para enriquecer después.")

    return observations[:6]


def build_performance_section(snapshot, pagespeed):
    items = []
    status_label = "Lectura básica"
    tone = "warn"

    if pagespeed.get("available"):
        performance_score = (pagespeed.get("categories") or {}).get("performance")
        if performance_score is not None:
            items.append({"label": "PageSpeed mobile", "value": f"{performance_score}/100"})
            if performance_score >= 80:
                status_label = "Rendimiento saludable"
                tone = "good"
            elif performance_score < 50:
                status_label = "Rendimiento frágil"
                tone = "critical"
            else:
                status_label = "Rendimiento mejorable"
        items.extend(pagespeed.get("metrics") or [])
    elif snapshot.get("available"):
        items.append({"label": "Respuesta inicial", "value": f"{snapshot.get('response_time_ms')} ms"})
        items.append({"label": "Fuente", "value": "Snapshot HTTP básico"})
        status_label = "Sin laboratorio externo"

    if not items:
        items.append({"label": "Estado", "value": "No disponible en esta ejecución"})
        status_label = "Sin datos"
        tone = "critical"

    return {
        "label": status_label,
        "tone": tone,
        "items": items,
        "note": "Si PageSpeed no responde, el auditor mantiene una lectura básica sin inventar datos.",
    }


def build_seo_section(snapshot, pagespeed):
    items = []
    score = (pagespeed.get("categories") or {}).get("seo")
    tone = "warn"
    label = "SEO básico"

    if score is not None:
        items.append({"label": "Score PageSpeed", "value": f"{score}/100"})
        if score >= 80:
            tone = "good"
            label = "SEO básico consistente"
        elif score < 50:
            tone = "critical"
            label = "SEO básico frágil"
        items.extend(pagespeed.get("seo_checks") or [])

    if snapshot.get("available"):
        items.extend(
            [
                {"label": "Title", "value": "Detectado" if snapshot.get("title") else "Falta o no se pudo leer"},
                {
                    "label": "Meta description",
                    "value": "Detectada" if snapshot.get("meta_description") else "Falta o no se pudo leer",
                },
                {"label": "Canonical", "value": "Detectada" if snapshot.get("canonical") else "No detectada"},
                {"label": "H1", "value": str(snapshot.get("h1_count") or 0)},
            ]
        )

    if not items:
        items.append({"label": "Estado", "value": "No disponible en esta ejecución"})
        tone = "critical"
        label = "Sin datos"

    return {
        "label": label,
        "tone": tone,
        "items": items[:8],
        "note": "La lectura SEO combina checks básicos del HTML con datos de PageSpeed cuando están disponibles.",
    }


def build_opportunities(snapshot, pagespeed):
    opportunities = []

    if pagespeed.get("available"):
        opportunities.extend(
            item["label"] + (f" ({item['value']})" if item.get("value") else "")
            for item in pagespeed.get("opportunities") or []
        )

    if snapshot.get("available"):
        if not snapshot.get("title"):
            opportunities.append("Agregar o revisar la etiqueta title.")
        if not snapshot.get("meta_description"):
            opportunities.append("Agregar o revisar meta description.")
        if not snapshot.get("canonical"):
            opportunities.append("Definir canonical si la página necesita una URL canónica explícita.")
        if snapshot.get("h1_count", 0) > 1:
            opportunities.append("Reducir la cantidad de H1 para ordenar la jerarquía.")

    if not opportunities:
        opportunities.append("No se detectaron oportunidades claras en esta primera lectura.")

    return opportunities[:5]


def build_recommendation(snapshot, pagespeed, opportunities):
    if not snapshot.get("available"):
        return "Primero hace falta asegurar que la URL responda de forma estable. Después conviene reintentar el auditor con PageSpeed operativo para una lectura más completa."

    performance_score = (pagespeed.get("categories") or {}).get("performance")
    seo_score = (pagespeed.get("categories") or {}).get("seo")

    if performance_score is not None and seo_score is not None:
        return (
            f"Prioridad sugerida: estabilizar los puntos con mayor impacto visible, empezando por {opportunities[0].lower()} "
            "Si esta URL forma parte de una capa comercial o editorial, conviene medir de nuevo después de cada ajuste."
        )

    return (
        "La primera recomendación es completar la base técnica más obvia del HTML y después habilitar una capa externa como "
        "PageSpeed para validar rendimiento y SEO con más precisión."
    )


def _snapshot_source_detail(snapshot):
    if snapshot.get("available"):
        return f"HTTP {snapshot.get('status_code')} en {snapshot.get('response_time_ms')} ms."
    return "No se pudo obtener una respuesta válida desde backend."


def build_insight(snapshot, pagespeed):
    issues = []

    if not snapshot.get("available"):
        issues.append(
            build_insight_issue(
                "La URL no respondió desde backend, así que no hay una base técnica confiable para auditar.",
                penalty=75,
                impact="Alto",
                risk="Bloqueante",
                priority="Corregir ahora",
                areas=["Entrega"],
            )
        )
        return summarize_insight(
            issues,
            positive_summary="No hay suficiente lectura para construir una priorización técnica.",
            context_label="base técnica",
        )

    status_code = snapshot.get("status_code") or 0
    response_time_ms = snapshot.get("response_time_ms") or 0
    performance_score = (pagespeed.get("categories") or {}).get("performance")
    seo_score = (pagespeed.get("categories") or {}).get("seo")

    if status_code >= 400:
        issues.append(
            build_insight_issue(
                f"HTTP {status_code} rompe la lectura base de la URL.",
                penalty=55,
                impact="Alto",
                risk="Bloqueante",
                priority="Corregir ahora",
                areas=["Entrega"],
            )
        )
    if not snapshot.get("https"):
        issues.append(
            build_insight_issue(
                "La URL no usa HTTPS.",
                penalty=15,
                impact="Medio",
                risk="Alto",
                priority="Revisar pronto",
                areas=["Entrega"],
            )
        )
    if response_time_ms >= 2500:
        issues.append(
            build_insight_issue(
                f"La respuesta base es alta: {response_time_ms} ms.",
                penalty=22,
                impact="Alto",
                risk="Alto",
                priority="Corregir ahora",
                areas=["Rendimiento"],
            )
        )
    elif response_time_ms >= 1200:
        issues.append(
            build_insight_issue(
                f"La respuesta base es mejorable: {response_time_ms} ms.",
                penalty=12,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["Rendimiento"],
            )
        )
    if not snapshot.get("title"):
        issues.append(
            build_insight_issue(
                "Falta el title y eso reduce la claridad para buscadores y listados.",
                penalty=14,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["SEO"],
            )
        )
    if not snapshot.get("meta_description"):
        issues.append(
            build_insight_issue(
                "Falta la meta description y eso reduce el control del snippet.",
                penalty=10,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["SEO"],
            )
        )
    if not snapshot.get("canonical"):
        issues.append(
            build_insight_issue(
                "La canonical no es visible en el HTML inicial.",
                penalty=8,
                impact="Bajo",
                risk="Bajo",
                priority="Monitorear",
                areas=["SEO"],
            )
        )

    h1_count = snapshot.get("h1_count") or 0
    if h1_count == 0:
        issues.append(
            build_insight_issue(
                "No se detectó ningún H1 en el HTML inicial.",
                penalty=10,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["SEO", "UX"],
            )
        )
    elif h1_count > 1:
        issues.append(
            build_insight_issue(
                f"{h1_count} etiquetas H1 reducen la claridad de la jerarquía.",
                penalty=10,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["SEO", "UX"],
            )
        )

    if performance_score is not None:
        if performance_score < 50:
            issues.append(
                build_insight_issue(
                    f"El puntaje de rendimiento es bajo: {performance_score}/100.",
                    penalty=24,
                    impact="Alto",
                    risk="Alto",
                    priority="Corregir ahora",
                    areas=["Rendimiento"],
                )
            )
        elif performance_score < 80:
            issues.append(
                build_insight_issue(
                    f"El puntaje de rendimiento es aceptable, pero no sólido: {performance_score}/100.",
                    penalty=12,
                    impact="Medio",
                    risk="Medio",
                    priority="Revisar pronto",
                    areas=["Rendimiento"],
                )
            )

    if seo_score is not None:
        if seo_score < 50:
            issues.append(
                build_insight_issue(
                    f"El puntaje de SEO es bajo: {seo_score}/100.",
                    penalty=18,
                    impact="Alto",
                    risk="Alto",
                    priority="Revisar pronto",
                    areas=["SEO"],
                )
            )
        elif seo_score < 80:
            issues.append(
                build_insight_issue(
                    f"El puntaje de SEO es aceptable, pero todavía deja margen claro de mejora: {seo_score}/100.",
                    penalty=10,
                    impact="Medio",
                    risk="Medio",
                    priority="Revisar pronto",
                    areas=["SEO"],
                )
            )

    return summarize_insight(
        issues,
        positive_summary="La base técnica es sólida para esta auditoría de primera pasada.",
        context_label="base técnica",
    )


def build_exports(diagnosis, ai_summary, insight):
    findings = diagnosis["technical_observations"] + diagnosis["opportunities"]
    if ai_summary.get("available") and ai_summary.get("text"):
        findings = [ai_summary["text"]] + findings

    return build_copy_exports(
        title="AI Auditor",
        summary=diagnosis["overview"]["summary"],
        findings=findings,
        recommendation=diagnosis["recommendation"],
        sections=[
            ("Observaciones técnicas", diagnosis["technical_observations"]),
            ("Rendimiento", [f"{item['label']}: {item['value']}" for item in diagnosis["performance"]["items"]]),
            ("SEO", [f"{item['label']}: {item['value']}" for item in diagnosis["seo"]["items"]]),
            ("Oportunidades", diagnosis["opportunities"]),
        ],
        insight=insight,
    )
