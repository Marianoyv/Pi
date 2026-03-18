from .export_utils import build_copy_exports
from .insight_utils import build_insight_issue, summarize_insight


FORMAT_RULES = {
    "html5": {"label": "Display HTML5", "max_weight_kb": 200, "requires_click": True},
    "static": {"label": "Imagen estática", "max_weight_kb": 150, "requires_click": True},
    "video": {"label": "Video", "max_weight_kb": 5000, "requires_click": True},
    "native": {"label": "Nativo / social", "max_weight_kb": 300, "requires_click": True},
    "other": {"label": "Otro", "max_weight_kb": 300, "requires_click": False},
}

DEVICE_LABELS = {
    "desktop": "Escritorio",
    "mobile": "Móvil",
    "both": "Ambos",
}

CONTEXT_LABELS = {
    "safeframe": "SafeFrame",
    "friendly_iframe": "Friendly iframe",
    "unknown": "Desconocido",
}

SOUND_LABELS = {
    "none": "sin sonido",
    "user_action": "sonido tras interacción",
    "load": "sonido al cargar",
}

AUTOPLAY_LABELS = {
    "none": "sin reproducción automática",
    "muted": "reproducción automática en silencio",
    "sound_on": "reproducción automática con sonido",
}


def run_creative_qa(cleaned_data):
    checklist_items = build_checklist(cleaned_data)
    correct_points = [item["detail"] for item in checklist_items if item["status"] == "ok"]
    observations = [item["detail"] for item in checklist_items if item["status"] == "warn"]
    flags = [item["detail"] for item in checklist_items if item["status"] == "fail"]
    overview = build_overview(cleaned_data, checklist_items)
    insight = build_insight(checklist_items)
    recommendation = build_recommendation(overview["state"], flags, observations)

    return {
        "overview": overview,
        "insight": insight,
        "checklist_items": checklist_items,
        "correct_points": correct_points,
        "observations": observations,
        "flags": flags,
        "recommendation": recommendation,
        "exports": build_exports(overview, checklist_items, correct_points, observations, flags, recommendation, insight),
    }


def build_checklist(cleaned_data):
    rules = FORMAT_RULES[cleaned_data["format_type"]]
    items = []

    destination_url = cleaned_data.get("destination_url") or ""
    click_tag_present = cleaned_data["click_tag_present"] == "yes"
    tracking_urls_included = cleaned_data["tracking_urls_included"] == "yes"
    dimensions = cleaned_data.get("dimensions") or ""
    weight_kb = cleaned_data.get("weight_kb")
    autoplay_behavior = cleaned_data["autoplay_behavior"]
    sound_behavior = cleaned_data["sound_behavior"]
    serving_context = cleaned_data["serving_context"]

    items.append(_build_item("Nombre de la pieza", "ok", f"Nombre declarado: {cleaned_data['creative_name']}.")) 
    items.append(_build_item("Formato", "ok", f"Formato declarado: {rules['label']}.")) 

    if dimensions:
        items.append(_build_item("Dimensiones", "ok", f"Dimensiones declaradas: {dimensions}."))
    else:
        items.append(_build_item("Dimensiones", "warn", "Faltan dimensiones declaradas para esta pieza."))

    click_status, click_detail = evaluate_click_path(rules["requires_click"], click_tag_present, destination_url)
    items.append(_build_item("Ruta de clic", click_status, click_detail))

    if tracking_urls_included:
        items.append(_build_item("Tracking", "ok", "Se declararon URLs de tracking adicionales para la revisión."))
    else:
        items.append(_build_item("Tracking", "warn", "No se declararon URLs de tracking; conviene revisar la medición antes de publicar."))

    if weight_kb is None:
        items.append(_build_item("Peso", "warn", "No se informó el peso del asset."))
    else:
        items.append(_build_item("Peso", *evaluate_weight(weight_kb, rules["max_weight_kb"])))

    items.append(
        _build_item(
            "Dispositivo objetivo",
            "ok",
            f"Dispositivo declarado: {DEVICE_LABELS[cleaned_data['device_target']]}.",
        )
    )

    sound_status, sound_detail = evaluate_sound_and_autoplay(sound_behavior, autoplay_behavior)
    items.append(_build_item("Reproducción", sound_status, sound_detail))

    if serving_context == "unknown":
        items.append(
            _build_item(
                "Contexto de serving",
                "warn",
                "El contexto de serving sigue sin definir; conviene confirmar si corre en SafeFrame o friendly iframe.",
            )
        )
    else:
        items.append(
            _build_item(
                "Contexto de serving",
                "ok",
                f"Contexto declarado: {CONTEXT_LABELS[serving_context]}.",
            )
        )

    if cleaned_data.get("extra_notes"):
        items.append(_build_item("Notas", "ok", "Se agregaron notas operativas para la revisión."))
    else:
        items.append(_build_item("Notas", "muted", "No se agregaron notas extra en esta corrida."))

    return items


def evaluate_click_path(requires_click, click_tag_present, destination_url):
    if requires_click and not click_tag_present and not destination_url:
        return "fail", "No hay click tag ni URL de destino para un formato que normalmente necesita salida de clic."
    if requires_click and not click_tag_present:
        return "warn", "Hay URL de destino, pero falta confirmar el click tag en un formato clickable."
    if click_tag_present and not destination_url:
        return "warn", "Se marcó click tag, pero falta la URL de destino para revisar el destino final."
    if destination_url:
        return "ok", "URL de destino declarada y lista para revisión manual."
    return "muted", "No se informó URL de destino y el contexto no obliga clic de forma explícita."


def evaluate_weight(weight_kb, max_weight_kb):
    if weight_kb > max_weight_kb * 1.5:
        return "fail", f"Peso de {weight_kb} KB, muy por encima del umbral de {max_weight_kb} KB."
    if weight_kb > max_weight_kb:
        return "warn", f"Peso de {weight_kb} KB, por encima del umbral sugerido de {max_weight_kb} KB."
    return "ok", f"Peso dentro del umbral sugerido ({weight_kb} KB sobre un máximo de {max_weight_kb} KB)."


def evaluate_sound_and_autoplay(sound_behavior, autoplay_behavior):
    if autoplay_behavior == "sound_on":
        return "fail", "Se detectó reproducción automática con sonido; necesita corrección antes de aprobar."
    if sound_behavior == "load":
        return "fail", "El sonido inicia al cargar; conviene bloquear la pieza hasta corregir ese comportamiento."
    if autoplay_behavior == "muted":
        return "warn", "Hay reproducción automática en silencio; conviene validar la política del placement y el comportamiento esperado."
    if sound_behavior == "user_action":
        return "ok", "El sonido queda atado a la interacción del usuario."
    return "ok", f"Comportamiento declarado: {AUTOPLAY_LABELS[autoplay_behavior]} y {SOUND_LABELS[sound_behavior]}."


def build_overview(cleaned_data, checklist_items):
    fail_count = sum(1 for item in checklist_items if item["status"] == "fail")
    warn_count = sum(1 for item in checklist_items if item["status"] == "warn")
    ok_count = sum(1 for item in checklist_items if item["status"] == "ok")

    if fail_count:
        return {
            "state": "Bloqueada",
            "tone": "critical",
            "summary": (
                f"La pieza {cleaned_data['creative_name']} tiene {fail_count} bloqueo(s) y {warn_count} observación(es). "
                "Conviene corregir los puntos críticos antes de aprobar."
            ),
            "counts": {"ok": ok_count, "warn": warn_count, "fail": fail_count},
        }

    if warn_count:
        return {
            "state": "Revisión necesaria",
            "tone": "warn",
            "summary": (
                f"La pieza {cleaned_data['creative_name']} no tiene bloqueos directos, pero deja {warn_count} punto(s) a revisar antes de salir."
            ),
            "counts": {"ok": ok_count, "warn": warn_count, "fail": fail_count},
        }

    return {
        "state": "Lista",
        "tone": "good",
        "summary": (
            f"La pieza {cleaned_data['creative_name']} pasa esta lectura inicial con checks básicos consistentes y sin alertas fuertes."
        ),
        "counts": {"ok": ok_count, "warn": warn_count, "fail": fail_count},
    }


def build_recommendation(state, flags, observations):
    if state == "Bloqueada":
        return f"Prioridad inmediata: resolver {flags[0].lower()} Después conviene repetir la checklist para validar que no queden bloqueos activos."
    if state == "Revisión necesaria":
        return f"Revisar primero {observations[0].lower()} Si el asset entra a trafficking, conviene dejar este output como checklist de preflight."
    return "La pieza queda lista para avanzar a una revisión operativa final o a trafficking, manteniendo esta checklist como soporte de QA."


def _build_item(label, status, detail):
    return {
        "label": label,
        "status": status,
        "detail": detail,
    }


def build_insight(checklist_items):
    issues = []

    for item in checklist_items:
        label = item["label"]
        status = item["status"]
        detail = item["detail"]

        if label == "Ruta de clic" and status == "fail":
            issues.append(
                build_insight_issue(
                    detail,
                    penalty=30,
                    impact="Alto",
                    risk="Bloqueante",
                    priority="Corregir ahora",
                    areas=["Tracking", "Entrega"],
                )
            )
        elif label == "Ruta de clic" and status == "warn":
            issues.append(
                build_insight_issue(
                    detail,
                    penalty=16,
                    impact="Medio",
                    risk="Alto",
                    priority="Revisar pronto",
                    areas=["Tracking", "Entrega"],
                )
            )
        elif label == "Tracking" and status == "warn":
            issues.append(
                build_insight_issue(
                    detail,
                    penalty=10,
                    impact="Medio",
                    risk="Medio",
                    priority="Revisar pronto",
                    areas=["Tracking", "QA"],
                )
            )
        elif label == "Dimensiones" and status == "warn":
            issues.append(
                build_insight_issue(
                    detail,
                    penalty=12,
                    impact="Medio",
                    risk="Medio",
                    priority="Revisar pronto",
                    areas=["Entrega", "QA"],
                )
            )
        elif label == "Peso" and status == "fail":
            issues.append(
                build_insight_issue(
                    detail,
                    penalty=24,
                    impact="Alto",
                    risk="Alto",
                    priority="Corregir ahora",
                    areas=["Entrega", "QA"],
                )
            )
        elif label == "Peso" and status == "warn":
            issues.append(
                build_insight_issue(
                    detail,
                    penalty=12,
                    impact="Medio",
                    risk="Medio",
                    priority="Revisar pronto",
                    areas=["Entrega", "QA"],
                )
            )
        elif label == "Reproducción" and status == "fail":
            issues.append(
                build_insight_issue(
                    detail,
                    penalty=30,
                    impact="Alto",
                    risk="Bloqueante",
                    priority="Corregir ahora",
                    areas=["QA", "UX"],
                )
            )
        elif label == "Reproducción" and status == "warn":
            issues.append(
                build_insight_issue(
                    detail,
                    penalty=15,
                    impact="Medio",
                    risk="Alto",
                    priority="Revisar pronto",
                    areas=["QA", "UX"],
                )
            )
        elif label == "Contexto de serving" and status == "warn":
            issues.append(
                build_insight_issue(
                    detail,
                    penalty=8,
                    impact="Bajo",
                    risk="Bajo",
                    priority="Monitorear",
                    areas=["Entrega"],
                )
            )

    return summarize_insight(
        issues,
        positive_summary="La pieza pasa esta base de QA sin issues de alta prioridad.",
        context_label="entrega creativa",
    )


def build_exports(overview, checklist_items, correct_points, observations, flags, recommendation, insight):
    checklist_lines = [f"{item['label']}: {item['detail']}" for item in checklist_items]
    finding_lines = flags + observations

    return build_copy_exports(
        title="Creative QA Checklist",
        summary=overview["summary"],
        findings=finding_lines or correct_points,
        recommendation=recommendation,
        sections=[
            ("Estado", [overview["state"]]),
            ("Checklist", checklist_lines),
            ("Puntos correctos", correct_points),
            ("Observaciones", observations),
            ("Alertas", flags),
        ],
        insight=insight,
    )
