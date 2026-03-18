from .export_utils import build_copy_exports
from .http_snapshot import fetch_site_snapshot
from .insight_utils import build_insight_issue, summarize_insight


RESPONSE_TIME_WARN_MS = 1200
RESPONSE_TIME_CRITICAL_MS = 2500


def run_landing_performance_snapshot(url):
    snapshot = fetch_site_snapshot(url)
    diagnosis = build_diagnosis(url, snapshot)
    insight = build_insight(snapshot)
    sources = build_sources(snapshot)

    return {
        "target_url": url,
        "snapshot": snapshot,
        "diagnosis": diagnosis,
        "insight": insight,
        "sources": sources,
        "exports": build_exports(diagnosis, insight),
    }


def build_diagnosis(url, snapshot):
    quick_signals = build_quick_signals(snapshot)
    return {
        "target_url": url,
        "overview": build_overview(snapshot, quick_signals),
        "status_items": build_status_items(snapshot),
        "structure_items": build_structure_items(snapshot),
        "quick_signals": quick_signals,
        "summary": build_summary(snapshot, quick_signals),
        "recommendation": build_recommendation(snapshot, quick_signals),
    }


def build_overview(snapshot, quick_signals):
    if not snapshot.get("available"):
        return {
            "label": "Lectura no disponible",
            "tone": "critical",
            "summary": "No se pudo obtener la URL desde backend. Sin respuesta válida no hay snapshot técnico para esta landing.",
        }

    fail_count = sum(1 for signal in quick_signals if signal["status"] == "fail")
    warn_count = sum(1 for signal in quick_signals if signal["status"] == "warn")

    if snapshot.get("status_code") and snapshot["status_code"] >= 400:
        return {
            "label": "Respuesta inestable",
            "tone": "critical",
            "summary": "La landing respondió con un estado HTTP problemático. Conviene estabilizar la respuesta antes de revisar detalles finos.",
        }

    if fail_count or warn_count >= 3:
        return {
            "label": "Base útil con varias fricciones",
            "tone": "warn",
            "summary": "La landing se pudo leer, pero el snapshot deja varias señales básicas a corregir para mejorar control técnico y legibilidad.",
        }

    if warn_count:
        return {
            "label": "Base legible con ajustes puntuales",
            "tone": "warn",
            "summary": "La landing responde y deja una lectura técnica rápida. Hay algunos puntos puntuales para revisar antes de seguir optimizando.",
        }

    return {
        "label": "Snapshot limpio",
        "tone": "good",
        "summary": "La landing responde, expone la estructura básica esperable y no deja alertas claras en esta lectura corta.",
    }


def build_status_items(snapshot):
    if not snapshot.get("available"):
        return [
            {"label": "Estado HTTP", "value": "No disponible"},
            {"label": "Tiempo de respuesta", "value": "No disponible"},
            {"label": "URL final", "value": "No disponible"},
        ]

    final_url = snapshot.get("final_url") or "No detectada"
    if not snapshot.get("redirected"):
        final_url = "Sin redirect visible"

    return [
        {"label": "Estado HTTP", "value": str(snapshot.get("status_code") or "No disponible")},
        {"label": "Tiempo de respuesta", "value": f"{snapshot.get('response_time_ms')} ms"},
        {"label": "URL final", "value": final_url},
    ]


def build_structure_items(snapshot):
    return [
        {"label": "Title", "value": _display_value(snapshot.get("title"), "No detectado")},
        {"label": "Meta description", "value": _display_value(snapshot.get("meta_description"), "No detectada")},
        {"label": "Canonical", "value": _display_value(snapshot.get("canonical"), "No detectada")},
        {"label": "Robots", "value": _display_value(snapshot.get("robots"), "No detectado")},
        {"label": "Cantidad de H1", "value": str(snapshot.get("h1_count") or 0)},
    ]


def build_quick_signals(snapshot):
    if not snapshot.get("available"):
        return [
            {
                "label": "Lectura HTML",
                "status": "fail",
                "detail": "No fue posible descargar HTML útil desde backend para construir el snapshot.",
            }
        ]

    robots_value = (snapshot.get("robots") or "").lower()
    response_time_ms = snapshot.get("response_time_ms") or 0
    return [
        _signal(
            "Title",
            "warn" if not snapshot.get("title") else "ok",
            "Falta title en el HTML recibido." if not snapshot.get("title") else "Title detectado en la respuesta inicial.",
        ),
        _signal(
            "Meta description",
            "warn" if not snapshot.get("meta_description") else "ok",
            "Falta meta description en la respuesta inicial."
            if not snapshot.get("meta_description")
            else "Meta description detectada.",
        ),
        _signal(
            "Canonical",
            "warn" if not snapshot.get("canonical") else "ok",
            "No se detectó canonical en esta lectura."
            if not snapshot.get("canonical")
            else "Canonical detectada.",
        ),
        _signal(
            "Jerarquía H1",
            "warn" if snapshot.get("h1_count", 0) == 0 or snapshot.get("h1_count", 0) > 1 else "ok",
            _h1_detail(snapshot.get("h1_count", 0)),
        ),
        _signal(
            "Robots",
            "warn" if _is_restrictive_robots(robots_value) else "ok",
            "Robots incluye una directiva restrictiva."
            if _is_restrictive_robots(robots_value)
            else "Sin directivas robots restrictivas visibles.",
        ),
        _signal(
            "Tiempo de respuesta",
            _response_time_status(response_time_ms),
            _response_time_detail(response_time_ms),
        ),
    ]


def build_summary(snapshot, quick_signals):
    if not snapshot.get("available"):
        return "No hubo respuesta válida para construir el snapshot técnico."

    active_signals = [signal["detail"] for signal in quick_signals if signal["status"] in {"warn", "fail"}]
    if not active_signals:
        return "La landing deja una base corta y legible: responde bien, muestra metadata central y no expone alertas claras en esta primera pasada."

    summary_items = "; ".join(active_signals[:3])
    return f"Snapshot rápido: {summary_items}"


def build_recommendation(snapshot, quick_signals):
    if not snapshot.get("available"):
        return "Primero hace falta que la URL responda de forma estable. Después conviene repetir el snapshot para revisar metadata y tiempos."

    priority_signal = next((signal for signal in quick_signals if signal["status"] in {"fail", "warn"}), None)
    if not priority_signal:
        return "La landing queda bien parada para esta lectura corta. Si hace falta más profundidad, el siguiente paso natural es correr AI Auditor."

    return (
        f"Prioridad sugerida: resolver {priority_signal['detail'].lower()} "
        "Después conviene repetir este snapshot o escalar a AI Auditor si necesitas una lectura más completa."
    )


def build_sources(snapshot):
    return [
        {
            "label": "Snapshot HTTP",
            "status": "ok" if snapshot.get("available") else "limited",
            "detail": _snapshot_source_detail(snapshot),
        },
        {
            "label": "Reglas rápidas",
            "status": "ok" if snapshot.get("available") else "limited",
            "detail": "Aplica chequeos simples sobre metadata, H1, robots y tiempo de respuesta sin sumar capas externas.",
        },
    ]


def _is_restrictive_robots(robots_value):
    return any(token in robots_value for token in ("noindex", "nofollow", "none", "noarchive"))


def _response_time_status(response_time_ms):
    if response_time_ms >= RESPONSE_TIME_CRITICAL_MS:
        return "fail"
    if response_time_ms >= RESPONSE_TIME_WARN_MS:
        return "warn"
    return "ok"


def _response_time_detail(response_time_ms):
    if response_time_ms >= RESPONSE_TIME_CRITICAL_MS:
        return f"Tiempo de respuesta alto para una lectura rápida: {response_time_ms} ms."
    if response_time_ms >= RESPONSE_TIME_WARN_MS:
        return f"Tiempo de respuesta mejorable: {response_time_ms} ms."
    return f"Tiempo de respuesta dentro de una lectura razonable: {response_time_ms} ms."


def _h1_detail(h1_count):
    if h1_count == 0:
        return "No se detectó ningún H1 en la respuesta inicial."
    if h1_count > 1:
        return f"Se detectaron {h1_count} H1; conviene revisar la jerarquía."
    return "Jerarquía H1 simple y legible."


def _snapshot_source_detail(snapshot):
    if snapshot.get("available"):
        return f"HTTP {snapshot.get('status_code')} en {snapshot.get('response_time_ms')} ms."
    return "No se pudo obtener una respuesta válida desde backend."


def _display_value(value, fallback):
    return value or fallback


def _signal(label, status, detail):
    return {
        "label": label,
        "status": status,
        "detail": detail,
    }


def build_insight(snapshot):
    issues = []

    if not snapshot.get("available"):
        issues.append(
            build_insight_issue(
                "La URL no devolvió HTML útil para construir el snapshot.",
                penalty=70,
                impact="Alto",
                risk="Bloqueante",
                priority="Corregir ahora",
                areas=["Entrega"],
            )
        )
        return summarize_insight(
            issues,
            positive_summary="Todavía no hay una base suficiente para este snapshot.",
            context_label="base de la landing",
        )

    status_code = snapshot.get("status_code") or 0
    response_time_ms = snapshot.get("response_time_ms") or 0
    robots_value = (snapshot.get("robots") or "").lower()
    h1_count = snapshot.get("h1_count") or 0

    if status_code >= 400:
        issues.append(
            build_insight_issue(
                f"HTTP {status_code} vuelve inestable la landing para esta revisión.",
                penalty=55,
                impact="Alto",
                risk="Bloqueante",
                priority="Corregir ahora",
                areas=["Entrega"],
            )
        )
    if not snapshot.get("title"):
        issues.append(
            build_insight_issue(
                "Falta el title y eso reduce la claridad de la página para los buscadores.",
                penalty=16,
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
                penalty=12,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["SEO"],
            )
        )
    if not snapshot.get("canonical"):
        issues.append(
            build_insight_issue(
                "La canonical no aparece en el HTML inicial.",
                penalty=8,
                impact="Bajo",
                risk="Bajo",
                priority="Monitorear",
                areas=["SEO"],
            )
        )
    if h1_count == 0:
        issues.append(
            build_insight_issue(
                "No se detectó ningún H1 en el HTML inicial.",
                penalty=12,
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
    if any(token in robots_value for token in ("noindex", "nofollow", "none", "noarchive")):
        issues.append(
            build_insight_issue(
                "La directiva robots expone una restricción en la respuesta inicial.",
                penalty=15,
                impact="Alto",
                risk="Alto",
                priority="Revisar pronto",
                areas=["SEO", "Entrega"],
            )
        )
    if response_time_ms >= RESPONSE_TIME_CRITICAL_MS:
        issues.append(
            build_insight_issue(
                f"La respuesta base es alta: {response_time_ms} ms.",
                penalty=18,
                impact="Alto",
                risk="Alto",
                priority="Corregir ahora",
                areas=["Rendimiento"],
            )
        )
    elif response_time_ms >= RESPONSE_TIME_WARN_MS:
        issues.append(
            build_insight_issue(
                f"La respuesta base es aceptable, pero todavía alta: {response_time_ms} ms.",
                penalty=10,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["Rendimiento"],
            )
        )

    return summarize_insight(
        issues,
        positive_summary="La base de la landing es limpia para este snapshot rápido.",
        context_label="base de la landing",
    )


def build_exports(diagnosis, insight):
    return build_copy_exports(
        title="Landing Performance Snapshot",
        summary=diagnosis["summary"],
        findings=[item["detail"] for item in diagnosis["quick_signals"]],
        recommendation=diagnosis["recommendation"],
        sections=[
            ("Estado", [f"{item['label']}: {item['value']}" for item in diagnosis["status_items"]]),
            ("Estructura", [f"{item['label']}: {item['value']}" for item in diagnosis["structure_items"]]),
            ("Señales rápidas", [f"{item['label']}: {item['detail']}" for item in diagnosis["quick_signals"]]),
        ],
        insight=insight,
    )
