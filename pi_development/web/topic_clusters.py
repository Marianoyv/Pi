from copy import deepcopy


TOPIC_CLUSTERS = {
    "ia": {
        "key": "ia",
        "title": "AI, work and people",
        "description": "How artificial intelligence changes jobs, decisions, creativity, power and everyday life.",
        "catalog_anchor": "",
        "catalog_label": "AI, work and people",
        "tool_slugs": [],
        "seo_page_slugs": [],
    },
    "web-actual": {
        "key": "web-actual",
        "title": "The current website",
        "description": "Design, trust, accessibility, performance, and the decisions that make a site feel human.",
        "catalog_anchor": "",
        "catalog_label": "The current website",
        "tool_slugs": [],
        "seo_page_slugs": [],
    },
    "tecnologia-vida": {
        "key": "tecnologia-vida",
        "title": "Technology and everyday life",
        "description": "Algorithms, privacy, habits, scams and digital changes explained from their human consequences.",
        "catalog_anchor": "",
        "catalog_label": "Technology and everyday life",
        "tool_slugs": [],
        "seo_page_slugs": [],
    },
    "producto": {
        "key": "producto",
        "title": "Build products",
        "description": "Decisions, errors, costs and real learnings behind digital products and systems.",
        "catalog_anchor": "",
        "catalog_label": "Build products",
        "tool_slugs": [],
        "seo_page_slugs": [],
    },
    "carrera": {
        "key": "carrera",
        "title": "Technology career and culture",
        "description": "Work, learning, burnout, specialization and craft within the technology industry.",
        "catalog_anchor": "",
        "catalog_label": "Technology career and culture",
        "tool_slugs": [],
        "seo_page_slugs": [],
    },
    "creatividades": {
        "key": "creatividades",
        "title": "Creatividades Group",
        "description": "Validation, preview and technical QA for HTML creatives, display and advertising tags.",
        "catalog_anchor": "qa_preview",
        "catalog_label": "QA and preview",
        "tool_slugs": ["creative-preview-lab", "creative-qa-checklist"],
        "seo_page_slugs": [
            "validar-creatividad-html",
            "preview-anuncios-html",
            "errores-creatividades-display",
            "como-validar-tags-publicitarios",
        ],
    },
    "adtech": {
        "key": "adtech",
        "title": "AdTech and digital operations",
        "description": "Digital advertising and monetization explained by its consequences for readers, teams and businesses.",
        "catalog_anchor": "diagnostics",
        "catalog_label": "Technical diagnostics",
        "tool_slugs": ["adtech-debug-tool"],
        "seo_page_slugs": [
            "debug-anuncios-web",
            "debug-gpt-ads",
            "herramientas-adtech",
        ],
    },
    "seo-performance": {
        "key": "seo-performance",
        "title": "SEO / Performance Group",
        "description": "Technical audit of URLs, visible on-page SEO and short response and metadata snapshots.",
        "catalog_anchor": "diagnostics",
        "catalog_label": "Technical diagnostics",
        "tool_slugs": ["ai-auditor", "landing-performance-snapshot"],
        "seo_page_slugs": [
            "auditoria-tecnica-web",
            "analizar-seo-pagina",
        ],
    },
    "tracking": {
        "key": "tracking",
        "title": "Grupo Tracking",
        "description": "UTM tagging, control of campaign URLs and operational order for tracking.",
        "catalog_anchor": "operations",
        "catalog_label": "Operation and labeling",
        "tool_slugs": ["utm-builder"],
        "seo_page_slugs": [
            "como-crear-utms",
        ],
    },
}


def get_topic_cluster(cluster_key):
    cluster = TOPIC_CLUSTERS.get(cluster_key)
    return deepcopy(cluster) if cluster else None


def get_topic_cluster_for_tool(tool_slug):
    for cluster in TOPIC_CLUSTERS.values():
        if tool_slug in cluster["tool_slugs"]:
            return deepcopy(cluster)
    return None


def get_topic_cluster_for_seo_page(seo_slug):
    for cluster in TOPIC_CLUSTERS.values():
        if seo_slug in cluster["seo_page_slugs"]:
            return deepcopy(cluster)
    return None


def get_related_seo_pages_for_tool(tool_slug, limit=3):
    cluster = get_topic_cluster_for_tool(tool_slug)
    if not cluster:
        return []
    return _get_seo_pages(cluster["seo_page_slugs"], current_slug=None, limit=limit)


def get_topic_cluster_context_for_tool(tool_slug):
    cluster = get_topic_cluster_for_tool(tool_slug)
    if not cluster:
        return None
    return _build_cluster_context(cluster, current_tool_slug=tool_slug)


def get_topic_cluster_context_for_seo_page(seo_slug):
    cluster = get_topic_cluster_for_seo_page(seo_slug)
    if not cluster:
        return None
    return _build_cluster_context(cluster, current_seo_slug=seo_slug)


def get_topic_clusters_with_content():
    return [_build_cluster_context(cluster) for cluster in TOPIC_CLUSTERS.values()]


def get_topic_clusters_for_keys(cluster_keys, current_tool_slug=None, current_seo_slug=None):
    clusters = []
    for cluster_key in cluster_keys:
        cluster = get_topic_cluster(cluster_key)
        if cluster:
            clusters.append(
                _build_cluster_context(
                    cluster,
                    current_tool_slug=current_tool_slug,
                    current_seo_slug=current_seo_slug,
                )
            )
    return clusters


def get_discovery_seo_hub_pages():
    pages = []
    for cluster in TOPIC_CLUSTERS.values():
        cluster_pages = _get_seo_pages(cluster["seo_page_slugs"], limit=1)
        if cluster_pages:
            pages.append(cluster_pages[0])
    return pages


def _build_cluster_context(cluster, current_tool_slug=None, current_seo_slug=None):
    from .tool_catalog import get_tool_groups

    cluster_copy = deepcopy(cluster)
    cluster_copy["tools"] = _get_tools(cluster_copy["tool_slugs"], current_slug=current_tool_slug)
    cluster_copy["seo_pages"] = _get_seo_pages(cluster_copy["seo_page_slugs"], current_slug=current_seo_slug)
    cluster_copy["tool_count"] = len(cluster_copy["tools"])
    cluster_copy["seo_page_count"] = len(cluster_copy["seo_page_slugs"])
    available_catalog_anchors = {group["key"] for group in get_tool_groups()}
    cluster_copy["catalog_available"] = cluster_copy["catalog_anchor"] in available_catalog_anchors
    return cluster_copy


def _get_tools(slugs, current_slug=None):
    from .tool_catalog import get_tool

    tools = []
    for slug in slugs:
        if slug == current_slug:
            continue
        tool = get_tool(slug)
        if tool and tool.get("public_visibility"):
            tools.append(tool)
    return tools


def _get_seo_pages(slugs, current_slug=None, limit=None):
    from .seo_pages import get_seo_page

    pages = []
    for slug in slugs:
        if slug == current_slug:
            continue
        page = get_seo_page(slug)
        if page:
            pages.append(page)
        if limit and len(pages) >= limit:
            break
    return pages
