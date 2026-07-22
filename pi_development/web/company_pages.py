"""Structured English content for Pi Development's commercial pages.

Templates render this module as the single source of truth for the current
English site. A future Spanish edition can provide the same schema without
duplicating copy in templates.
"""

from copy import deepcopy


HOME_PAGE = {
    "language": "en",
    "seo_title": "Custom Software & AdTech Development | Pi Development",
    "meta_description": (
        "Pi Development builds custom software, MVPs, AI automation and AdTech products for companies and "
        "digital publishers. Based in Buenos Aires, working globally."
    ),
    "hero": {
        "eyebrow": "Custom software development · AI automation · AdTech",
        "title": "We build software for problems worth solving.",
        "description": (
            "Pi Development turns product ideas, manual operations and monetization challenges into reliable "
            "software—from MVPs and internal platforms to AI workflows and publisher technology."
        ),
        "primary_cta": {"label": "Discuss a project", "href": "/contact/"},
        "secondary_cta": {"label": "Explore our work", "href": "/work/"},
        "location": "Based in Buenos Aires. Working globally.",
    },
    "audience": ["For founders", "Operational teams", "Digital publishers"],
    "what_we_solve": {
        "eyebrow": "What we solve",
        "title": "Different problems. The same standard.",
        "description": "Useful software that works in the real world.",
        "items": [
            {
                "title": "Launch a product",
                "text": (
                    "MVPs and custom web platforms designed to validate an idea, serve real users and evolve "
                    "without starting over."
                ),
                "href": "/solutions/#mvp-development",
            },
            {
                "title": "Improve an operation",
                "text": (
                    "Internal tools, integrations and AI automation that reduce manual work, errors and "
                    "operational delay."
                ),
                "href": "/solutions/#internal-tools",
            },
            {
                "title": "Build better publisher technology",
                "text": (
                    "AdTech products and technical systems for monetization, campaign operations, creative QA "
                    "and web performance."
                ),
                "href": "/adtech/",
            },
        ],
        "cta": {"label": "Explore solutions", "href": "/solutions/"},
    },
    "how_we_build": {
        "eyebrow": "How we build",
        "title": "Start with the problem. Keep only what creates value.",
        "description": (
            "We map the workflow, constraints and business outcome before choosing the architecture. Then we "
            "build the smallest complete system that can operate reliably, be measured and improve over time."
        ),
        "items": [
            {
                "title": "Define",
                "text": "Clarify the users, workflow, data, constraints and expected outcome.",
            },
            {
                "title": "Build",
                "text": "Connect product, engineering and automation in one coherent system.",
            },
            {
                "title": "Improve",
                "text": "Measure real use, remove friction and expand what proves valuable.",
            },
        ],
    },
    "why_pi": {
        "eyebrow": "Why Pi Development",
        "title": "One technical perspective from problem to production.",
        "description": (
            "Product thinking, software engineering, automation and operational context remain connected "
            "throughout the project. The result is less translation, fewer unnecessary layers and software "
            "that fits the work it was built for."
        ),
        "items": [
            {
                "title": "Direct technical ownership",
                "text": "The business problem and the implementation remain connected.",
            },
            {
                "title": "Purposeful technology",
                "text": (
                    "Architecture, AI and automation are selected because they create value—not because they "
                    "are fashionable."
                ),
            },
            {
                "title": "Production-minded delivery",
                "text": (
                    "Reliability, QA, maintainability and future iteration are considered from the beginning."
                ),
            },
        ],
    },
    "adtech": {
        "eyebrow": "Publisher technology",
        "title": "AdTech is not an add-on here.",
        "paragraphs": [
            "Pi Development works at the intersection of publisher monetization and web engineering.",
            (
                "We build custom ad products, Google Ad Manager and GPT solutions, creative QA tools, technical "
                "diagnostics, tracking systems and operational automation for publishers, AdOps and revenue teams."
            ),
        ],
        "cta": {"label": "Explore AdTech", "href": "/adtech/"},
    },
    "products": {
        "eyebrow": "Products",
        "title": "Products built from recurring problems.",
        "description": "Some problems should not be solved repeatedly. They should become products.",
        "items": [
            {
                "title": "AI Auditor",
                "text": (
                    "Turn a URL into a clear technical baseline for metadata, structure, discoverability and "
                    "improvement priorities."
                ),
                "cta": "Open AI Auditor",
                "href": "/tools/ai-auditor/",
            },
            {
                "title": "AdTech Debug Tool",
                "text": (
                    "Surface visible ad stack and monetization signals before beginning a deeper technical "
                    "investigation."
                ),
                "cta": "Open AdTech Debug Tool",
                "href": "/tools/adtech-debug-tool/",
            },
        ],
        "cta": {"label": "Explore all products", "href": "/products/"},
    },
    "selected_work": {
        "eyebrow": "Selected work",
        "title": "Software designed around a clear purpose.",
        "items": [
            {
                "slug": "arcade-world",
                "title": "Arcade World",
                "text": (
                    "A catalog and discovery platform built around content hierarchy, visual exploration and "
                    "responsive interaction."
                ),
            },
            {
                "slug": "blog-int-emocional",
                "title": "Blog Int Emocional",
                "text": (
                    "An editorial system structured for long-form publishing, organic discovery and "
                    "maintainable content growth."
                ),
            },
            {
                "slug": "indices-argentinos",
                "title": "Índices Argentinos",
                "text": (
                    "A financial data interface designed to make economic indicators easier to scan, compare "
                    "and understand."
                ),
            },
        ],
        "cta": {"label": "View selected work", "href": "/work/"},
    },
    "contact": {
        "eyebrow": "Contact",
        "title": "A real problem is enough to start.",
        "description": (
            "Tell us what needs to be launched, automated, repaired or made easier to operate. We will define "
            "the right system around it."
        ),
        "cta": {"label": "Bring us the problem", "href": "/contact/"},
    },
}


SOLUTIONS_PAGE = {
    "slug": "solutions",
    "language": "en",
    "seo_title": "Custom Software Development Services | Pi Development",
    "meta_description": (
        "Custom software development, MVP development, internal tools, integrations and AI automation from "
        "Pi Development in Buenos Aires, working globally."
    ),
    "eyebrow": "Solutions",
    "title": "Software built around the problem you need to solve.",
    "description": (
        "Launch an MVP, replace manual work, connect fragmented tools or improve an existing platform with "
        "custom software development shaped around real users and operations."
    ),
    "intro_title": "Start with the situation—not a technology label.",
    "intro": (
        "The right build may be a focused MVP, an internal tool, an integration layer or an AI-enabled workflow. "
        "We define the boundary from the outcome, the people involved and the work the software must support."
    ),
    "support_title": "Typical engagement",
    "support_text": (
        "Discovery, product definition, UX structure, engineering, QA and launch remain connected through one "
        "technical delivery path."
    ),
    "sections": [
        {
            "anchor": "mvp-development",
            "label": "Launch",
            "title": "MVP Development",
            "description": "A usable first product built to test the core value with real users.",
            "solves": "An idea needs evidence before a larger product investment.",
            "for_whom": "Founders, product teams and new ventures with a defined problem and an uncertain solution.",
            "builds": "Web applications, SaaS foundations, onboarding, account flows, dashboards and essential integrations.",
            "scope": "Product definition, architecture, interface, implementation, QA, launch and an iteration plan.",
        },
        {
            "anchor": "custom-platforms",
            "label": "Build",
            "title": "Custom Web Platforms",
            "description": "Purpose-built platforms for products, content, transactions or specialized operations.",
            "solves": "Off-the-shelf software cannot support the required workflow, experience or business logic.",
            "for_whom": "Companies that need a durable product surface rather than a generic website.",
            "builds": "Role-aware platforms, customer portals, structured content systems and data-backed applications.",
            "scope": "Discovery, information architecture, data model, frontend, backend, integrations, QA and deployment.",
        },
        {
            "anchor": "internal-tools",
            "label": "Operate",
            "title": "Internal Tools",
            "description": "Software that gives teams a clearer, safer way to run recurring work.",
            "solves": "Critical operations depend on spreadsheets, copy-paste, inboxes or disconnected interfaces.",
            "for_whom": "Operational, finance, content, support, AdOps and revenue teams.",
            "builds": "Dashboards, review queues, admin tools, approval systems and reporting interfaces.",
            "scope": "Workflow mapping, roles, data inputs, business rules, auditability, implementation and rollout.",
        },
        {
            "anchor": "process-automation",
            "label": "Automate",
            "title": "Business Process Automation",
            "description": "Controlled automation for repeatable work, handoffs and operational checks.",
            "solves": "Manual repetition creates delay, inconsistent output and avoidable errors.",
            "for_whom": "Teams with a stable recurring process and a clear human review boundary.",
            "builds": "Workflow automation, data processing, notifications, scheduled jobs and exception handling.",
            "scope": "Process analysis, automation design, implementation, safeguards, monitoring and documentation.",
        },
        {
            "anchor": "ai-workflows",
            "label": "Assist",
            "title": "AI-Enabled Workflows",
            "description": "AI applied inside a defined workflow where it can save time or improve access to information.",
            "solves": "Review, classification, summarization or routing work consumes time but still needs oversight.",
            "for_whom": "Teams with repeatable knowledge work, usable source data and a clear quality standard.",
            "builds": "GPT implementations, assisted review, retrieval, classification and human-in-the-loop workflows.",
            "scope": "Use-case definition, data boundaries, prompts, evaluation, interface, safeguards and operational QA.",
        },
        {
            "anchor": "integrations-data",
            "label": "Connect",
            "title": "Integrations and Data Systems",
            "description": "A reliable layer between tools, data sources and the people who depend on them.",
            "solves": "Information is fragmented, duplicated or moved manually between systems.",
            "for_whom": "Companies with growing tool stacks, recurring imports or reporting gaps.",
            "builds": "APIs, system integrations, data pipelines, synchronized records and operational dashboards.",
            "scope": "Source audit, data mapping, integration design, implementation, error handling and monitoring.",
        },
    ],
    "process": {
        "eyebrow": "Process",
        "title": "From unclear need to working software.",
        "items": [
            {"title": "Define", "text": "Map users, workflow, constraints, data and the outcome that must change."},
            {"title": "Design", "text": "Choose the smallest complete product boundary and make the workflow testable."},
            {"title": "Build", "text": "Implement product, engineering and automation as one coherent system."},
            {"title": "Improve", "text": "Use real operation and feedback to remove friction and expand proven value."},
        ],
    },
    "deliverables_title": "What a delivery can include",
    "deliverables": [
        "Problem definition, workflow map and product scope.",
        "UX structure, software architecture and implementation.",
        "Integrations, automation, data handling and QA.",
        "Deployment, technical documentation and an iteration plan.",
    ],
    "evidence_title": "Relevant work",
    "evidence": [
        {"label": "Catalog and discovery platform", "title": "Arcade World", "href": "/work/#arcade-world"},
        {"label": "Editorial system", "title": "Blog Int Emocional", "href": "/work/#blog-int-emocional"},
        {"label": "Financial data interface", "title": "Índices Argentinos", "href": "/work/#indices-argentinos"},
    ],
    "technology_title": "Technology follows the system",
    "technology_text": (
        "Python, Django, JavaScript, relational data, APIs, cloud infrastructure and AI services are selected "
        "only when they fit the product, operating model and maintenance needs."
    ),
    "faqs": [
        {
            "question": "Can Pi Development start from an idea rather than a technical specification?",
            "answer": "Yes. A problem, intended user and business outcome are enough to begin product definition.",
        },
        {
            "question": "Do you only build new products?",
            "answer": "No. Work can begin with an existing platform, workflow, integration or operation that needs improvement.",
        },
        {
            "question": "Where does AI fit?",
            "answer": "AI is used as an applied capability inside a defined workflow, with evaluation and human review where needed.",
        },
    ],
    "cta_title": "Bring the workflow, product idea or technical bottleneck.",
    "cta_text": "We will define the smallest reliable system that can create value and keep improving.",
    "cta_label": "Discuss a project",
}


PRODUCTS_PAGE = {
    "slug": "products",
    "language": "en",
    "seo_title": "Software Products & Public Tools | Pi Development",
    "meta_description": (
        "Explore live software products and public tools from Pi Development for technical audits, AdTech "
        "diagnostics, creative QA, campaign tracking and web performance."
    ),
    "eyebrow": "Products",
    "title": "Products built from recurring technical work.",
    "description": (
        "Pi Development turns repeated diagnostics, quality checks and operational tasks into accessible software."
    ),
    "intro_title": "Only usable products are published.",
    "intro": (
        "Every item below has a working public interface. Experimental work remains private until it provides "
        "a clear use case and a reliable implementation."
    ),
    "support_title": "Publication rule",
    "support_text": "Live tools appear publicly. Draft, private and planned products do not.",
    "tools_eyebrow": "Live products and public tools",
    "tools_title": "Open a tool and use it now.",
    "tools_text": "Choose the product that matches the technical task in front of you.",
    "cta_title": "Does your team repeat a technical check every week?",
    "cta_text": "A recurring workflow may be ready to become an internal tool or a product.",
    "cta_label": "Discuss a product workflow",
}


ADTECH_PAGE = {
    "slug": "adtech",
    "language": "en",
    "seo_title": "AdTech Development & Publisher Technology | Pi Development",
    "meta_description": (
        "AdTech development, Google Ad Manager and GPT implementation, creative QA, publisher tools and "
        "monetization diagnostics from Pi Development."
    ),
    "eyebrow": "AdTech development",
    "title": "Publisher technology built with monetization context.",
    "description": (
        "Custom AdTech engineering for publishers, AdOps, RevOps and monetization teams that need clearer "
        "diagnostics, better operations and software beyond standard platform limits."
    ),
    "intro_title": "AdTech is a complete technical practice here.",
    "intro": (
        "Publisher monetization sits across browser behavior, ad serving, creative delivery, tracking, page "
        "performance and daily operations. Pi Development connects those layers before deciding what to build or fix."
    ),
    "support_title": "Typical starting points",
    "support_text": (
        "A Google Ad Manager implementation, an unclear ad stack, repeated creative QA, a monetization workflow "
        "or a custom ad product that existing platforms cannot support."
    ),
    "sections": [
        {
            "anchor": "adtech-engineering",
            "label": "Engineering",
            "title": "AdTech Engineering",
            "description": "Custom publisher technology, monetization interfaces and technical product development.",
            "solves": "A commercial or operational requirement does not fit an existing ad platform.",
            "builds": "Publisher tools, custom ad products, dashboards, integrations and workflow systems.",
        },
        {
            "anchor": "gam-gpt",
            "label": "Implementation",
            "title": "Google Ad Manager and GPT",
            "description": "Implementation and review work around inventory, slots, tags and publisher-side behavior.",
            "solves": "Ad delivery is difficult to reason about, change safely or validate consistently.",
            "builds": "GPT implementation, slot architecture, diagnostics, technical review and supporting tools.",
        },
        {
            "anchor": "audits-diagnostics",
            "label": "Diagnostics",
            "title": "Ad Stack Audits and Monetization Diagnostics",
            "description": "Evidence-led investigation across visible vendors, tags, slots, wrappers and page context.",
            "solves": "The current implementation state is unclear and troubleshooting starts from assumptions.",
            "builds": "Technical baselines, diagnostic tooling, implementation maps and prioritized findings.",
        },
        {
            "anchor": "creative-qa",
            "label": "Quality",
            "title": "Creative QA",
            "description": "Structured checks for HTML creatives, tags, click paths, tracking and serving context.",
            "solves": "Repeated review work is inconsistent, slow or difficult to document.",
            "builds": "QA workflows, checklists, preview tools and review interfaces.",
        },
        {
            "anchor": "adops-automation",
            "label": "Operations",
            "title": "AdOps Automation",
            "description": "Software and automation for repeated campaign, QA, tracking and reporting work.",
            "solves": "Operational capacity is consumed by predictable manual checks and handoffs.",
            "builds": "Internal tools, integrations, controlled automation and exception queues.",
        },
    ],
    "process": {
        "eyebrow": "How an AdTech engagement works",
        "title": "Start with evidence. Build around the operation.",
        "items": [
            {"title": "Inspect", "text": "Map the stack, browser behavior, workflow, constraints and commercial objective."},
            {"title": "Prioritize", "text": "Separate implementation risk, operational friction and product opportunity."},
            {"title": "Implement", "text": "Build or repair the smallest complete technical layer that can operate reliably."},
            {"title": "Validate", "text": "Test behavior, document limits and improve the workflow with real use."},
        ],
    },
    "tools_eyebrow": "Public AdTech tools",
    "tools_title": "Begin with a focused technical check.",
    "tools_text": "Use a live tool for an initial signal, then escalate to browser-level investigation or custom engineering when needed.",
    "faqs": [
        {
            "question": "Does an AdTech audit replace browser and network inspection?",
            "answer": "No. An initial audit creates a baseline and better hypotheses; runtime behavior still requires the right browser-level evidence.",
        },
        {
            "question": "Can Pi Development build custom ad products?",
            "answer": "Yes. Custom formats, publisher tools and supporting delivery or QA systems can be defined around a real commercial requirement.",
        },
        {
            "question": "Do you work with Google Ad Manager and GPT?",
            "answer": "Yes. The AdTech practice includes Google Ad Manager context, GPT implementation, slot architecture and publisher-side diagnostics.",
        },
    ],
    "cta_title": "Bring the implementation, workflow or monetization problem.",
    "cta_text": "We will determine whether it needs diagnosis, repair, automation or a new AdTech product.",
    "cta_label": "Discuss an AdTech solution",
}


INSIGHTS_PAGE = {
    "slug": "insights",
    "language": "en",
    "seo_title": "Software & AdTech Insights | Pi Development",
    "meta_description": (
        "Technical insights from Pi Development on AdTech, Google Publisher Tag, creative QA, publisher "
        "technology, tracking, technical SEO and web performance."
    ),
    "eyebrow": "Insights",
    "title": "Technical writing connected to real products and services.",
    "description": (
        "Guides and implementation notes for teams working on publisher technology, creative QA, tracking, "
        "technical SEO and web performance."
    ),
    "intro_title": "Useful content should help someone make a better technical decision.",
    "intro": (
        "The current library focuses on areas where Pi Development already has working tools or implementation "
        "context. New clusters will be added only when there is enough useful material to support them."
    ),
    "support_title": "Editorial structure",
    "support_text": "Each article connects to a related tool, service or next technical step.",
    "insights_eyebrow": "Published insights",
    "insights_title": "Explore the current topic clusters.",
    "insights_text": "The existing Spanish technical library remains available while the localized editorial system is expanded.",
    "cta_title": "Need help applying a technical guide to a real implementation?",
    "cta_text": "Share the system, URL or workflow that needs a closer review.",
    "cta_label": "Review an implementation",
}


COMPANY_PAGE = {
    "slug": "company",
    "language": "en",
    "seo_title": "Company | Pi Development",
    "meta_description": (
        "Pi Development is an independent custom software and AdTech company based in Buenos Aires, Argentina, "
        "working globally."
    ),
    "eyebrow": "Company",
    "title": "An independent custom software and AdTech company.",
    "description": (
        "Pi Development defines, designs and builds software for product ideas, operational problems and "
        "publisher technology. Based in Buenos Aires, Argentina, and working globally."
    ),
    "intro_title": "Why Pi Development exists",
    "intro": (
        "Useful software often begins between categories: a product idea that still needs definition, an "
        "operation held together manually or a monetization problem that generic development teams do not understand."
    ),
    "support_title": "Position",
    "support_text": "Independent, technically direct and designed to grow through working software rather than inflated claims.",
    "sections": [
        {
            "label": "Purpose",
            "title": "Problems worth solving",
            "description": "The work begins with a recurring problem, a clear user or an outcome that software can materially improve.",
        },
        {
            "label": "Method",
            "title": "Product and engineering stay connected",
            "description": "Definition, interface, architecture, automation and QA are treated as one delivery system.",
        },
        {
            "label": "Experience",
            "title": "Software, operations and AdTech",
            "description": "The company combines product development with operational context and publisher-side advertising technology.",
        },
        {
            "label": "Reach",
            "title": "Buenos Aires. Working globally.",
            "description": "Pi Development is based in Argentina and collaborates remotely with teams beyond the local market.",
        },
    ],
    "process": {
        "eyebrow": "Working principles",
        "title": "Clear enough to explain. Strong enough to operate.",
        "items": [
            {"title": "Define before building", "text": "Understand the user, operation and outcome before selecting technology."},
            {"title": "Use evidence", "text": "Prefer working software, observable behavior and explicit constraints over claims."},
            {"title": "Keep ownership direct", "text": "Maintain the connection between the business problem and its implementation."},
            {"title": "Prepare for iteration", "text": "Build a maintainable base without pretending the first version knows everything."},
        ],
    },
    "cta_title": "A clear problem is a useful starting point.",
    "cta_text": "Tell us what needs to be launched, automated, repaired or made easier to operate.",
    "cta_label": "Bring us the problem",
}


CONTACT_PAGE = {
    "slug": "contact",
    "language": "en",
    "seo_title": "Contact Pi Development | Discuss a Software Project",
    "meta_description": (
        "Contact Pi Development to discuss an MVP, custom software, internal tool, AI automation, platform "
        "improvement or AdTech solution."
    ),
    "eyebrow": "Contact",
    "title": "Bring the problem. We will define the right system around it.",
    "description": (
        "A complete brief is not required. Share what needs to be launched, automated, repaired or made easier "
        "to operate."
    ),
    "intro_title": "A useful first message is short.",
    "intro": "Tell us who the software is for, what happens today and what should work better.",
    "support_title": "Good starting points",
    "support_text": "An MVP, custom platform, internal tool, recurring operation, existing implementation or AdTech requirement.",
    "contact_reassurance": "Your message goes directly to Pi Development. No sales sequence or formal request for proposal is required.",
}


# Backwards-compatible import name while /about/ redirects to /company/.
ABOUT_PAGE = COMPANY_PAGE

PAGE_BY_SLUG = {
    "solutions": SOLUTIONS_PAGE,
    "products": PRODUCTS_PAGE,
    "adtech": ADTECH_PAGE,
    "insights": INSIGHTS_PAGE,
    "company": COMPANY_PAGE,
    "contact": CONTACT_PAGE,
}


def get_home_page(language="en"):
    if language != "en":
        raise KeyError(f"Unsupported commercial content language: {language}")
    from .tool_availability import is_tool_available

    page = deepcopy(HOME_PAGE)
    page["products"]["items"] = [
        item
        for item in page["products"]["items"]
        if not item.get("href", "").startswith("/tools/")
        or is_tool_available(item["href"].strip("/").split("/")[-1])
    ]
    return page


def get_company_page(slug, language="en"):
    if language != "en":
        raise KeyError(f"Unsupported commercial content language: {language}")
    return deepcopy(PAGE_BY_SLUG[slug])
