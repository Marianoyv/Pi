from copy import deepcopy


EXAMPLE_CREATIVE_HTML = """<div style="width:300px;height:250px;padding:20px;background:linear-gradient(180deg,#0f172a,#1e293b);color:#f8fafc;font-family:Inter,Arial,sans-serif;display:flex;flex-direction:column;justify-content:space-between;border:1px solid rgba(148,163,184,.25);">
  <div>
    <p style="margin:0 0 10px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#7dd3fc;">Demo HTML</p>
    <h2 style="margin:0 0 12px;font-size:24px;line-height:1.1;">Example creative preview</h2>
    <p style="margin:0;font-size:14px;line-height:1.45;color:#cbd5e1;">A simple asset for testing the render and first-pass review without third-party dependencies.</p>
  </div>
  <a href="https://pidevelopment.web.app/contact/" style="display:inline-block;padding:10px 14px;border-radius:999px;background:#2563eb;color:#fff;text-decoration:none;font-size:14px;font-weight:600;">View contact</a>
</div>"""


TOOL_EXAMPLES = {
    "utm-builder": {
        "button_label": "Load example",
        "title": "Quick example",
        "description": "Build a tagged URL with source, medium and campaign values to inspect the final output.",
        "form_data": {
            "destination_url": "https://pidevelopment.web.app/contact/",
            "utm_source": "newsletter",
            "utm_medium": "email",
            "utm_campaign": "seo_examples",
            "utm_term": "software-project",
            "utm_content": "primary-cta",
        },
    },
    "creative-qa-checklist": {
        "button_label": "Load example",
        "title": "Quick example",
        "description": "Load a realistic 300x250 display case with click, tracking and serving context.",
        "form_data": {
            "creative_name": "Display launch 300x250",
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
            "extra_notes": "Example first-pass review with declared click and tracking details.",
        },
    },
    "creative-preview-lab": {
        "button_label": "Load example",
        "title": "Quick example",
        "description": "Render simple HTML markup to inspect the sandbox and structural first-pass output.",
        "form_data": {
            "creative_name": "Demo CTA 300x250",
            "creative_type": "display",
            "width": 300,
            "height": 250,
            "input_mode": "html",
            "code": EXAMPLE_CREATIVE_HTML,
            "click_url": "https://pidevelopment.web.app/contact/",
            "notes": "Simple example for testing the sandbox and first-pass markup review.",
        },
    },
}


def get_tool_example(slug):
    example = TOOL_EXAMPLES.get(slug)
    return deepcopy(example) if example else None


