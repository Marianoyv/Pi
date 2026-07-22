from copy import deepcopy


REBUILD_DESCRIPTOR = "Independent software and research studio."
REBUILD_STATEMENT = "Think clearly. Build what matters."

REBUILD_NAV_ITEMS = [
    {"slug": "studio", "label": "Studio"},
    {"slug": "capabilities", "label": "Capabilities"},
    {"slug": "ad-products", "label": "Ad Products"},
    {"slug": "research", "label": "Research"},
    {"slug": "insights", "label": "Insights"},
    {"slug": "about", "label": "About"},
]


REBUILD_HOME_PAGE = {
    "slug": "home",
    "path": "/rebuild/",
    "title": REBUILD_STATEMENT,
    "meta_description": (
        "Pi Development is an independent software and research studio focused on software systems, "
        "artificial intelligence, automation, advertising technology, applied research, and complex technical problems."
    ),
    "hero": {
        "eyebrow": REBUILD_DESCRIPTOR,
        "title": REBUILD_STATEMENT,
        "body": "Pi Development studies complex problems and turns them into focused software, AI systems, and automation.",
        "primary_cta": {"label": "Bring a problem", "href": "/rebuild/contact/"},
        "secondary_cta": {"label": "Explore the studio", "href": "/rebuild/studio/"},
        "microcopy": "No formal brief required.",
    },
    "sections": [
        {
            "type": "proposition",
            "title": "Start with the problem.",
            "body": (
                "Technology only matters when it changes an outcome. We study the system, find the real constraint, "
                "and build only what the problem requires."
            ),
            "supporting_line": "No templates. No technology for its own sake.",
            "link": {"label": "How we work", "href": "/rebuild/studio/"},
        },
        {
            "type": "capabilities",
            "title": "What we work on.",
            "intro": "A focused set of technical disciplines, combined according to the problem.",
            "items": [
                {
                    "title": "Software systems",
                    "body": "Digital products, internal platforms, and operational tools built around real requirements.",
                },
                {
                    "title": "AI and automation",
                    "body": "Intelligent workflows that reduce repetitive work, improve decisions, and expand operational capacity.",
                },
                {
                    "title": "Advertising technology",
                    "body": "Custom ad products, publisher systems, creative technology, and campaign quality infrastructure.",
                },
            ],
            "link": {"label": "View capabilities", "href": "/rebuild/capabilities/"},
        },
        {
            "type": "method",
            "title": "A disciplined way to build.",
            "steps": [
                {
                    "name": "Understand",
                    "body": "Define the problem, the people affected, and the outcome that must change.",
                },
                {
                    "name": "Design",
                    "body": "Reduce complexity into a system that can be explained and tested.",
                },
                {
                    "name": "Build",
                    "body": "Create the smallest useful version capable of proving value.",
                },
                {
                    "name": "Evolve",
                    "body": "Measure real use, learn from it, and improve continuously.",
                },
            ],
            "link": {"label": "Inside the studio", "href": "/rebuild/studio/"},
        },
        {
            "type": "ad_products",
            "label": "Specialized practice",
            "title": "Advertising should be engineered.",
            "body": (
                "Pi develops advertising technology for publishers, media companies, and commercial teams that need "
                "more control over formats, delivery, quality, and monetization."
            ),
            "items": [
                "Creative technology",
                "Publisher systems",
                "Campaign quality",
                "Monetization workflows",
            ],
            "link": {"label": "Explore Ad Products", "href": "/rebuild/ad-products/"},
        },
        {
            "type": "research",
            "title": "Research before certainty.",
            "body": (
                "Pi Research explores emerging technologies, complex systems, and unresolved problems before their path "
                "to a product is obvious."
            ),
            "supporting_line": "Experiments, technical notes, prototypes, and structured problem analysis.",
            "link": {"label": "Explore research", "href": "/rebuild/research/"},
        },
        {
            "type": "insights",
            "title": "What we are learning.",
            "body": (
                "Notes on software, artificial intelligence, automation, advertising technology, systems, and product decisions."
            ),
            "link": {"label": "Read the insights", "href": "/rebuild/insights/"},
        },
        {
            "type": "final_cta",
            "title": "What needs to work better?",
            "body": "Tell us what is broken, repetitive, inefficient, difficult to scale, or still missing.",
            "link": {"label": "Bring a problem", "href": "/rebuild/contact/"},
        },
    ],
}


REBUILD_PAGES = {
    "studio": {
        "slug": "studio",
        "path": "/rebuild/studio/",
        "label": "The studio",
        "title": "Independent by design.",
        "intro": (
            "Pi Development is an independent software and research studio created to study difficult problems and "
            "build focused technical solutions."
        ),
        "meta_description": (
            "Pi Development is an independent software and research studio created to study difficult problems and "
            "build focused technical solutions."
        ),
        "sections": [
            {
                "type": "text",
                "title": "Why Pi exists",
                "paragraphs": [
                    "Pi begins with a simple belief: technology should help solve meaningful problems, not create more noise.",
                    (
                        "Software, artificial intelligence, and automation are tools. The real work is understanding the "
                        "system, selecting the right intervention, and changing the outcome."
                    ),
                ],
            },
            {
                "type": "principles",
                "title": "How Pi works",
                "items": [
                    {
                        "title": "Resolve before building.",
                        "body": "Every project begins with a real problem and a clearly defined outcome.",
                    },
                    {
                        "title": "Evidence over opinion.",
                        "body": "Ideas are welcome. Decisions must be supported by observation, data, or testing.",
                    },
                    {
                        "title": "Automate the repetitive.",
                        "body": "Repeated work should become a system when automation creates a meaningful benefit.",
                    },
                    {
                        "title": "Create shared value.",
                        "body": (
                            "A strong solution should benefit the people using it, the organization supporting it, "
                            "and the system around it."
                        ),
                    },
                ],
            },
            {
                "type": "text",
                "title": "Operating model",
                "paragraphs": [
                    (
                        "Pi combines research, product thinking, engineering, and continuous improvement. Each engagement "
                        "begins by understanding the problem before selecting the technology."
                    )
                ],
            },
            {
                "type": "list",
                "title": "Current focus",
                "items": [
                    "Software systems",
                    "Artificial intelligence",
                    "Automation",
                    "Advertising technology",
                    "Applied research",
                ],
            },
        ],
        "cta": {"label": "Bring a problem", "href": "/rebuild/contact/"},
    },
    "capabilities": {
        "slug": "capabilities",
        "path": "/rebuild/capabilities/",
        "label": "Capabilities",
        "title": "Technology shaped around the problem.",
        "intro": (
            "Pi combines software engineering, artificial intelligence, automation, and systems thinking to build focused "
            "solutions for complex operational needs."
        ),
        "meta_description": (
            "Pi combines software engineering, artificial intelligence, automation, and systems thinking to build focused "
            "solutions for complex operational needs."
        ),
        "sections": [
            {
                "type": "list_with_copy",
                "title": "Software systems",
                "body": (
                    "Custom digital products, internal platforms, operational tools, and software infrastructure designed "
                    "around how an organization actually works."
                ),
                "items": [
                    "MVP architecture and development",
                    "Internal tools",
                    "Business platforms",
                    "Dashboards",
                    "APIs and integrations",
                    "Workflow systems",
                    "Data-driven applications",
                ],
            },
            {
                "type": "list_with_copy",
                "title": "AI and automation",
                "body": (
                    "Systems that reduce repetitive work, improve access to information, assist decisions, and expand "
                    "what teams can accomplish."
                ),
                "items": [
                    "AI-assisted workflows",
                    "Process automation",
                    "Knowledge systems",
                    "Intelligent internal tools",
                    "Data processing",
                    "Operational agents",
                    "Human-in-the-loop systems",
                ],
            },
            {
                "type": "list_with_copy",
                "title": "Technical problem solving",
                "body": (
                    "Research, diagnosis, architecture, and implementation for technical problems that do not fit inside "
                    "a standard service package."
                ),
                "items": [
                    "Technical discovery",
                    "System architecture",
                    "Process analysis",
                    "Prototyping",
                    "Performance investigation",
                    "Integration planning",
                    "Product validation",
                ],
            },
        ],
        "closing": {
            "title": "Bring the problem, not the specification.",
            "body": (
                "A complete technical brief is not required. Pi can begin with the problem, the current constraints, "
                "and the outcome that needs to change."
            ),
            "cta": {"label": "Discuss a problem", "href": "/rebuild/contact/"},
        },
    },
    "ad-products": {
        "slug": "ad-products",
        "path": "/rebuild/ad-products/",
        "label": "Ad Products",
        "title": "Advertising should be engineered.",
        "intro": (
            "Pi develops custom advertising technology for publishers, media companies, and commercial teams that need "
            "more control over formats, delivery, quality, and monetization."
        ),
        "meta_description": (
            "Pi develops custom advertising technology for publishers, media companies, and commercial teams that need "
            "more control over formats, delivery, quality, and monetization."
        ),
        "sections": [
            {
                "type": "list_with_copy",
                "title": "Creative technology",
                "body": (
                    "Custom advertising experiences built beyond standard display formats, with attention to interaction, "
                    "delivery, performance, compatibility, and measurement."
                ),
                "items": [
                    "Rich media",
                    "Custom display formats",
                    "Interactive creatives",
                    "Video experiences",
                    "Responsive advertising",
                    "Creative delivery systems",
                ],
            },
            {
                "type": "list_with_copy",
                "title": "Publisher systems",
                "body": (
                    "Technical systems that help publishers manage, deliver, inspect, and improve advertising across their "
                    "digital properties."
                ),
                "items": [
                    "Google Ad Manager integrations",
                    "GPT implementations",
                    "Ad slot architecture",
                    "Publisher QA",
                    "Monetization workflows",
                    "Ad delivery diagnostics",
                ],
            },
            {
                "type": "list_with_copy",
                "title": "Campaign quality",
                "body": (
                    "Tools and processes for validating advertising behavior before issues reach users, publishers, or "
                    "commercial teams."
                ),
                "items": [
                    "Creative validation",
                    "Tracking verification",
                    "Click testing",
                    "Rendering checks",
                    "SafeFrame compatibility",
                    "Campaign diagnostics",
                ],
            },
            {
                "type": "text",
                "title": "Custom Ad Products",
                "paragraphs": [
                    (
                        "When a commercial idea cannot be implemented with an existing format, Pi can research and develop "
                        "the system required to make it possible."
                    )
                ],
            },
        ],
        "closing": {
            "title": "Need an ad product that does not exist yet?",
            "cta": {"label": "Describe the requirement", "href": "/rebuild/contact/"},
        },
    },
    "research": {
        "slug": "research",
        "path": "/rebuild/research/",
        "label": "Research",
        "title": "Research before certainty.",
        "intro": (
            "Pi studies emerging technologies, complex systems, and unresolved problems before their path to a product is obvious."
        ),
        "meta_description": (
            "Pi studies emerging technologies, complex systems, and unresolved problems before their path to a product is obvious."
        ),
        "sections": [
            {
                "type": "principles",
                "title": "What belongs here",
                "items": [
                    {
                        "title": "Experiments",
                        "body": "Small technical tests used to validate an assumption or explore a capability.",
                    },
                    {
                        "title": "Research notes",
                        "body": "Structured observations about technologies, systems, and unresolved questions.",
                    },
                    {
                        "title": "Prototypes",
                        "body": "Early implementations designed to make an idea testable.",
                    },
                    {
                        "title": "Challenges",
                        "body": (
                            "Problems that may require collaboration across engineering, research, industry, and society."
                        ),
                    },
                ],
            },
            {
                "type": "text",
                "title": "Research principles",
                "paragraphs": [
                    (
                        "Research should produce clearer questions, useful evidence, reusable knowledge, or a path toward "
                        "implementation."
                    )
                ],
            },
            {
                "type": "text",
                "title": "Future direction",
                "paragraphs": [
                    (
                        "Pi intends to develop an environment where engineers, researchers, and specialists can contribute "
                        "structured ideas toward difficult technical and societal problems."
                    )
                ],
                "label": "Concept under development",
            },
        ],
    },
    "insights": {
        "slug": "insights",
        "path": "/rebuild/insights/",
        "label": "Insights",
        "title": "Ideas become useful when they can be examined.",
        "intro": (
            "Technical writing on software, artificial intelligence, automation, advertising technology, systems, and product decisions."
        ),
        "meta_description": (
            "Technical writing on software, artificial intelligence, automation, advertising technology, systems, and product decisions."
        ),
        "sections": [],
        "articles": [],
    },
    "about": {
        "slug": "about",
        "path": "/rebuild/about/",
        "label": "About Pi",
        "title": "Built to become larger than its founder.",
        "intro": (
            "Pi Development is an independent studio created to build useful systems, develop technical knowledge, and grow "
            "into an organization capable of solving increasingly important problems."
        ),
        "meta_description": (
            "Pi Development is an independent studio created to build useful systems, develop technical knowledge, and grow "
            "into an organization capable of solving increasingly important problems."
        ),
        "sections": [
            {
                "type": "text",
                "title": "Mission",
                "paragraphs": [
                    (
                        "Build systems that solve real problems, reduce unnecessary friction, and expand what people and "
                        "organizations are able to accomplish."
                    )
                ],
            },
            {
                "type": "text",
                "title": "Long-term direction",
                "paragraphs": [
                    (
                        "Pi aims to evolve from an independent studio into a durable technology organization with products, "
                        "research, specialized teams, and the ability to support projects with measurable social and economic impact."
                    )
                ],
            },
            {
                "type": "list",
                "title": "Principles",
                "items": [
                    "Work toward a net positive outcome.",
                    "Be transparent about decisions, evidence, limitations, and mistakes.",
                    "Use data and observation instead of ego.",
                    "Create value that can be shared.",
                    "Learn through building, testing, and experience.",
                    "Automate repeated work when doing so improves the system.",
                    "Protect the purpose of the work from short-term incentives.",
                ],
            },
            {
                "type": "text",
                "title": "Founder",
                "paragraphs": [
                    (
                        "Pi Development was founded by Mariano Tami, a software builder and AdTech specialist working across "
                        "web development, automation, advertising systems, and digital product engineering."
                    )
                ],
            },
        ],
    },
    "contact": {
        "slug": "contact",
        "path": "/rebuild/contact/",
        "label": "Contact",
        "title": "Bring a problem.",
        "intro": (
            "Explain what is not working, what is repeated too often, what needs to scale, or what does not exist yet."
        ),
        "meta_description": (
            "Explain what is not working, what is repeated too often, what needs to scale, or what does not exist yet."
        ),
        "microcopy": "No formal brief required.",
        "sections": [],
    },
}


def get_rebuild_page(slug="home"):
    if slug == "home":
        return deepcopy(REBUILD_HOME_PAGE)
    page = REBUILD_PAGES.get(slug)
    return deepcopy(page) if page else None


def get_rebuild_nav_items():
    return deepcopy(REBUILD_NAV_ITEMS)
