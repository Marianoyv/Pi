"""Structured work entries kept separate from services, tools and articles."""

from copy import deepcopy


WORK_PAGE = {
    "language": "en",
    "seo_title": "Selected Software Work | Pi Development",
    "meta_description": (
        "Selected software work from Pi Development across discovery platforms, editorial systems, financial "
        "data interfaces and custom web platforms."
    ),
    "eyebrow": "Selected work",
    "title": "Software designed around a clear purpose.",
    "description": (
        "Published implementations explained through context, problem, approach, technical decisions and "
        "observable result—without invented metrics or client claims."
    ),
    "intro_title": "What this work demonstrates",
    "intro": (
        "Each project starts from a different content, data or commercial problem. The common thread is a clear "
        "information model, responsive interaction and a base that can be maintained after launch."
    ),
    "notes": [
        "Project type and status are stated explicitly.",
        "Results describe what was built and made possible, not unsupported growth claims.",
        "External links are included only where a published implementation is available.",
    ],
    "cta_title": "Have a product, workflow or platform that needs a clearer system?",
    "cta_text": "Share the current problem and the outcome the software should support.",
    "cta_label": "Discuss a project",
}


WORK_ITEMS = [
    {
        "slug": "arcade-world",
        "name": "Arcade World",
        "work_type": "Independent product",
        "status": "Published",
        "category": "Catalog and discovery platform",
        "summary": (
            "A catalog and discovery platform built around content hierarchy, visual exploration and responsive "
            "interaction."
        ),
        "context": "An entertainment catalog needed a strong visual identity without losing navigation clarity.",
        "problem": (
            "A dense catalog can become difficult to scan when atmosphere, hierarchy and responsive behavior are "
            "treated as separate concerns."
        ),
        "approach": (
            "Structure the experience around stable content entry points, controlled visual layers and consistent "
            "discovery patterns."
        ),
        "what_built": (
            "A responsive catalog interface with modular sections, visual exploration and reusable content patterns."
        ),
        "technical_decisions": (
            "A component-based frontend and constrained media treatment keep hierarchy and interaction predictable "
            "across viewport sizes."
        ),
        "result": (
            "A live platform where the catalog can expand without changing the core discovery model."
        ),
        "technologies": ["Custom frontend", "Responsive UI", "Content architecture"],
        "image": "web/img/arcade.mp4",
        "media_type": "video",
        "poster": "web/img/1.png",
        "url": "https://arcade-world.web.app/",
    },
    {
        "slug": "blog-int-emocional",
        "name": "Blog Int Emocional",
        "work_type": "Independent project",
        "status": "Published",
        "category": "Editorial system",
        "summary": (
            "An editorial system structured for long-form publishing, organic discovery and maintainable content growth."
        ),
        "context": "A long-form publication needed stronger reading structure and a foundation for continued publishing.",
        "problem": (
            "Editorial growth becomes fragile when articles, navigation and discovery do not share a consistent "
            "information architecture."
        ),
        "approach": (
            "Prioritize semantic hierarchy, readable content blocks, topic continuity and simple navigation."
        ),
        "what_built": (
            "A maintainable publishing interface with structured article pages and clear routes into related content."
        ),
        "technical_decisions": (
            "Content structure and on-page SEO are handled in the rendered document so important copy remains "
            "readable to people and search engines."
        ),
        "result": "A published editorial base that can support more long-form content without redesigning each article.",
        "technologies": ["Semantic HTML", "Editorial architecture", "On-page SEO"],
        "image": "web/img/2.png",
        "url": "https://blogintemocional.web.app/index.html",
    },
    {
        "slug": "indices-argentinos",
        "name": "Índices Argentinos",
        "work_type": "Independent product",
        "status": "Published",
        "category": "Financial data interface",
        "summary": (
            "A financial data interface designed to make economic indicators easier to scan, compare and understand."
        ),
        "context": "Economic indicators needed a compact interface for fast comparison without unnecessary visual noise.",
        "problem": "Dense financial information becomes harder to use when hierarchy and comparison are not explicit.",
        "approach": "Organize indicators around scanability, consistent grouping and restrained visual emphasis.",
        "what_built": "A responsive data interface for browsing and comparing Argentine economic indicators.",
        "technical_decisions": (
            "Table, metric and summary patterns use a shared hierarchy so new indicators can be added consistently."
        ),
        "result": "A live reference interface that makes multiple indicators easier to inspect from one place.",
        "technologies": ["Data interface", "Responsive tables", "Information design"],
        "image": "web/img/indices.png",
        "url": "https://indices-argentinos.web.app/",
    },
    {
        "slug": "recetas-del-sapi",
        "name": "Recetas del Sapi",
        "work_type": "Independent project",
        "status": "Published",
        "category": "Content platform",
        "summary": "A structured content experience for recipe discovery, categories and continued editorial growth.",
        "context": "A recipe project needed a clear way to organize entries and support continued browsing.",
        "problem": "Content was difficult to sustain without stable category and article patterns.",
        "approach": "Use repeatable content modules, readable entry pages and clear category routes.",
        "what_built": "A published recipe platform with a reusable content structure.",
        "technical_decisions": "Shared page patterns reduce the amount of one-off layout work required for new entries.",
        "result": "A maintainable content base that can grow through additional recipes and categories.",
        "technologies": ["Content architecture", "Responsive frontend", "Reusable templates"],
        "image": "web/img/recetas.png",
        "url": "https://recetasdelsapi.web.app/",
    },
    {
        "slug": "juno-metales",
        "name": "Juno Metales",
        "work_type": "Published implementation",
        "status": "Published",
        "category": "Industrial company platform",
        "summary": "A focused B2B platform for presenting an industrial offer and creating clear contact paths.",
        "context": "An industrial business needed a more structured digital presence for its offer and commercial entry points.",
        "problem": "Technical credibility and service clarity were difficult to communicate in an unstructured presentation.",
        "approach": "Use restrained visual hierarchy, concrete service language and direct contact routes.",
        "what_built": "A responsive company platform with organized service content and commercial calls to action.",
        "technical_decisions": "A compact multipage structure keeps the offer understandable without decorative complexity.",
        "result": "A live platform that presents the business offer and contact path in one coherent system.",
        "technologies": ["Multipage frontend", "Responsive UI", "B2B information architecture"],
        "image": "web/img/juno.mp4",
        "media_type": "video",
        "poster": "web/img/5.png",
        "url": "https://junometales.com/",
    },
    {
        "slug": "system-vesta",
        "name": "System Vesta",
        "work_type": "Published implementation",
        "status": "Published",
        "category": "Services platform",
        "summary": "A multipage services platform built around technical clarity and consistent offer structure.",
        "context": "A services business needed a dependable base for explaining its offer and process.",
        "problem": "The existing message needed clearer hierarchy and a more coherent multipage structure.",
        "approach": "Reduce noise, strengthen page relationships and keep the commercial narrative consistent.",
        "what_built": "A responsive multipage platform with reusable service and contact patterns.",
        "technical_decisions": "Shared templates and a stable navigation model prepare the site for deeper content over time.",
        "result": "A live, maintainable platform that presents the technical offer with clearer structure.",
        "technologies": ["Multipage architecture", "Responsive frontend", "Reusable components"],
        "image": "web/img/sistemvesta.mp4",
        "media_type": "video",
        "poster": "web/img/4.png",
        "url": "https://systemvesta.com/",
    },
]


def get_work_page():
    return deepcopy(WORK_PAGE)


def get_work_items():
    return deepcopy(WORK_ITEMS)
