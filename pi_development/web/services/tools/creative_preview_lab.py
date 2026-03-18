import re
from html.parser import HTMLParser
from urllib.parse import urlparse

from .export_utils import build_copy_exports
from .insight_utils import build_insight_issue, summarize_insight


CREATIVE_TYPE_LABELS = {
    "display": "Display",
    "third_party": "Tag de terceros",
    "rich_media": "Rich media",
    "other": "Otro",
}

INPUT_MODE_LABELS = {
    "html": "Creatividad HTML",
    "third_party": "Tag de terceros",
}

MACRO_PATTERNS = (
    re.compile(r"%%[A-Z0-9_]+%%", re.IGNORECASE),
    re.compile(r"\{\{[^}]+\}\}"),
    re.compile(r"\$\{[^}]+\}"),
    re.compile(r"\[\[?[A-Z0-9_]+\]?\]", re.IGNORECASE),
    re.compile(r"\bclicktag\b", re.IGNORECASE),
)

FRAME_BUSTING_PATTERNS = (
    re.compile(r"top\.location", re.IGNORECASE),
    re.compile(r"parent\.location", re.IGNORECASE),
    re.compile(r"window\.top", re.IGNORECASE),
    re.compile(r"window\.parent", re.IGNORECASE),
    re.compile(r"document\.location", re.IGNORECASE),
)

PLACEHOLDER_PATTERNS = (
    re.compile(r"replace[_ -]?me", re.IGNORECASE),
    re.compile(r"todo", re.IGNORECASE),
    re.compile(r"example\.com", re.IGNORECASE),
    re.compile(r"your[-_ ]?click[-_ ]?url", re.IGNORECASE),
)


class CreativeMarkupParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.script_count = 0
        self.iframe_count = 0
        self.link_count = 0
        self.media_count = 0
        self.autoplay_count = 0
        self.audio_count = 0
        self.video_count = 0
        self.inline_handler_count = 0
        self.external_assets = []
        self.script_sources = []
        self.iframe_sources = []
        self.anchor_targets = []

    def handle_starttag(self, tag, attrs):
        attrs_map = {key.lower(): value for key, value in attrs}
        attr_names = {key.lower() for key, _ in attrs}

        if tag == "script":
            self.script_count += 1
            src = attrs_map.get("src") or ""
            if src:
                self.script_sources.append(src)
                self._collect_external(src)
        elif tag == "iframe":
            self.iframe_count += 1
            src = attrs_map.get("src") or ""
            if src:
                self.iframe_sources.append(src)
                self._collect_external(src)
        elif tag == "a":
            self.link_count += 1
            href = attrs_map.get("href") or ""
            if href:
                self.anchor_targets.append(href)
                self._collect_external(href)

        if tag in {"video", "audio"}:
            self.media_count += 1
            if tag == "video":
                self.video_count += 1
            if tag == "audio":
                self.audio_count += 1
            if "autoplay" in attr_names:
                self.autoplay_count += 1

        if tag == "source":
            src = attrs_map.get("src") or ""
            if src:
                self._collect_external(src)

        if tag in {"img", "link"}:
            ref = attrs_map.get("src") or attrs_map.get("href") or ""
            if ref:
                self._collect_external(ref)

        for attr_name in attr_names:
            if attr_name.startswith("on"):
                self.inline_handler_count += 1

    def _collect_external(self, reference):
        if not reference:
            return
        if reference.startswith(("http://", "https://", "//")):
            self.external_assets.append(reference)


def run_creative_preview_lab(cleaned_data):
    code = cleaned_data.get("code", "")
    parser = analyze_markup(code)
    macro_hits = find_pattern_hits(code, MACRO_PATTERNS)
    placeholder_hits = find_pattern_hits(code, PLACEHOLDER_PATTERNS)
    blocked_hits = find_pattern_hits(code, FRAME_BUSTING_PATTERNS)

    detected = build_detected_elements(parser, macro_hits, placeholder_hits)
    preview = build_preview(cleaned_data, parser, macro_hits, blocked_hits)
    technical_flags = build_technical_flags(cleaned_data, parser, macro_hits, placeholder_hits, blocked_hits)
    qa_observations = build_qa_observations(cleaned_data, parser, macro_hits, placeholder_hits, preview)
    limitations = build_limitations(cleaned_data, parser, preview)
    insight = build_insight(cleaned_data, parser, macro_hits, placeholder_hits, preview)
    recommendation = build_recommendation(preview, technical_flags, qa_observations)

    return {
        "preview": preview,
        "insight": insight,
        "detected_elements": detected,
        "technical_flags": technical_flags,
        "qa_observations": qa_observations,
        "limitations": limitations,
        "recommendation": recommendation,
        "exports": build_exports(preview, detected, technical_flags, qa_observations, limitations, recommendation, insight),
    }


def analyze_markup(code):
    parser = CreativeMarkupParser()
    if code:
        parser.feed(code)
    return parser


def build_detected_elements(parser, macro_hits, placeholder_hits):
    return [
        {
            "label": "Scripts",
            "count": parser.script_count,
            "detail": build_count_detail(parser.script_count, parser.script_sources, "etiquetas script"),
        },
        {
            "label": "Iframes",
            "count": parser.iframe_count,
            "detail": build_count_detail(parser.iframe_count, parser.iframe_sources, "iframes"),
        },
        {
            "label": "Links",
            "count": parser.link_count,
            "detail": build_count_detail(parser.link_count, parser.anchor_targets, "enlaces"),
        },
        {
            "label": "Recursos externos",
            "count": len(unique_preserve_order(parser.external_assets)),
            "detail": build_external_detail(parser.external_assets),
        },
        {
            "label": "Etiquetas multimedia",
            "count": parser.media_count,
            "detail": build_media_detail(parser),
        },
        {
            "label": "Macros / placeholders",
            "count": len(unique_preserve_order(macro_hits + placeholder_hits)),
            "detail": build_macro_detail(macro_hits, placeholder_hits),
        },
    ]


def build_preview(cleaned_data, parser, macro_hits, blocked_hits):
    code = cleaned_data.get("code", "")
    width = cleaned_data["width"]
    height = cleaned_data["height"]
    input_mode = cleaned_data["input_mode"]

    if not code:
        return {
            "label": "Sin contenido",
            "tone": "warn",
            "summary": "No se envió código para renderizar. La herramienta queda lista, pero no hay vista previa ni lectura técnica real.",
            "note": "Pega una creatividad HTML o un tag de terceros para activar la vista previa.",
            "width": width,
            "height": height,
            "creative_type": CREATIVE_TYPE_LABELS[cleaned_data["creative_type"]],
            "input_mode": INPUT_MODE_LABELS[input_mode],
            "frame_document": "",
        }

    if blocked_hits:
        return {
            "label": "Bloqueada",
            "tone": "critical",
            "summary": "La vista previa no se ejecutó porque el código incluye patrones de navegación de frame que no conviene correr dentro de este sandbox.",
            "note": "El análisis básico sigue disponible, pero la ejecución visual se reemplazó por un marcador seguro.",
            "width": width,
            "height": height,
            "creative_type": CREATIVE_TYPE_LABELS[cleaned_data["creative_type"]],
            "input_mode": INPUT_MODE_LABELS[input_mode],
            "frame_document": build_blocked_preview_document(width, height),
        }

    is_partial = (
        input_mode == "third_party"
        or parser.script_count > 0
        or parser.iframe_count > 0
        or len(parser.external_assets) > 0
        or len(macro_hits) > 0
    )

    return {
        "label": "Parcial" if is_partial else "Renderizada",
        "tone": "warn" if is_partial else "good",
        "summary": build_preview_summary(is_partial, parser, macro_hits, input_mode),
        "note": "Vista previa en sandbox únicamente. No replica SafeFrame, ad server, validación de red ni clic real.",
        "width": width,
        "height": height,
        "creative_type": CREATIVE_TYPE_LABELS[cleaned_data["creative_type"]],
        "input_mode": INPUT_MODE_LABELS[input_mode],
        "frame_document": build_preview_document(code, width, height),
    }


def build_technical_flags(cleaned_data, parser, macro_hits, placeholder_hits, blocked_hits):
    flags = []

    if not cleaned_data.get("code"):
        flags.append("No hay código cargado para revisar.")
        return flags

    if blocked_hits:
        flags.append("La vista previa visual se bloqueó por patrones de navegación de frame o escape del contenedor.")

    if cleaned_data["width"] <= 0 or cleaned_data["height"] <= 0:
        flags.append("El tamaño declarado no es válido para una vista previa útil.")

    if parser.autoplay_count:
        flags.append("Se detectaron etiquetas multimedia con reproducción automática; conviene revisar la política del placement.")

    if parser.audio_count and parser.autoplay_count:
        flags.append("Hay audio o video con reproducción automática, lo que necesita revisión técnica antes de aprobar.")

    if parser.link_count == 0 and not cleaned_data.get("click_url") and cleaned_data["creative_type"] in {"display", "rich_media"}:
        flags.append("No se detectaron enlaces ni una URL de clic de referencia en un formato que probablemente necesita click path.")

    if cleaned_data["input_mode"] == "third_party" and parser.script_count == 0 and parser.iframe_count == 0:
        flags.append("Se eligió Tag de terceros, pero no aparecen scripts ni iframes en el código cargado.")

    if placeholder_hits:
        flags.append("Hay placeholders o texto incompleto visibles dentro del código.")

    return flags


def build_qa_observations(cleaned_data, parser, macro_hits, placeholder_hits, preview):
    observations = []

    if not cleaned_data.get("code"):
        observations.append("Pega una creatividad o un tag para generar vista previa y hallazgos.")
        return observations

    if parser.script_count:
        observations.append("La pieza incluye scripts; la ejecución puede depender de recursos externos o condiciones del entorno.")

    if parser.iframe_count:
        observations.append("Se detectaron iframes; parte del contenido puede vivir fuera del sandbox principal.")

    if len(parser.external_assets) > 0:
        observations.append("Hay referencias externas y su render puede ser parcial o quedar bloqueado según la disponibilidad o las políticas del recurso.")

    if macro_hits:
        observations.append("Hay macros o placeholders visibles; la vista previa no reemplaza esas variables automáticamente.")

    if cleaned_data.get("click_url") and parser.link_count == 0:
        observations.append("Se declaró una URL de clic, pero la herramienta no la inyecta dentro del markup en esta versión.")

    if parser.inline_handler_count:
        observations.append("Se detectaron manejadores inline; conviene revisar comportamiento y dependencias de JavaScript.")

    if parser.media_count and not parser.autoplay_count:
        observations.append("Hay etiquetas multimedia sin reproducción automática visible. Igual conviene revisar codecs, peso y políticas del placement.")

    if cleaned_data.get("notes"):
        observations.append("La ejecución incluye notas operativas para dar contexto a la revisión.")

    if preview["label"] == "Parcial":
        observations.append("La vista previa debe leerse como un sandbox controlado y no como una réplica exacta del entorno de serving.")

    return observations or ["No aparecieron observaciones adicionales en esta ejecución."]


def build_limitations(cleaned_data, parser, preview):
    limitations = [
        "La vista previa corre dentro de un iframe con sandbox y prioriza estabilidad sobre fidelidad absoluta.",
        "No simula un ad server real, SafeFrame, tracking de red ni compatibilidad completa entre placements.",
    ]

    if cleaned_data.get("input_mode") == "third_party" or parser.script_count or parser.iframe_count:
        limitations.append("La ejecución de tags de terceros puede depender de entornos externos y renderizar de forma parcial.")

    if preview["label"] == "Bloqueada":
        limitations.append("Algunos patrones de navegación o escape del frame se bloquean de forma preventiva en esta versión.")

    if parser.external_assets:
        limitations.append("Los scripts o recursos externos pueden fallar, demorarse o renderizar de forma parcial dentro del sandbox.")

    return limitations


def build_recommendation(preview, technical_flags, qa_observations):
    if preview["label"] == "Sin contenido":
        return {
            "label": "Sin contenido",
            "tone": "warn",
            "text": "Pega código y vuelve a renderizar. La herramienta está pensada para dar vista previa y hallazgos en una sola pasada corta.",
        }

    if preview["label"] == "Bloqueada":
        return {
            "label": "No se puede validar por completo",
            "tone": "critical",
            "text": "La vista previa visual no es segura en este sandbox. Hace falta una revisión técnica más controlada antes de intentar validar la pieza.",
        }

    if technical_flags:
        return {
            "label": "Necesita revisión técnica" if preview["label"] == "Renderizada" else "Vista previa parcial",
            "tone": "warn",
            "text": f"Primer foco: {technical_flags[0].lower()} Después conviene repetir la vista previa o escalar a una revisión técnica más profunda según el caso.",
        }

    if preview["label"] == "Parcial":
        return {
            "label": "Vista previa parcial",
            "tone": "warn",
            "text": "La vista previa es útil para una lectura inicial, pero el comportamiento final puede depender de entornos externos o condiciones de serving.",
        }

    return {
        "label": "Lista para revisión inicial",
        "tone": "good",
        "text": "La pieza queda lista para una revisión visual y técnica inicial dentro de este sandbox controlado.",
    }


def build_preview_document(code, width, height):
    if looks_like_full_document(code):
        return code

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      background: #090d13;
      overflow: auto;
    }}
    body {{
      display: flex;
      align-items: flex-start;
      justify-content: flex-start;
    }}
    .preview-root {{
      width: {width}px;
      min-height: {height}px;
      box-sizing: border-box;
      pointer-events: none;
    }}
    * {{
      box-sizing: border-box;
    }}
  </style>
</head>
<body>
  <div class="preview-root">{code}</div>
</body>
</html>"""


def build_blocked_preview_document(width, height):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      background: #090d13;
      color: #d7e0eb;
      font-family: system-ui, sans-serif;
    }}
    body {{
      display: grid;
      place-items: center;
    }}
    .blocked-state {{
      width: min(100%, {width}px);
      min-height: min(100%, {height}px);
      padding: 24px;
      border: 1px solid rgba(130, 154, 181, 0.35);
      border-radius: 16px;
      background: rgba(14, 18, 26, 0.9);
    }}
    .blocked-state strong {{
      display: block;
      margin-bottom: 12px;
      color: #ffffff;
    }}
  </style>
</head>
<body>
  <div class="blocked-state">
    <strong>Vista previa bloqueada en el sandbox</strong>
    <span>El código incluye patrones de navegación de frame que esta vista previa no ejecuta.</span>
  </div>
</body>
</html>"""


def build_preview_summary(is_partial, parser, macro_hits, input_mode):
    if not is_partial:
        return "La vista previa se renderizó dentro del sandbox sin depender de ejecución externa evidente."

    if input_mode == "third_party":
        return "La ejecución de tags de terceros puede depender de entornos externos. La vista previa sirve como lectura inicial y puede ser parcial."

    if parser.script_count or parser.iframe_count:
        return "La pieza incluye código ejecutable o frames externos. La vista previa puede quedarse en una lectura parcial."

    if macro_hits:
        return "Hay macros o placeholders sin resolver. La vista previa visual puede no representar la salida final."

    return "La vista previa se renderizó con limitaciones parciales propias de este sandbox."


def build_count_detail(count, references, label):
    if not count:
        return f"No se detectaron {label}."

    unique_references = unique_preserve_order(references)
    if unique_references:
        return f"{count} detectado(s). Ejemplo: {unique_references[0]}"
    return f"{count} detectado(s)."


def build_external_detail(references):
    unique_refs = unique_preserve_order(references)
    if not unique_refs:
        return "No se detectaron referencias externas."

    host = extract_host(unique_refs[0])
    return f"{len(unique_refs)} referencia(s) externa(s). Primer host visible: {host or unique_refs[0]}"


def build_media_detail(parser):
    if not parser.media_count:
        return "No se detectaron etiquetas de audio o video."

    parts = [f"{parser.media_count} etiqueta(s) multimedia"]
    if parser.autoplay_count:
        parts.append(f"{parser.autoplay_count} con autoplay")
    return ". ".join(parts) + "."


def build_macro_detail(macro_hits, placeholder_hits):
    hits = unique_preserve_order(macro_hits + placeholder_hits)
    if not hits:
        return "No se detectaron macros o placeholders visibles."
    return f"{len(hits)} patron(es) visible(s). Ejemplo: {hits[0]}"


def looks_like_full_document(code):
    lowered = code.lower()
    return "<html" in lowered or "<!doctype" in lowered


def find_pattern_hits(text, patterns):
    hits = []
    for pattern in patterns:
        hits.extend(pattern.findall(text or ""))
    return unique_preserve_order(str(hit) for hit in hits)


def unique_preserve_order(items):
    seen = set()
    result = []
    for item in items:
        normalized = (item or "").strip()
        if not normalized:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def extract_host(reference):
    parsed = urlparse(reference if not reference.startswith("//") else f"https:{reference}")
    return parsed.netloc


def build_insight(cleaned_data, parser, macro_hits, placeholder_hits, preview):
    issues = []

    if preview["label"] == "Bloqueada":
        issues.append(
            build_insight_issue(
                "La vista previa fue bloqueada por las reglas de seguridad del sandbox.",
                penalty=45,
                impact="Alto",
                risk="Bloqueante",
                priority="Corregir ahora",
                areas=["Entrega", "QA"],
            )
        )
    elif preview["label"] == "Parcial":
        issues.append(
            build_insight_issue(
                "La vista previa es parcial, por lo que la base de render sigue incompleta.",
                penalty=18,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["Entrega", "QA"],
            )
        )
    elif preview["label"] == "Sin contenido":
        issues.append(
            build_insight_issue(
                "No se cargó código para la vista previa ni para la revisión.",
                penalty=28,
                impact="Bajo",
                risk="Bajo",
                priority="Informativa",
                areas=["QA"],
            )
        )

    if parser.audio_count and parser.autoplay_count:
        issues.append(
            build_insight_issue(
                "El autoplay con audio o video necesita revisión técnica antes de aprobar.",
                penalty=24,
                impact="Alto",
                risk="Alto",
                priority="Corregir ahora",
                areas=["QA", "UX"],
            )
        )
    elif parser.autoplay_count:
        issues.append(
            build_insight_issue(
                "La reproducción automática es visible dentro del markup.",
                penalty=14,
                impact="Medio",
                risk="Alto",
                priority="Revisar pronto",
                areas=["QA", "UX"],
            )
        )

    if parser.link_count == 0 and not cleaned_data.get("click_url") and cleaned_data["creative_type"] in {"display", "rich_media"}:
        issues.append(
            build_insight_issue(
                "No hay un click path visible para un formato que probablemente lo necesita.",
                penalty=18,
                impact="Medio",
                risk="Alto",
                priority="Revisar pronto",
                areas=["Tracking", "Entrega"],
            )
        )

    if placeholder_hits or macro_hits:
        issues.append(
            build_insight_issue(
                "Las macros o placeholders visibles reducen la confianza en la salida de la vista previa.",
                penalty=12,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["Entrega", "QA"],
            )
        )

    if parser.external_assets:
        issues.append(
            build_insight_issue(
                "Los recursos externos pueden cambiar o fallar fuera de este sandbox.",
                penalty=8,
                impact="Bajo",
                risk="Bajo",
                priority="Monitorear",
                areas=["Entrega"],
            )
        )

    if cleaned_data.get("input_mode") == "third_party" and parser.script_count == 0 and parser.iframe_count == 0:
        issues.append(
            build_insight_issue(
                "Se eligió el modo de terceros sin etiquetas visibles de ejecución.",
                penalty=12,
                impact="Medio",
                risk="Medio",
                priority="Revisar pronto",
                areas=["QA"],
            )
        )

    if parser.inline_handler_count:
        issues.append(
            build_insight_issue(
                "Los manejadores inline agregan supuestos de ejecución que este sandbox no valida por completo.",
                penalty=8,
                impact="Bajo",
                risk="Bajo",
                priority="Monitorear",
                areas=["QA"],
            )
        )

    return summarize_insight(
        issues,
        positive_summary="La vista previa es lo bastante estable para una revisión visual y técnica inicial.",
        context_label="vista previa de creatividad",
    )


def build_exports(preview, detected, technical_flags, qa_observations, limitations, recommendation, insight):
    detected_lines = [f"{item['label']}: {item['detail']}" for item in detected]
    findings = technical_flags + qa_observations + limitations

    return build_copy_exports(
        title="Creative Preview Lab",
        summary=preview["summary"],
        findings=findings,
        recommendation=recommendation["text"],
        sections=[
            ("Estado de la vista previa", [preview["label"], preview["note"]]),
            ("Elementos detectados", detected_lines),
            ("Alertas técnicas", technical_flags),
            ("Observaciones de QA", qa_observations),
            ("Limitaciones", limitations),
        ],
        insight=insight,
    )
