from copy import deepcopy


TOPIC_CLUSTERS = {
    "creatividades": {
        "key": "creatividades",
        "title": "Grupo Creatividades",
        "description": "Validacion, preview y QA tecnico para creatividades HTML, display y tags publicitarios.",
        "catalog_anchor": "qa_preview",
        "catalog_label": "QA y vista previa",
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
        "title": "Grupo AdTech",
        "description": "Diagnostico de monetizacion visible, GPT, stack publicitario y lecturas iniciales de implementacion.",
        "catalog_anchor": "diagnostics",
        "catalog_label": "Diagnostico tecnico",
        "tool_slugs": ["adtech-debug-tool"],
        "seo_page_slugs": [
            "debug-anuncios-web",
            "debug-gpt-ads",
            "herramientas-adtech",
        ],
    },
    "seo-performance": {
        "key": "seo-performance",
        "title": "Grupo SEO / Performance",
        "description": "Auditoria tecnica de URLs, SEO on-page visible y snapshots cortos de respuesta y metadata.",
        "catalog_anchor": "diagnostics",
        "catalog_label": "Diagnostico tecnico",
        "tool_slugs": ["ai-auditor", "landing-performance-snapshot"],
        "seo_page_slugs": [
            "auditoria-tecnica-web",
            "analizar-seo-pagina",
        ],
    },
    "tracking": {
        "key": "tracking",
        "title": "Grupo Tracking",
        "description": "Etiquetado UTM, control de URLs de campana y orden operativo para tracking.",
        "catalog_anchor": "operations",
        "catalog_label": "Operacion y etiquetado",
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
    cluster_copy = deepcopy(cluster)
    cluster_copy["tools"] = _get_tools(cluster_copy["tool_slugs"], current_slug=current_tool_slug)
    cluster_copy["seo_pages"] = _get_seo_pages(cluster_copy["seo_page_slugs"], current_slug=current_seo_slug)
    cluster_copy["tool_count"] = len(cluster_copy["tool_slugs"])
    cluster_copy["seo_page_count"] = len(cluster_copy["seo_page_slugs"])
    return cluster_copy


def _get_tools(slugs, current_slug=None):
    from .tool_catalog import get_tool

    tools = []
    for slug in slugs:
        if slug == current_slug:
            continue
        tool = get_tool(slug)
        if tool:
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
