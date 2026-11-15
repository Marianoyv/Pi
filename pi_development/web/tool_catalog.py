from copy import deepcopy


TOOLS_INDEX_PAGE = {
    "eyebrow": "Products",
    "title": "Working products for campaign tagging and creative quality checks.",
    "description": (
        "Three maintained, deterministic products for building UTM-tagged URLs, guiding a manual creative QA review "
        "and running a sandboxed first-pass creative preview."
    ),
    "seo_title": "AdTech & Campaign Products | Pi Development",
    "featured_label": "Featured product",
    "featured_title": "UTM Builder",
    "featured_description": "Build consistent campaign URLs while preserving existing query parameters.",
    "catalog_title": "Maintained public products",
    "catalog_description": "Each product has a narrow, explicit purpose and states its real limitations.",
}

TOOL_GROUPS = {
    "operations": {
        "key": "operations",
        "title": "Campaign operations",
        "description": "Utilities for consistent tagging and fewer manual campaign URL errors.",
    },
    "qa_preview": {
        "key": "qa_preview",
        "title": "Creative QA and preview",
        "description": "Manual review guidance and a constrained sandbox for first-pass creative inspection.",
    },
}

OPERATION_AND_QA_TOOLS = [
    {
        "slug": "utm-builder",
        "name": "UTM Builder",
        "tag": "Tagging",
        "status_label": "Active",
        "status_tone": "live",
        "summary": "URL generator with consistent UTM parameters.",
        "description": "Build URLs with UTM parameters without breaking existing query params and leave a clear output for copying, validating and sharing.",
        "seo_title": "URL generator with UTM parameters | Pi Development",
        "meta_description": "UTM Builder builds URLs with consistent UTM parameters, preserves existing query params, and avoids common tagging errors.",
        "meta_keywords": "UTM generator, UTM URL builder, utm parameters, campaign tagging, url tracking",
        "page_title": "URL generator with UTM parameters",
        "page_description": "UTM Builder assembles tagged URLs, preserves previous parameters, and shows which fields are missing to maintain consistent analytical tagging.",
        "is_live": True,
        "group_key": "operations",
        "cta_label": "Open UTM Builder",
        "recommended_for": ["Campaign tagging", "Trafficking", "Control de URLs con tracking"],
        "related_slugs": ["landing-performance-snapshot", "ai-auditor", "creative-qa-checklist"],
        "related_context": "If the final URL also needs technical review or QA control, these tools complete the flow.",
        "capabilities": [
            "Rebuild URLs without losing existing query params.",
            "Normalizes UTM values ​​to reduce manual errors.",
            "Flag when source, medium or campaign are missing.",
        ],
        "inputs": ["destination URL", "utm_source, utm_medium, utm_campaign", "optional utm_term and utm_content"],
        "outputs": ["Constructed final URL", "Parameter preview", "Labeling remarks"],
        "detail_blocks": [
            {
                "title": "What does this version do?",
                "items": [
                    "Validate the destination URL and rebuild the query safely.",
                    "Preserves existing parameters and adds only completed UTM keys.",
                    "Flag missing base fields before sharing the URL.",
                ],
            },
            {
                "title": "What a future version can add",
                "items": [
                    "Templates by channel or client.",
                    "Naming presets.",
                    "Mass URL generation.",
                ],
            },
        ],
        "editorial": {
            "analysis_title": "What UTM Builder does",
            "analysis_items": [
                "Validate the destination URL before building the output.",
                "Preserves existing query params that do not belong to UTM.",
                "Add only the UTM parameters that you complete in the form.",
            ],
            "use_title": "When should it be used?",
            "use_items": [
                "Before launching campaigns with tracking by source, medium and campaign.",
                "When you need to share clean URLs with consistent tracking criteria.",
                "To check if a URL already has UTM parameters or if it is incomplete.",
            ],
            "results_title": "What results does it return?",
            "results_items": [
                "The final URL ready to copy.",
                "A clear view of applied and preserved parameters.",
                "Observations about missing fields or overwriting of existing UTMs.",
            ],
            "limitations_title": "Real limitations",
            "limitations_items": [
                "It does not validate internal taxonomies or naming conventions of each team.",
                "It does not save presets or generate batches in this version.",
                "It does not replace analytical governance if the naming changes between campaigns.",
            ],
            "faq_title": "UTM Builder FAQ",
            "faqs": [
                {"question": "Does the tool remove parameters that already exist?", "answer": "No. Keep the existing parameters unless you send a UTM with the same key."},
                {"question": "Can I leave empty fields?", "answer": "Yes. Optional fields can be left empty and the tool does not invent values."},
                {"question": "Does it work for any URL?", "answer": "Yes, as long as the URL is public and uses http or https."},
            ],
        },
    },
    {
        "slug": "creative-qa-checklist",
        "name": "Creative QA Checklist",
        "tag": "Technical QA",
        "status_label": "Active",
        "status_tone": "live",
        "summary": "Technical checklist to review creatives and tags.",
        "description": "Convert manual data from a creative into an initial technical reading with checklist, observations, alerts and final status.",
        "seo_title": "Technical checklist to validate creativity | Pi Development",
        "meta_description": "Creative QA Checklist reviews dimensions, click path, tracking, weight, autoplay and serving context to evaluate a creative.",
        "meta_keywords": "creative validation, technical checklist, banner qa, click path, advertising tracking",
        "page_title": "Technical checklist to validate advertising creativity",
        "page_description": "Creative QA Checklist organizes the initial review of a creative with simple rules on dimensions, click path, tracking, weight, playback, and serving context.",
        "is_live": True,
        "group_key": "qa_preview",
        "cta_label": "Abrir Creative QA Checklist",
        "recommended_for": ["Preflight of creativity", "QA previo a trafficking", "Initial technical review"],
        "related_slugs": ["creative-preview-lab", "adtech-debug-tool", "utm-builder"],
        "related_context": "If you need to preview the piece or review the ad stack where it could be served, these tools follow the same flow.",
        "capabilities": [
            "Evaluates click path, tracking, weight, context and playback.",
            "Deliver final status with transparent criteria.",
            "Separates correct points, observations and strong alerts.",
        ],
        "inputs": ["Manual creativity data", "URL, weight, context and playback", "Optional notes"],
        "outputs": ["Structured checklist", "Observations and alerts", "QA Final Status"],
        "detail_blocks": [
            {
                "title": "What does this version do?",
                "items": [
                    "Take manual data and apply simple but useful rules.",
                    "Distinguishes between correct points, observations and crash alerts.",
                    "Clearly shows what needs to be reviewed before approving.",
                ],
            },
            {
                "title": "What it doesn't do",
                "items": [
                    "It does not inspect actual binaries or manifests.",
                    "It does not validate the loading of network resources.",
                    "It does not replace a final trafficking operational review.",
                ],
            },
        ],
        "editorial": {
            "analysis_title": "What Creative QA Checklist analyzes",
            "analysis_items": [
                "Declared dimensions, click path and destination URL.",
                "Additional tracking, asset weight and target device.",
                "Audio behavior, autoplay and serving context.",
            ],
            "use_title": "When should it be used?",
            "use_items": [
                "Before approving a creative for trafficking.",
                "When you need quick validation based on clear rules.",
                "To document technical observations without opening a separate control sheet.",
            ],
            "results_title": "What results does it return?",
            "results_items": [
                "Final status: ready, needs review, or blocked.",
                "Checklist with detail by criterion.",
                "Observations and prioritized alerts.",
            ],
            "limitations_title": "Real limitations",
            "limitations_items": [
                "It depends on the manual data loaded in the form.",
                "It does not inspect the source file or verify the actual execution.",
                "It does not validate compatibility by ad server or specific platform.",
            ],
            "faq_title": "Creative QA Checklist FAQ",
            "faqs": [
                {"question": "Can I use it without having the final file?", "answer": "Yes. The tool is intended for an initial review based on manual data."},
                {"question": "Does it mark real locks?", "answer": "Yes. Some rules, such as autoplay with sound or complete lack of click path, are considered blocking."},
                {"question": "Does it work for any format?", "answer": "It serves as a first review of various formats, but does not cover all the particularities of each platform."},
            ],
        },
    },
    {
        "slug": "creative-preview-lab",
        "name": "Creative Preview Lab",
        "tag": "Preview and QA",
        "status_label": "Active",
        "status_tone": "live",
        "summary": "Controlled preview for HTML creatives and tags.",
        "description": "It allows you to paste third-party markup or tags, define dimensions and obtain a contained preview along with a basic and honest technical reading.",
        "seo_title": "Preview HTML creatives and ad tags | Pi Development",
        "meta_description": "Creative Preview Lab renders HTML creatives and ad tags in a controlled sandbox and detects scripts, iframes, links, and technical limitations.",
        "meta_keywords": "html creative preview, advertising tag validator, html sandbox, banner review, third-party tag preview",
        "page_title": "Preview HTML creatives and ad tags",
        "page_description": "Creative Preview Lab allows you to paste HTML code or third-party tags, render a preview in a sandbox, and receive a basic technical reading on scripts, iframes, links, and limitations.",
        "is_live": True,
        "group_key": "qa_preview",
        "cta_label": "Abrir Creative Preview Lab",
        "recommended_for": ["Quick markup preview", "Initial review of third-party tags", "Visual QA before scaling"],
        "related_slugs": ["creative-qa-checklist", "adtech-debug-tool", "landing-performance-snapshot"],
        "related_context": "If after the preview you need to validate QA criteria or review the AdTech layer, these tools complete the review.",
        "capabilities": [
            "Render code inside a sandboxed iframe.",
            "Detects visible scripts, iframes, links, media, external references, and macros.",
            "Clarifies when the preview is partial, blocked, or dependent on an external environment.",
        ],
        "inputs": ["Part type", "Width and height", "input mode", "HTML code or tag", "Click URL and optional notes"],
        "outputs": ["Preview status", "Detected elements", "Technical observations", "Final recommendation"],
        "detail_blocks": [
            {
                "title": "What does this version do?",
                "items": [
                    "Receives markup or tags from third parties and renders them within a controlled iframe.",
                    "Deliver immediate technical findings without promising full validation.",
                    "Explains when the preview is partial or locked for security.",
                ],
            },
            {
                "title": "What it doesn't do",
                "items": [
                    "It does not simulate the real behavior of an ad server.",
                    "It does not validate network tracking or real clicks.",
                    "It does not replicate SafeFrame or proprietary environments.",
                ],
            },
        ],
        "editorial": {
            "analysis_title": "What Creative Preview Lab analyzes",
            "analysis_items": [
                "Scripts, iframes, links, external resources and multimedia tags.",
                "Macros, placeholders and patterns that limit the preview.",
                "Declared dimensions and general condition of the render.",
            ],
            "use_title": "When should it be used?",
            "use_items": [
                "When you need to review HTML code or a tag in a few seconds.",
                "Before passing a part on to a deeper technical review.",
                "To immediately detect if the preview is partial or unsafe.",
            ],
            "results_title": "What results does it return?",
            "results_items": [
                "A rendered, partial, locked, or empty preview.",
                "Count of elements detected within the code.",
                "Observations and technical limitations for a first review.",
            ],
            "limitations_title": "Real limitations",
            "limitations_items": [
                "It does not replicate SafeFrame or the behavior of a real ad server.",
                "External scripts may hang or render partially.",
                "It does not verify tracking, real clicks or total compatibility.",
            ],
            "faq_title": "Creative Preview Lab FAQ",
            "faqs": [
                {"question": "Does the preview exactly replicate the ad server?", "answer": "No. This is a controlled preview for initial review, not an exact simulation of actual serving."},
                {"question": "Can you lock a code?", "answer": "Yes. If it detects patterns of frame escape or unsafe navigation, it blocks the visual execution and maintains the technical analysis."},
                {"question": "Does it work for third-party tags?", "answer": "Yes, but execution can be partial if it depends on external resources or a proprietary environment."},
            ],
        },
    },
]

TOOL_DEFINITIONS = OPERATION_AND_QA_TOOLS

PUBLIC_TOOL_SLUGS = {"utm-builder", "creative-qa-checklist", "creative-preview-lab"}

# English public presentation for the three static browser tools.
PUBLIC_TOOL_CONTENT = {
    "utm-builder": {
        "tag": "Campaign tagging",
        "status_label": "Available",
        "summary": "Build consistent UTM-tagged URLs without discarding existing query parameters.",
        "description": "A deterministic URL builder for consistent campaign tagging and easier review.",
        "seo_title": "UTM Builder for Campaign URLs | Pi Development",
        "meta_description": "Build consistent UTM campaign URLs while preserving existing query parameters.",
        "page_title": "Build a campaign URL with consistent UTM parameters",
        "page_description": "UTM Builder validates the destination, preserves existing query parameters and adds only the UTM values you provide.",
        "cta_label": "Open UTM Builder",
        "recommended_for": ["Campaign tagging", "Trafficking workflows", "Analytics QA"],
        "related_slugs": ["creative-qa-checklist", "creative-preview-lab"],
        "related_context": "Use the creative products when the campaign asset also needs a structured first-pass review.",
        "capabilities": ["Preserves existing query parameters.", "Normalizes UTM values.", "Flags missing base UTM fields."],
        "inputs": ["Destination URL", "Source, medium and campaign", "Optional term and content"],
        "outputs": ["Final tagged URL", "Applied parameter summary", "Tagging observations"],
        "detail_blocks": [
            {"title": "What this version does", "items": ["Validates and rebuilds the destination URL safely.", "Preserves existing parameters.", "Adds only completed UTM fields."]},
            {"title": "Current limits", "items": ["It does not enforce an internal naming taxonomy.", "It does not save presets or generate URL batches."]},
        ],
        "editorial": {
            "analysis_title": "What UTM Builder does",
            "analysis_items": ["Validates the destination URL.", "Preserves non-UTM query parameters.", "Adds only the supplied UTM fields."],
            "use_title": "When to use it",
            "use_items": ["Before launching a tagged campaign.", "When sharing URLs under a consistent convention.", "When reviewing an existing tagged URL."],
            "results_title": "What it returns",
            "results_items": ["A copy-ready URL.", "A parameter summary.", "Warnings about missing base fields or replaced UTM values."],
            "limitations_title": "Real limitations",
            "limitations_items": ["It cannot validate an internal naming taxonomy.", "It does not store presets.", "It does not replace analytics governance."],
            "faq_title": "UTM Builder questions",
            "faqs": [{"question": "Does it remove existing parameters?", "answer": "No. Existing parameters remain unless a supplied UTM value uses the same key."}],
        },
    },
    "creative-qa-checklist": {
        "tag": "Guided self-assessment",
        "status_label": "Available",
        "summary": "A guided manual self-assessment for common creative QA criteria.",
        "description": "Enter known creative details and receive a transparent rule-based checklist for a first-pass review.",
        "seo_title": "Creative QA Checklist | Pi Development",
        "meta_description": "Run a guided manual self-assessment for creative dimensions, click paths, tracking, weight, playback and serving context.",
        "page_title": "Run a guided creative QA self-assessment",
        "page_description": "Creative QA Checklist applies explicit rules to the information you enter. It does not inspect the source asset or replace final trafficking QA.",
        "cta_label": "Open Creative QA Checklist",
        "recommended_for": ["Creative preflight", "Pre-trafficking review", "Documented manual QA"],
        "related_slugs": ["creative-preview-lab", "utm-builder"],
        "related_context": "Preview markup separately when a visual first pass is also useful.",
        "capabilities": ["Reviews manually entered details.", "Uses visible deterministic rules.", "Separates passes, cautions and blockers."],
        "inputs": ["Manually entered creative details", "Destination and tracking context", "Optional notes"],
        "outputs": ["Guided checklist", "Observations and flags", "Rule-based status"],
        "detail_blocks": [
            {"title": "What this version does", "items": ["Applies transparent rules to entered information.", "Highlights items that need human follow-up."]},
            {"title": "What it does not do", "items": ["It does not inspect assets or manifests.", "It does not validate network requests.", "It does not replace final platform QA."]},
        ],
        "editorial": {
            "analysis_title": "What the checklist reviews",
            "analysis_items": ["Declared dimensions and click path.", "Tracking, file weight and target device.", "Audio, autoplay and serving context."],
            "use_title": "When to use it",
            "use_items": ["Before a creative enters trafficking.", "For a quick review under explicit rules.", "To document known first-pass concerns."],
            "results_title": "What it returns",
            "results_items": ["A rule-based status.", "A criterion-by-criterion checklist.", "Prioritized observations and flags."],
            "limitations_title": "Real limitations",
            "limitations_items": ["Results depend on entered information.", "The source file is not inspected.", "Platform compatibility is not verified."],
            "faq_title": "Creative QA Checklist questions",
            "faqs": [{"question": "Is this an automated asset validator?", "answer": "No. It is a guided self-assessment based on the details you provide."}],
        },
    },
    "creative-preview-lab": {
        "tag": "Sandboxed preview",
        "status_label": "Available",
        "summary": "A sandboxed first-pass preview for HTML creatives and third-party tags.",
        "description": "Render supplied markup in a constrained iframe and review visible structural signals and limitations.",
        "seo_title": "Creative Preview Lab | Pi Development",
        "meta_description": "Run a sandboxed first-pass preview of HTML creative markup or a third-party tag with explicit limitations.",
        "page_title": "Preview creative markup in a constrained sandbox",
        "page_description": "Creative Preview Lab is a sandboxed first-pass preview. It is not an ad server, SafeFrame or full tracking simulation.",
        "cta_label": "Open Creative Preview Lab",
        "recommended_for": ["Markup first pass", "Third-party tag review", "Visual QA before escalation"],
        "related_slugs": ["creative-qa-checklist", "utm-builder"],
        "related_context": "Use the checklist to record manual QA criteria alongside the preview.",
        "capabilities": ["Renders code in a sandboxed iframe.", "Surfaces visible structural elements.", "Explains partial or blocked previews."],
        "inputs": ["Creative type and dimensions", "HTML markup or third-party tag", "Optional click URL and notes"],
        "outputs": ["Sandboxed preview state", "Detected structural elements", "First-pass limitations"],
        "detail_blocks": [
            {"title": "What this version does", "items": ["Renders supplied markup in a constrained iframe.", "Surfaces structural observations.", "Explains partial or blocked previews."]},
            {"title": "What it does not do", "items": ["It does not simulate an ad server.", "It does not reproduce SafeFrame.", "It does not validate real network tracking or clicks."]},
        ],
        "editorial": {
            "analysis_title": "What the preview inspects",
            "analysis_items": ["Scripts, iframes, links and media tags.", "Visible macros and placeholders.", "Declared dimensions and render state."],
            "use_title": "When to use it",
            "use_items": ["For a quick markup first pass.", "Before deeper browser or platform QA.", "To identify an obviously partial or unsafe preview."],
            "results_title": "What it returns",
            "results_items": ["A rendered, partial, blocked or empty state.", "Detected element counts.", "First-pass observations and limitations."],
            "limitations_title": "Real limitations",
            "limitations_items": ["It is not a SafeFrame or ad-server simulation.", "External scripts may be blocked or partial.", "Tracking and full compatibility are not verified."],
            "faq_title": "Creative Preview Lab questions",
            "faqs": [{"question": "Does this reproduce real ad serving?", "answer": "No. It is a constrained first-pass preview, not a real ad-server or SafeFrame simulation."}],
        },
    },
}


def get_tools_index_page():
    return deepcopy(TOOLS_INDEX_PAGE)


def get_tools(include_unavailable=False):
    tools = [_with_availability(tool) for tool in TOOL_DEFINITIONS]
    if include_unavailable:
        return tools
    return [tool for tool in tools if tool["is_available"] and tool["public_visibility"]]


def get_featured_tool():
    tools = get_tools()
    return tools[0] if tools else None


def get_tool(slug, include_unavailable=False):
    for tool in TOOL_DEFINITIONS:
        if tool["slug"] == slug:
            prepared_tool = _with_availability(tool)
            if prepared_tool["is_available"] or include_unavailable:
                return prepared_tool
            return None
    return None


def get_public_tool_slugs():
    return [tool["slug"] for tool in get_tools() if tool.get("is_live") and tool["public_visibility"]]


def get_tool_groups():
    available_tools = get_tools()
    groups = []
    for group_key, group_meta in TOOL_GROUPS.items():
        group_tools = [tool for tool in available_tools if tool.get("group_key") == group_key]
        if group_tools:
            groups.append(
                {
                    "key": group_meta["key"],
                    "title": group_meta["title"],
                    "description": group_meta["description"],
                    "tools": group_tools,
                }
            )
    return groups


def get_related_tools(slug, limit=3):
    current_tool = get_tool(slug, include_unavailable=True)
    if not current_tool:
        return []

    related_slugs = list(current_tool.get("related_slugs") or [])
    ordered_slugs = related_slugs + [
        tool["slug"] for tool in TOOL_DEFINITIONS if tool["slug"] not in related_slugs and tool["slug"] != slug
    ]
    related_tools = []

    for related_slug in ordered_slugs:
        if related_slug == slug:
            continue
        tool = get_tool(related_slug)
        if tool and tool.get("public_visibility"):
            related_tools.append(tool)
        if len(related_tools) >= limit:
            break

    return related_tools


def _with_availability(tool):
    prepared_tool = deepcopy(tool)
    prepared_tool.update(deepcopy(PUBLIC_TOOL_CONTENT.get(prepared_tool["slug"], {})))
    prepared_tool["public_visibility"] = prepared_tool["slug"] in PUBLIC_TOOL_SLUGS
    prepared_tool["is_available"] = True
    return prepared_tool
