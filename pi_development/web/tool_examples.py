from copy import deepcopy


EXAMPLE_CREATIVE_HTML = """<div style="width:300px;height:250px;padding:20px;background:linear-gradient(180deg,#0f172a,#1e293b);color:#f8fafc;font-family:Inter,Arial,sans-serif;display:flex;flex-direction:column;justify-content:space-between;border:1px solid rgba(148,163,184,.25);">
  <div>
    <p style="margin:0 0 10px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#7dd3fc;">Demo HTML</p>
    <h2 style="margin:0 0 12px;font-size:24px;line-height:1.1;">Creative preview de ejemplo</h2>
    <p style="margin:0;font-size:14px;line-height:1.45;color:#cbd5e1;">Una pieza simple para probar render, clic y lectura inicial sin depender de terceros.</p>
  </div>
  <a href="https://pidevelopment.web.app/contact/" style="display:inline-block;padding:10px 14px;border-radius:999px;background:#2563eb;color:#fff;text-decoration:none;font-size:14px;font-weight:600;">Ver contacto</a>
</div>"""


TOOL_EXAMPLES = {
    "ai-auditor": {
        "button_label": "Probar con ejemplo",
        "title": "Ejemplo rapido",
        "description": "Usa la home publica de Pi Development para mostrar una auditoria tecnica de primera pasada sin que tengas que buscar una URL.",
        "form_data": {
            "url": "https://pidevelopment.web.app/",
        },
    },
    "adtech-debug-tool": {
        "button_label": "Probar con ejemplo",
        "title": "Ejemplo rapido",
        "description": "Carga una URL publica orientada a medios para probar el flujo de deteccion AdTech. El resultado puede variar si el sitio cambia su stack visible.",
        "form_data": {
            "url": "https://edition.cnn.com/",
        },
    },
    "landing-performance-snapshot": {
        "button_label": "Probar con ejemplo",
        "title": "Ejemplo rapido",
        "description": "Usa la pagina de tools de Pi Development para ver un snapshot corto de metadata, respuesta y estructura HTML.",
        "form_data": {
            "url": "https://pidevelopment.web.app/tools/",
        },
    },
    "utm-builder": {
        "button_label": "Probar con ejemplo",
        "title": "Ejemplo rapido",
        "description": "Construye una URL etiquetada con source, medium y campaign para ver al instante como queda el output final.",
        "form_data": {
            "destination_url": "https://pidevelopment.web.app/tools/ai-auditor/",
            "utm_source": "newsletter",
            "utm_medium": "email",
            "utm_campaign": "seo_examples",
            "utm_term": "auditoria-tecnica",
            "utm_content": "cta_superior",
        },
    },
    "creative-qa-checklist": {
        "button_label": "Probar con ejemplo",
        "title": "Ejemplo rapido",
        "description": "Carga una creatividad display realista de 300x250 con click path, tracking y contexto de serving para ver la checklist completa en segundos.",
        "form_data": {
            "creative_name": "Lanzamiento display 300x250",
            "format_type": "html5",
            "dimensions": "300x250",
            "destination_url": "https://pidevelopment.web.app/contact/",
            "click_tag_present": "yes",
            "tracking_urls_included": "yes",
            "weight_kb": 145,
            "device_target": "both",
            "sound_behavior": "none",
            "autoplay_behavior": "none",
            "serving_context": "safeframe",
            "extra_notes": "Ejemplo de preflight para una creatividad display con salida de clic y tracking declarados.",
        },
    },
    "creative-preview-lab": {
        "button_label": "Probar con ejemplo",
        "title": "Ejemplo rapido",
        "description": "Renderiza una creatividad HTML simple y funcional para que puedas ver el sandbox, el preview y los hallazgos tecnicos sin preparar codigo propio.",
        "form_data": {
            "creative_name": "Demo CTA 300x250",
            "creative_type": "display",
            "width": 300,
            "height": 250,
            "input_mode": "html",
            "code": EXAMPLE_CREATIVE_HTML,
            "click_url": "https://pidevelopment.web.app/contact/",
            "notes": "Ejemplo simple para probar el sandbox y la lectura inicial del markup.",
        },
    },
}


def get_tool_example(slug):
    example = TOOL_EXAMPLES.get(slug)
    return deepcopy(example) if example else None
