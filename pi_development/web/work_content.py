"""Central visibility and evidence registry for Pi Development work.

Commercial templates, case routes, structured data and sitemaps must use these
selectors instead of maintaining their own project lists.
"""

from copy import deepcopy


WORK_PAGE = {
    "language": "en",
    "seo_title": "Product & Software Case Studies | Pi Development",
    "meta_description": (
        "Published Pi Development work across product development, assisted commerce, browser software and AdTech."
    ),
    "eyebrow": "Selected work",
    "title": "Products and systems operating in the real world.",
    "description": (
        "Each case connects the original problem to the shipped solution, technical decisions and an observable result."
    ),
    "intro_title": "See the product, then inspect the decisions.",
    "intro": (
        "Public implementations, current interfaces and measured scope make the work concrete. Where usage data is "
        "available, it is separated from commercial outcomes that cannot be attributed."
    ),
    "notes": [
        "Every case links to a published implementation.",
        "Scope and results are stated separately.",
        "Traffic, revenue and conversion claims appear only when verified.",
    ],
    "cta_title": "Building a useful product or operational system?",
    "cta_text": "Share the current process, constraint and outcome the software should support.",
    "cta_label": "Discuss a project",
}


WORK_REGISTRY = [
    {
        "slug": "juno-metales",
        "name": "Juno Metales",
        "public_visibility": True,
        "featured": True,
        "indexable": True,
        "project_type": "Lean website MVP",
        "evidence_status": "Verified GA4 usage evidence",
        "supported_commercial_pillar": "Product Development",
        "internal_case_route_available": True,
        "external_link_available": True,
        "permission_status": "Permission confirmed",
        "current_status": "Operational with measured traffic since 2022",
        "home_status": "Live",
        "timeline_label": "2022—26",
        "category": "Website development, SEO and analytics",
        "summary": (
            "A lean website MVP with a durable SEO and analytics foundation, launched around September 2022."
        ),
        "home_summary": (
            "A lean website MVP that remained operational and continued attracting measured direct and organic traffic."
        ),
        "launch_date": "Around September 2022",
        "date_published": "2022-09",
        "context": (
            "Juno Metales needed a complete website and a practical foundation for discovery and measurement."
        ),
        "problem": (
            "The project needed to establish a useful digital presence, make the business easier to discover and "
            "start measuring site usage without expanding beyond a lean first release."
        ),
        "constraints": (
            "The initial budget was relatively small, so delivery was deliberately scoped as a lean MVP. "
            "The actual development price is private."
        ),
        "role": (
            "Mariano Tami, through Pi Development, built the complete website and led website development, SEO, "
            "analytics and the related implementation work."
        ),
        "what_built": (
            "A complete public website with a focused information structure, responsive implementation, "
            "search-oriented foundations and measurement in place."
        ),
        "seo_analytics": (
            "The MVP included an SEO foundation and GA4 measurement so discovery and usage could be observed over time."
        ),
        "delivery_approach": (
            "The work prioritized the smallest maintainable release that could launch, remain useful and provide "
            "evidence for later improvement."
        ),
        "result": (
            "The lean MVP remained operational and continued attracting direct and organic traffic over several years. "
            "GA4 recorded more than 4.8K users, 6K sessions and 7.6K page views across the available reporting period."
        ),
        "metrics": [
            {"value": "4.8K+", "label": "users"},
            {"value": "6K+", "label": "sessions"},
            {"value": "7.6K+", "label": "page views"},
            {"value": "2.6K+", "label": "organic-search sessions"},
        ],
        "evidence_period": "Available GA4 reporting period from 2022 through July 2026",
        "context_heading": "A durable lean MVP.",
        "build_heading": "Complete website MVP",
        "supporting_work_label": "SEO and analytics",
        "supporting_work_title": "Discovery and measurement",
        "result_heading": "Sustained measured traffic since 2022",
        "evidence_eyebrow": "Verifiable usage evidence",
        "evidence_title": "Conservative rounded GA4 metrics.",
        "evidence_boundaries": [
            "The figures describe measured website usage, not attributed business revenue.",
            "No leads, sales, conversions, ROI or customer-growth result is claimed.",
            "The evidence does not establish that every visit resulted from Pi Development's SEO work.",
            "GA4 users are website users and are not described as customers.",
        ],
        "technologies": ["Web development", "SEO foundation", "Google Analytics", "Responsive implementation"],
        "image": "web/img/juno.mp4",
        "media_type": "responsive_video",
        "mobile_image": "web/img/juno-mobile.png",
        "poster": "web/img/5.png",
        "external_url": "https://junometales.com/",
    },
    {
        "slug": "arcade-world",
        "name": "Arcade World",
        "public_visibility": True,
        "featured": True,
        "indexable": True,
        "project_type": "Browser arcade product",
        "evidence_status": "Public implementation and product scope verified",
        "supported_commercial_pillar": "Product Development",
        "internal_case_route_available": True,
        "external_link_available": True,
        "permission_status": "Owner-approved public case",
        "current_status": "Live public product",
        "home_status": "Live",
        "timeline_label": "LIVE / 2026",
        "category": "Game discovery, browser emulation and local-first library",
        "summary": (
            "A retro browser arcade that turns a 50-game catalog into a searchable, playable and installable product."
        ),
        "home_summary": (
            "A 50-game browser arcade with search, category filters, local favorites, ROM import and six supported systems."
        ),
        "launch_date": "Current public product reviewed August 2026",
        "date_published": "2026-08",
        "context": (
            "Classic browser games are often scattered across provider pages, while local ROM play, discovery and "
            "personal libraries live in separate tools."
        ),
        "problem": (
            "The product needed to make a large retro catalog easy to explore without hiding the difference between "
            "external cabinets, local files and creator-approved downloads."
        ),
        "constraints": (
            "Commercial ROMs cannot be bundled, external providers can introduce ads and browser storage must remain "
            "local to the device. Each play mode therefore needs a visible boundary."
        ),
        "role": (
            "Pi Development designed and built the product structure, responsive interface, game catalog, local "
            "library behavior, browser-player flows, editorial system and Firebase deployment."
        ),
        "what_built": (
            "A searchable game room with category and mode filters, an installable PWA, an instant-play cabinet, "
            "favorites and recent sessions, local ROM import, homebrew discovery and indexed game and guide pages."
        ),
        "seo_analytics": (
            "Game detail pages and editorial guides create indexable discovery paths, while the manifest and local "
            "library make the experience useful beyond a single visit."
        ),
        "delivery_approach": (
            "The interface labels external-provider, own-player and import flows separately. ROM files stay on the "
            "user's device; only library metadata and preferences are stored locally."
        ),
        "result": (
            "A live arcade product with 50 catalog entries, six listed emulator systems and a coherent path from "
            "discovery to browser play or a local session—without requiring an account."
        ),
        "metrics": [
            {"value": "50", "label": "catalog games"},
            {"value": "6", "label": "supported systems"},
            {"value": "3", "label": "clearly separated play paths"},
            {"value": "0", "label": "accounts required"},
        ],
        "evidence_period": "Public implementation reviewed on 23 August 2026",
        "context_heading": "One room for discovery and play.",
        "build_heading": "A complete browser arcade",
        "supporting_work_label": "Discovery and retention",
        "supporting_work_title": "Catalog, guides and a local library",
        "result_heading": "Fifty games across six supported systems",
        "evidence_eyebrow": "Observable product scope",
        "evidence_title": "Capabilities visible in the live product.",
        "evidence_boundaries": [
            "The figures describe published product scope, not traffic, retention or commercial performance.",
            "Some catalog items use an external provider; others require a local ROM that the user is allowed to use.",
            "Arcade World does not bundle or upload commercial ROM files.",
            "No claim is made about emulator compatibility for every file, browser or device.",
        ],
        "technologies": ["HTML", "CSS", "JavaScript", "EmulatorJS", "PWA", "Firebase Hosting"],
        "image": "web/img/arcade-world-desktop.jpg",
        "poster": "web/img/arcade-world-desktop.jpg",
        "desktop_image": "web/img/arcade-world-desktop.jpg",
        "mobile_image": "web/img/arcade-world-mobile.jpg",
        "media_type": "project_screenshots",
        "external_url": "https://arcade-world.web.app/",
    },
    {
        "slug": "blog-int-emocional",
        "name": "Blog Int Emocional",
        "public_visibility": False,
        "featured": False,
        "indexable": False,
        "project_type": "Draft project record",
        "evidence_status": "Insufficient verified public evidence",
        "supported_commercial_pillar": "Product Development",
        "internal_case_route_available": False,
        "external_link_available": False,
        "permission_status": "Not approved for this batch",
        "current_status": "Private draft",
    },
    {
        "slug": "recetas-del-sapi",
        "name": "A mano",
        "public_visibility": True,
        "featured": True,
        "indexable": True,
        "project_type": "Recipe discovery and food information product",
        "evidence_status": "Public implementation and launch scope verified",
        "supported_commercial_pillar": "Product Development",
        "internal_case_route_available": True,
        "external_link_available": True,
        "permission_status": "Owner-approved public case",
        "current_status": "Newly launched public product",
        "home_status": "Newly launched",
        "timeline_label": "LIVE / SEP 2026",
        "category": "Ingredient-led recipe discovery, nutritional data and sourced editorial content",
        "summary": (
            "A practical cooking product that turns ingredients already at home into recipes, with nutritional "
            "estimates readers can trace to their sources."
        ),
        "home_summary": (
            "A recipe finder built around what is already in the kitchen, supported by reproducible nutritional "
            "estimates and primary-source references."
        ),
        "launch_date": "September 2026",
        "date_published": "2026-09",
        "context": (
            "The everyday question of what to cook with available ingredients is usually separated from the work of "
            "checking quantities, nutritional estimates and the source behind a food claim."
        ),
        "problem": (
            "The product needed to make the next meal easier to choose while keeping useful food information "
            "inspectable, appropriately qualified and close to each recipe."
        ),
        "constraints": (
            "This is an early public release with a deliberately small catalog. Recipes were prepared with AI "
            "assistance and have not yet been kitchen-tested; nutritional values are estimates based on referenced "
            "ingredient records, not measurements of the finished dish or personal dietary advice."
        ),
        "role": (
            "Pi Development defined, designed and built the product, including its content model, ingredient finder, "
            "nutrition calculation pipeline, editorial structure, responsive interface and Firebase deployment."
        ),
        "what_built": (
            "A responsive recipe finder that works from ingredients on hand, a ten-recipe launch catalog with clear "
            "quantities and steps, per-portion nutritional estimates, editorial explainers and a browsable source record."
        ),
        "seo_analytics": (
            "Indexable recipe and editorial pages connect to a documented methodology, original references and a "
            "downloadable nutrition dataset. Analytics remains inactive until the visitor explicitly consents."
        ),
        "delivery_approach": (
            "Cooking guidance, nutritional estimates and official recommendations are kept distinct. Ingredient state, "
            "calculation rules, missing values and known limitations are documented so the information can be checked."
        ),
        "result": (
            "A newly launched public product that makes an everyday pantry searchable and connects each recipe to "
            "practical instructions, transparent estimates and the underlying information sources."
        ),
        "metrics": [
            {"value": "10", "label": "launch recipes"},
            {"value": "21", "label": "referenced foods"},
            {"value": "19", "label": "nutrition fields"},
            {"value": "5", "label": "food explainers"},
        ],
        "evidence_period": "Public implementation reviewed on 14 September 2026",
        "context_heading": "A daily decision made easier.",
        "build_heading": "Recipes from what is already at hand",
        "supporting_work_label": "Methodology and sources",
        "supporting_work_title": "Useful information that can be checked",
        "result_heading": "A transparent first public release",
        "evidence_eyebrow": "Observable launch scope",
        "evidence_title": "Published capabilities, without premature performance claims.",
        "evidence_boundaries": [
            "The figures describe the scope of the first public release, not traffic, adoption or commercial performance.",
            "Recipes in this edition were produced with AI assistance and have not yet been tested in a kitchen.",
            "Nutritional values are estimates derived from referenced ingredient data and do not measure the finished dish.",
            "The content does not replace personalized medical or nutritional advice.",
        ],
        "technologies": ["Astro", "JavaScript", "Structured food data", "Responsive UX", "Firebase Hosting"],
        "image": "web/img/recetas-del-sapi-desktop.png",
        "poster": "web/img/recetas-del-sapi-desktop.png",
        "desktop_image": "web/img/recetas-del-sapi-desktop.png",
        "mobile_image": "web/img/recetas-del-sapi-mobile.png",
        "media_type": "project_screenshots",
        "external_url": "https://recetasdelsapi.web.app/",
    },
    {
        "slug": "indices-argentinos",
        "name": "Índices Argentinos",
        "public_visibility": True,
        "featured": True,
        "indexable": True,
        "project_type": "Live financial tool suite",
        "evidence_status": "Public implementation and functional scope verified",
        "supported_commercial_pillar": "Operational Software",
        "internal_case_route_available": True,
        "external_link_available": True,
        "permission_status": "Owner-approved public case",
        "current_status": "Live public product",
        "home_status": "Live",
        "timeline_label": "LIVE / 2026",
        "category": "Financial calculators, public data and browser-side tools",
        "summary": (
            "A fast public suite of financial calculators and Argentine index tools built with transparent formulas."
        ),
        "home_summary": (
            "Twelve browser-based calculators plus IPC and ICL tools that turn public financial data into clear, repeatable answers."
        ),
        "launch_date": "Public implementation reviewed August 2026",
        "date_published": "2026-08",
        "context": (
            "People regularly need to resolve interest, loan, rate, percentage, tax and index-adjustment questions "
            "without navigating spreadsheets or opaque financial interfaces."
        ),
        "problem": (
            "The product needed to make common Argentine financial calculations approachable while keeping formulas, "
            "data sources and limitations visible to the user."
        ),
        "constraints": (
            "The experience had to remain fast, mobile-first and understandable without a framework-heavy frontend or "
            "a server round trip for each calculation."
        ),
        "role": (
            "Pi Development designed and produced the public product, its calculator system, content structure, "
            "responsive interface and deployment architecture."
        ),
        "what_built": (
            "A suite of 12 financial calculators covering interest, loans, rates, percentages, VAT and returns, "
            "plus dedicated IPC and ICL adjustment experiences."
        ),
        "seo_analytics": (
            "The interface explains its methodology and data sources, uses official public IPC and ICL references, "
            "and keeps deterministic calculations inside the browser."
        ),
        "delivery_approach": (
            "The product uses a reusable calculator pattern and a lightweight HTML, CSS and JavaScript foundation so "
            "new tools can be added without compromising speed or clarity."
        ),
        "result": (
            "A live, mobile-ready product where users can access 12 financial calculators, official-index adjustment "
            "tools, methodology and source information from one coherent system."
        ),
        "metrics": [
            {"value": "12", "label": "financial calculators"},
            {"value": "2", "label": "official index tools"},
            {"value": "100%", "label": "browser-side calculations"},
            {"value": "0", "label": "frontend frameworks"},
        ],
        "evidence_period": "Public implementation reviewed on 22 August 2026",
        "context_heading": "Useful financial answers without the friction.",
        "build_heading": "A reusable calculator system",
        "supporting_work_label": "Methodology and data",
        "supporting_work_title": "Transparent by design",
        "result_heading": "Fourteen focused public tools in one system",
        "evidence_eyebrow": "Verifiable product scope",
        "evidence_title": "Capabilities visible in the live implementation.",
        "evidence_boundaries": [
            "The figures describe product scope, not traffic, adoption or commercial outcomes.",
            "Financial results are deterministic estimates and do not replace professional advice or contractual terms.",
            "IPC and ICL coverage depends on the public source ranges documented by the product.",
            "No claim is made about user volume, conversion or revenue impact.",
        ],
        "technologies": ["HTML", "CSS", "JavaScript", "Public index data", "Firebase Hosting"],
        "image": "web/img/indices-desktop.webp",
        "media_type": "responsive_image",
        "poster": "web/img/indices-desktop.webp",
        "external_url": "https://indices-argentinos.web.app/",
    },
    {
        "slug": "taitet",
        "name": "Taitet",
        "public_visibility": True,
        "featured": True,
        "indexable": True,
        "project_type": "Assisted commerce platform",
        "evidence_status": "Public implementation and purchase flow verified",
        "supported_commercial_pillar": "Product Development",
        "internal_case_route_available": True,
        "external_link_available": True,
        "permission_status": "Owner-approved public case",
        "current_status": "Live commercial platform",
        "home_status": "Live",
        "timeline_label": "LIVE / 2026",
        "category": "Assisted commerce, product catalog and lead qualification",
        "summary": (
            "A made-to-measure curtain platform that helps buyers move from an uncertain need to a useful product and price reference."
        ),
        "home_summary": (
            "A guided commerce experience connecting product discovery, room-based recommendations, indicative pricing and human advice."
        ),
        "launch_date": "Current public product reviewed August 2026",
        "date_published": "2026-08",
        "context": (
            "Buying custom curtains requires decisions about room, light, fabric, system, dimensions, installation and budget before a final visit."
        ),
        "problem": (
            "A conventional brochure site would show products but leave buyers without enough context to choose a direction or prepare a useful inquiry."
        ),
        "constraints": (
            "Online measurements and prices can only be indicative. Final commercial and technical decisions still depend on an in-person measurement and advice."
        ),
        "role": (
            "Pi Development designed and produced the public platform, product model, responsive interface, guided advisor, quotation flow and deployment."
        ),
        "what_built": (
            "A responsive catalog with category and product-detail pages, selection and quote flows, a room-and-goal-based advisor, indicative cost breakdowns and direct advisor contact."
        ),
        "seo_analytics": (
            "Structured product pages expose fabrics, variants, compatible systems, lead times and service details while keeping consultation calls to action close to each decision."
        ),
        "delivery_approach": (
            "The product gives the buyer a concrete initial reference, then makes the handoff explicit: visit, real measurement and final proposal remain part of the service."
        ),
        "result": (
            "A live assisted-commerce system that lets buyers compare four current product options, explore five room contexts and prepare a more informed quotation request."
        ),
        "metrics": [
            {"value": "4", "label": "current catalog products"},
            {"value": "5", "label": "room presets"},
            {"value": "3", "label": "service stages"},
            {"value": "1", "label": "guided recommendation flow"},
        ],
        "evidence_period": "Public implementation reviewed on 23 August 2026",
        "context_heading": "Custom products need guided decisions.",
        "build_heading": "An assisted buying journey",
        "supporting_work_label": "Catalog and handoff",
        "supporting_work_title": "Product detail connected to advice",
        "result_heading": "A clearer path from room to quotation",
        "evidence_eyebrow": "Observable product scope",
        "evidence_title": "Capabilities visible in the live platform.",
        "evidence_boundaries": [
            "The figures describe current catalog and workflow scope, not sales, leads or conversion performance.",
            "Indicative prices depend on entered measurements and the current catalog configuration.",
            "Final price, fabric, system and installation are confirmed after professional measurement and advice.",
            "No traffic, revenue or customer-growth outcome is claimed.",
        ],
        "technologies": ["React", "Vite", "Firebase", "Responsive commerce UX"],
        "image": "web/img/taitet-desktop.jpg",
        "poster": "web/img/taitet-desktop.jpg",
        "desktop_image": "web/img/taitet-desktop.jpg",
        "mobile_image": "web/img/taitet-mobile.jpg",
        "media_type": "project_screenshots",
        "external_url": "https://taitet.com/",
    },
]


# The home is intentionally selective: these cases demonstrate the broadest
# combination of product logic, interface design, integrations and operational scope.
HOME_FEATURED_WORK_SLUGS = (
    "taitet",
    "arcade-world",
    "indices-argentinos",
)


def _prepare(item):
    prepared = deepcopy(item)
    prepared["internal_url"] = f"/work/{item['slug']}/"
    return prepared


def get_work_page():
    return deepcopy(WORK_PAGE)


def get_work_registry():
    return [_prepare(item) for item in WORK_REGISTRY]


def get_public_work_items():
    return [item for item in get_work_registry() if item["public_visibility"]]


def get_featured_work_items():
    return [item for item in get_public_work_items() if item["featured"]]


def get_home_featured_work_items():
    public_items = {item["slug"]: item for item in get_public_work_items()}
    return [public_items[slug] for slug in HOME_FEATURED_WORK_SLUGS if slug in public_items]


def get_indexable_work_case_slugs():
    return [
        item["slug"]
        for item in get_public_work_items()
        if item["indexable"] and item["internal_case_route_available"]
    ]


def get_work_case(slug):
    for item in get_public_work_items():
        if item["slug"] == slug and item["internal_case_route_available"]:
            return item
    return None


def get_related_work_items(commercial_pillar, exclude_slug=None):
    return [
        item
        for item in get_public_work_items()
        if item["supported_commercial_pillar"] == commercial_pillar and item["slug"] != exclude_slug
    ]


# Backwards-compatible selector used by the Work index view.
def get_work_items():
    return get_public_work_items()
