"Structured English content for Pi Development's commercial pages.\n\nTemplates render this module as the single source of truth for the current\nEnglish site. A future Spanish edition can provide the same schema without\nduplicating copy in templates."

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
        "brand_statement": "Think clearly. Build what matters.",
        "title": "We build software for problems worth solving.",
        "description": (
            "Pi Development turns product ideas, manual operations and monetization challenges into reliable "
            "software—from MVPs and internal platforms to AI workflows and publisher technology."
        ),
        "primary_cta": {"label": "Discuss a project", "href": "/contact/"},
        "secondary_cta": {"label": "Explore our work", "href": "/work/"},
        "location": "Based in Buenos Aires. Available for remote work.",
    },
    "audience": ["For founders", "Operational teams", "Digital publishers"],
    "business_value": {
        "items": [
            {
                "title": "More paths to revenue",
                "text": "Build a better way to sell, serve, package or monetize what the business already knows.",
            },
            {
                "title": "Less repeated work",
                "text": "Turn recurring checks and handoffs into software people can understand and control.",
            },
            {
                "title": "Earlier signals",
                "text": "Make delays, errors and weak points visible before they become the normal way of working.",
            },
        ],
    },
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
                "title": "Understand",
                "text": "Define the problem, the people affected and the outcome that must change.",
            },
            {
                "title": "Design",
                "text": "Reduce complexity into a system that can be explained, tested and maintained.",
            },
            {
                "title": "Build",
                "text": "Create the smallest useful version capable of operating reliably and proving value.",
            },
            {
                "title": "Evolve",
                "text": "Measure real use, learn from it and improve what proves valuable.",
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
    "tools": {
        "eyebrow": "Products",
        "title": "Working products for repeatable technical work.",
        "description": "Maintained products with live interfaces, explicit capabilities and documented limits.",
        "items": [],
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
                "title": "Emotional Int Blog",
                "text": (
                    "An editorial system structured for long-form publishing, organic discovery and "
                    "maintainable content growth."
                ),
            },
            {
                "slug": "indices-argentinos",
                "title": "Pi Finance",
                "text": (
                    "Eighteen financial tools for everyday decisions, transparent formulas and official Argentine data."
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
        {"label": "Editorial system", "title": "Emotional Int Blog", "href": "/work/#blog-int-emocional"},
        {"label": "Financial product suite", "title": "Pi Finance", "href": "/work/#indices-argentinos"},
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
    "tools_eyebrow": "Public AdTech products",
    "tools_title": "Begin with a focused technical check.",
    "tools_text": "Use a live product for an initial signal, then escalate to browser-level investigation or custom engineering when needed.",
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
    "seo_title": "Spanish Software & AdTech Insights | Pi Development",
    "meta_description": (
        "Technical insights from Pi Development on AdTech, Google Publisher Tag, creative QA, publisher "
        "technology, tracking, technical SEO and web performance."
    ),
    "eyebrow": "Insights",
    "title": "Spanish technical guides connected to real products and services.",
    "description": (
        "A clearly separated Spanish-language library for teams working on publisher technology, creative QA, "
        "tracking, technical SEO and web performance."
    ),
    "intro_title": "Useful content should help someone make a better technical decision.",
    "intro": (
        "The current library focuses on areas where Pi Development already has working tools or implementation "
        "context. New clusters will be added only when there is enough useful material to support them."
    ),
    "support_title": "Editorial structure",
    "support_text": "Each article connects to a related tool, service or next technical step.",
    "insights_eyebrow": "Spanish-language library",
    "insights_title": "Explore the current topic clusters in Spanish.",
    "insights_text": "All articles in this library are published in Spanish; Pi Development's commercial pages remain in English.",
    "cta_title": "Need help applying a technical guide to a real implementation?",
    "cta_text": "Share the system, URL or workflow that needs a closer review.",
    "cta_label": "Review an implementation",
}


COMPANY_PAGE = {
    "slug": "company",
    "language": "en",
    "seo_title": "Founder-Led Software & AdTech Studio | Pi Development",
    "meta_description": (
        "Pi Development is a founder-led software and AdTech studio led by Mariano Tami in Buenos Aires, Argentina, "
        "and available for remote work."
    ),
    "eyebrow": "Company",
    "title": "Founder-led, with direct technical ownership.",
    "description": (
        "Mariano Tami leads Pi Development and remains responsible for product definition, architecture, "
        "implementation, deployment, measurement and ongoing improvement."
    ),
    "intro_title": "Mariano Tami · Founder",
    "intro": (
        "Mariano is a self-taught software developer and AdTech practitioner with experience across digital "
        "marketing, analytics, SEO and web measurement. He works professionally in English and is a native "
        "Spanish speaker."
    ),
    "support_title": "Founder role",
    "support_text": "Founder · AdTech, Web Monetization & Product Development",
    "sections": [
        {
            "label": "Background",
            "title": "From aviation to digital systems",
            "description": (
                "Before entering technology, Mariano trained in civil aviation and worked as a commercial pilot. "
                "That background supports a systems-oriented approach to preparation, constraints, testing and clear responsibility."
            ),
        },
        {
            "label": "Transition",
            "title": "A practical path into technology",
            "description": (
                "During the pandemic, Mariano began studying digital marketing, web development and programming. "
                "His initial digital work included SEO and landing pages, followed by marketing specialist and "
                "marketing leadership roles for a language-education organization."
            ),
        },
        {
            "label": "Delivery",
            "title": "Direct technical ownership",
            "description": (
                "Mariano personally connects problem discovery, product definition, architecture, frontend and backend "
                "implementation, infrastructure, analytics, AdTech, QA, documentation and maintenance."
            ),
        },
        {
            "label": "Delivery model",
            "title": "Founder-led by design",
            "description": (
                "Pi Development does not currently have a standing team. When a project genuinely requires additional "
                "expertise, collaborators may be incorporated with their responsibilities made explicit."
            ),
        },
        {
            "label": "Fit",
            "title": "Useful, maintainable and responsibly operated",
            "description": (
                "Pi works with people committed to building a useful product and operating it responsibly, including "
                "founders, local businesses, operations teams, publishers and monetization teams."
            ),
        },
        {
            "label": "Availability",
            "title": "Buenos Aires Remote",
            "description": (
                "Pi Development is based in Buenos Aires, Argentina, and available for remote work. Capacity is "
                "deliberately limited and depends on the complexity and responsibilities of each project."
            ),
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


BUSINESS_SOLUTIONS_PAGE = {
    "slug": "business-solutions",
    "language": "es",
    "seo_title": "Web design for business, with strategy and marketing | Pi Development",
    "meta_description": (
        "Complete web design for businesses: strategy, content, experience, SEO, measurement and queries by "
        "WhatsApp, with direct attention from Mariano Tami."
    ),
    "eyebrow": "Business solutions",
    "title": "A website that explains your business, generates trust and converts interest into inquiries.",
    "description": (
        "It's not just about publishing a page. I connect strategy, content, design, development and "
        "measurement so that your digital presence has a clear commercial purpose."
    ),
    "hero_primary_label": "Know the service",
    "hero_secondary_label": "See plans and prices",
    "outcomes_title": "What changes when the website is thought of as part of the business",
    "outcomes": [
        {
            "number": "01",
            "title": "Your offer is understood",
            "text": "Information is no longer dispersed among publications, messages and repeated explanations.",
        },
        {
            "number": "02",
            "title": "Your business transmits trust",
            "text": "You have your own space, coherent and prepared to work well on any device.",
        },
        {
            "number": "03",
            "title": "The consultation arrives better prepared",
            "text": "Each journey leads to a clear action: write, request a quote or consult a product.",
        },
        {
            "number": "04",
            "title": "You can learn and improve",
            "text": "Measurement allows us to observe what is visited, what is of interest and where it is advisable to continue investing.",
        },
    ],
    "service_title": "A complete service, not a collection of separate tasks",
    "service_intro": (
        "I work directly with you to transform the reality of the business into a clear web experience, "
        "published and ready to evolve."
    ),
    "service_items": [
        {"title": "Strategy", "text": "Objective, audience, value proposition and main action before choosing technology."},
        {"title": "Content and structure", "text": "Order of services, products, arguments and questions that a person needs to solve."},
        {"title": "Design and development", "text": "Its own interface, responsive, accessible and built around the real route."},
        {"title": "Marketing and conversion", "text": "Technical SEO, messages, calls to action and contact connected with a commercial intent."},
        {"title": "Publishing and measurement", "text": "Domain, hosting, testing, Analytics and events to observe usage since launch."},
        {"title": "Accompaniment", "text": "Explanation of decisions, clear boundaries and a maintenance option after delivery."},
    ],
    "ai_title": "AI can create a page. The value is in deciding which page your business needs.",
    "ai_intro": (
        "I use artificial intelligence when it speeds up work, but I don't delegate business understanding to it. "
        "nor responsibility for the result."
    ),
    "ai_columns": [
        {
            "label": "Do it only with AI",
            "items": [
                "You receive options, drafts and code quickly.",
                "You define what to ask for, what to keep and what to correct.",
                "You connect domain, measurement, forms and publication.",
                "You test, maintain and respond when something fails.",
            ],
        },
        {
            "label": "work with me",
            "items": [
                "First I understand the situation and reduce the complexity.",
                "I make content, experience and technology decisions with common criteria.",
                "I deliver the integrated, published and tested solution.",
                "There is a person responsible before, during and after the launch.",
            ],
        },
    ],
    "marketing_title": "The web also needs a marketing base",
    "marketing_intro": (
        "I do not promise results that a page alone cannot guarantee. Yes I build the conditions for "
        "make the business easier to find, understand, consult and measure."
    ),
    "marketing_items": [
        {"title": "Positioning", "text": "A message that explains who the offer is for and why to choose it."},
        {"title": "Discovery", "text": "Content and technical foundations that help search engines and people interpret the site."},
        {"title": "Conversion", "text": "Walkthroughs and calls to action that reduce the distance to a real consultation."},
        {"title": "Measurement", "text": "Useful events and metrics to stop deciding solely by intuition."},
    ],
    "intro_title": "A concrete solution, without becoming a technology specialist.",
    "intro": (
        "You don't need to arrive with a perfect brief or decide which platform to use. First I understand how it works "
        "your business, I organize the information and build the smallest version that can really help you."
    ),
    "support_title": "Direct work",
    "support_text": (
        "You talk to Mariano from the first conversation to publication. The same person understands the "
        "problem, makes technical decisions, tests the solution and monitors its evolution."
    ),
    "sections": [
        {
            "anchor": "sitio-comercial",
            "label": "Offer 01",
            "title": "Commercial site",
            "description": (
                "A professional presence to explain what you do, show confidence and facilitate a consultation."
            ),
            "solves": (
                "Your business depends on social networks, recommendations or a page that no longer represents what you offer well."
            ),
            "for_whom": "Professionals, businesses, manufacturers, distributors and service companies.",
            "builds": (
                "Home page, products or services, business information, contact by WhatsApp, technical SEO "
                "basic, measurement and mobile experience."
            ),
            "scope": "Content, design, development, mastering, publishing, testing and a ready base to maintain.",
        },
        {
            "anchor": "catalogo-guiado",
            "label": "Offer 02",
            "title": "Guided digital catalog",
            "description": (
                "An experience that orders products, helps compare them and turns a visit into a better prepared consultation."
            ),
            "solves": (
                "Your products have variants, measurements, categories or decisions that do not fit well in a list or social post."
            ),
            "for_whom": "Businesses with physical products, custom work, advice or personalized budgets.",
            "builds": (
                "Catalog, filters or categories, product sheets, recommendation tours and direct contact via WhatsApp."
            ),
            "scope": (
                "Definition of the route, organization of information, interface, development, publication, testing and evolution."
            ),
        },
    ],
    "process": {
        "title": "The difference is not generating a page. It is taking responsibility for the result.",
        "items": [
            {
                "title": "Understand",
                "text": "I listen to how the business works, what the customer needs, and where an opportunity is being missed today.",
            },
            {
                "title": "Organize",
                "text": "I turn dispersed products, services and decisions into a clear and easy-to-navigate structure.",
            },
            {
                "title": "Build and test",
                "text": "I deliver the published site, mobile responsive, measured and reviewed as a complete experience.",
            },
            {
                "title": "Accompany",
                "text": "I explain decisions, document boundaries, and can remain available when the business changes.",
            },
        ],
    },
    "deliverables_title": "What delivery may include",
    "deliverables": [
        "Structure and content oriented to a real query.",
        "Responsive design for cell phone, tablet and desktop.",
        "WhatsApp, email, domain, hosting and measurement.",
        "Basic technical SEO, testing and delivery documentation.",
        "A maintenance proposal according to the real scope.",
    ],
    "technology_title": "AI is a tool, not who is responsible for the project",
    "technology_text": (
        "Artificial intelligence can speed up drafts, code, and exploration. Mariano defines what is appropriate "
        "build, reviews every decision and assumes technical responsibility for the entire delivery."
    ),
    "evidence_title": "Two ways to turn a business into a clear experience",
    "evidence": [
        {
            "label": "Commercial site SEO and measurement",
            "title": "Juno Metals",
            "href": "/work/juno-metales/",
        },
        {
            "label": "Catalog · recommendation and consultation",
            "title": "Taitet",
            "href": "/work/taitet/",
        },
    ],
    "faq_title": "Questions before talking.",
    "faqs": [
        {
            "question": "Why hire a person when I can create a page with AI?",
            "answer": (
                "If you need to experiment and have time to learn, AI may be enough. Pi provides criteria, "
                "organization, complete implementation, testing and a responsible person when the result matters."
            ),
        },
        {
            "question": "Do I need a complete online store?",
            "answer": (
                "Not necessarily. Many businesses first need to present their offer well and prepare a useful consultation. "
                "by WhatsApp. The smallest solution that resolves this path is proposed."
            ),
        },
        {
            "question": "How is the budget defined?",
            "answer": (
                "After a brief conversation, content, functions, responsibilities and maintenance are defined. "
                "The proposal separates the initial project from recurring costs."
            ),
        },
        {
            "question": "Who does the work?",
            "answer": (
                "Mariano Tami personally leads the definition, development, testing and publishing. "
                "Business understanding and technical responsibility are not delegated."
            ),
        },
    ],
    "labels": {
        "problem": "Situation",
        "for_whom": "for whom",
        "builds": "What do I build?",
        "scope": "What it covers",
        "delivery": "Delivery",
        "technology": "Judgment",
        "evidence": "Published work",
    },
    "cta_title": "I chose a clear starting point.",
    "cta_text": (
        "The plans order scope, times and reference price. Then we confirm which option corresponds "
        "to the reality of your business."
    ),
    "cta_label": "Compare plans and prices",
}


BUSINESS_PLANS_PAGE = {
    "slug": "web-plans",
    "language": "es",
    "seo_title": "Website plans and pricing | Pi Development",
    "meta_description": (
        "Compare web design plans for commercial presence, digital catalogs and assisted sales, with scope, "
        "clear reference times and prices."
    ),
    "eyebrow": "Website plans",
    "title": "A clear starting point for each stage of the business.",
    "description": (
        "Three comparable scopes to know what you receive, how much it may cost and when it could be published. "
        "The final proposal confirms the content and functions before starting."
    ),
    "plans": [
        {
            "slug": "presencia",
            "name": "Presence",
            "purpose": "To explain",
            "price": "USD 550",
            "price_note": "from",
            "timeline": "10 business days",
            "description": "To stop depending solely on social networks and present the business clearly.",
            "features": [
                "Up to 5 sections",
                "Main services or products",
                "Responsive design",
                "WhatsApp and email",
                "Domain and publication",
                "Basic technical SEO",
                "Google Analytics",
                "1 round of adjustments",
            ],
            "not_included": "It does not include a complete catalog, online payments or personalized functions.",
        },
        {
            "slug": "catalogo",
            "name": "Catalog",
            "purpose": "To display and order",
            "price": "USD 1,100",
            "price_note": "from",
            "timeline": "3 weeks",
            "featured": True,
            "description": "To organize a broad offer and convert each product into a specific query.",
            "features": [
                "Everything included in Presencia",
                "Categories and product sheets",
                "Up to 20 starting elements",
                "Filters or category navigation",
                "WhatsApp from each product",
                "Variants, measures or characteristics",
                "Measurement of visits and contacts",
                "2 rounds of adjustments",
            ],
            "not_included": "Does not include checkout, real-time inventory or complex integrations.",
        },
        {
            "slug": "venta-asistida",
            "name": "Assisted sale",
            "purpose": "To guide and qualify",
            "price": "USD 2,200",
            "price_note": "from",
            "timeline": "4 to 6 weeks",
            "description": "For offers that need recommendation, calculation or context before quoting.",
            "features": [
                "Everything included in the Catalog",
                "Guided tour of recommendation",
                "Questions to qualify the query",
                "Guidance calculation when feasible",
                "Up to 50 starting items",
                "Simple automations or integrations",
                "Custom analytics",
                "3 rounds of adjustments and training",
            ],
            "not_included": "Final logic and integrations are confirmed before closing the quote.",
        },
    ],
    "common_title": "All plans include a complete delivery",
    "common_items": [
        "Direct work with Mariano",
        "Defining scope before building",
        "Responsive experience",
        "Publishing and testing",
        "Reported recurring costs",
        "30 days to correct delivery errors",
        "AI used under human supervision",
        "Post maintenance option",
    ],
    "faq_title": "Before choosing a plan",
    "faqs": [
        {
            "question": "Is the published price final?",
            "answer": (
                "It is a reference price from the scope described. Before starting, confirm in writing the "
                "amount of content, functions, responsibilities, third party services and final price."
            ),
        },
        {
            "question": "Who prepares the texts and images?",
            "answer": (
                "The plan organizes and adapts the agreed material. Extensive writing, photography, visual identity or "
                "additional production are included only when they appear in the proposal."
            ),
        },
        {
            "question": "What costs continue after publishing?",
            "answer": (
                "Domain, paid tools, infrastructure and maintenance are detailed separately. They are prioritized "
                "simple options and transparent operating costs."
            ),
        },
        {
            "question": "Can I start with a plan and expand it later?",
            "answer": (
                "Yes. The solution is designed to evolve, but each new stage is defined and priced according to the "
                "actual scope at that time."
            ),
        },
    ],
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
        "A complete brief is not required. Share the problem, current stage and intended outcome. Mariano reviews "
        "each commercial inquiry personally."
    ),
    "intro_title": "A useful first message is short.",
    "intro": "Tell us who the software is for, what happens today and what should work better.",
    "support_title": "Good starting points",
    "support_text": "An MVP, custom platform, internal tool, recurring operation, existing implementation or AdTech requirement.",
    "form_title": "Tell Mariano what needs to work better.",
    "response_time": "Normally within 2–3 business days",
    "contact_reassurance": (
        "Use the short project brief to organize the essentials. It is prepared in your browser and is only shared "
        "if you choose WhatsApp or email."
    ),
}


# Backwards-compatible import name while /about/ redirects to /company/.
ABOUT_PAGE = COMPANY_PAGE

PAGE_BY_SLUG = {
    "business-solutions": BUSINESS_SOLUTIONS_PAGE,
    "web-plans": BUSINESS_PLANS_PAGE,
    "solutions": SOLUTIONS_PAGE,
    "adtech": ADTECH_PAGE,
    "insights": INSIGHTS_PAGE,
    "company": COMPANY_PAGE,
    "contact": CONTACT_PAGE,
}


def get_home_page(language="en"):
    if language != "en":
        raise KeyError(f"Unsupported commercial content language: {language}")
    from .tool_catalog import get_tools
    from .work_content import get_home_featured_work_items

    page = deepcopy(HOME_PAGE)
    page["meta_description"] = (
        "Founder-led product development, operational software and AdTech engineering from Buenos Aires, "
        "available for remote work."
    )
    page["hero"].update(
        {
            "eyebrow": "Custom software for business growth",
            "title": (
                "I build software that helps businesses find new revenue opportunities, reduce repeated work "
                "and expose operational blind spots."
            ),
            "description": (
                "Product development, operational software and AdTech engineering—led directly from the business "
                "problem through implementation and measurement."
            ),
            "primary_cta": {"label": "Explore the products", "href": "#products"},
            "secondary_cta": {"label": "Discuss a business problem", "href": "/contact/"},
            "location": "Based in Buenos Aires. Available for remote work.",
        }
    )
    page["audience"] = ["For founders", "Operations teams", "Publishers and monetization teams"]
    page["what_we_solve"].update(
        {
            "title": "Three connected commercial specialties.",
            "description": "Software and measurement shaped around the way the work actually operates.",
            "items": [
                {
                    "title": "Product Development",
                    "text": "Custom web products and maintainable MVPs built around a defined problem and real users.",
                    "href": "/solutions/#product-development",
                },
                {
                    "title": "Operational Software",
                    "text": "Internal tools, integrations and controlled automation for recurring business processes.",
                    "href": "/solutions/#operational-software",
                },
                {
                    "title": "AdTech Engineering",
                    "text": "Publisher monetization, Google Ad Manager and GPT workflows, creative QA and technical debugging.",
                    "href": "/adtech/",
                },
            ],
        }
    )
    page["why_pi"].update(
        {
            "title": "Founder-led from discovery to maintenance.",
            "description": (
                "Every engagement stays directly connected to product decisions, implementation, measurement "
                "and technical responsibility."
            ),
            "items": [
                {"title": "Direct ownership", "text": "The founder who defines the problem also leads the technical delivery."},
                {"title": "Responsible fit", "text": "Projects are selected for useful outcomes, maintainability and responsible operation."},
                {"title": "Deliberate capacity", "text": "Capacity stays limited and is assessed according to project complexity."},
            ],
        }
    )
    page["tools"].update(
        {
            "eyebrow": "Products",
            "title": "Working products for repeatable technical work.",
            "description": "Maintained products with live interfaces, explicit capabilities and documented limits.",
            "items": [
                {
                    "title": tool["name"],
                    "text": tool["summary"],
                    "cta": tool["cta_label"],
                    "href": f"/products/{tool['slug']}/",
                }
                for tool in get_tools()
            ],
            "cta": {"label": "Explore all products", "href": "/products/"},
        }
    )
    page["selected_work"]["items"] = [
        {
            "slug": item["slug"],
            "title": item["name"],
            "text": item["home_summary"],
            "href": item["internal_url"],
            "image": item["poster"],
            "metrics": item["metrics"],
            "project_type": item["project_type"],
            "status": item.get("home_status", "Live"),
            "visual_note_primary": item["project_type"],
            "visual_note_secondary": item["timeline_label"],
        }
        for item in get_home_featured_work_items()
    ]
    return page


def get_company_page(slug, language="en"):
    if language != "en":
        raise KeyError(f"Unsupported commercial content language: {language}")
    page = deepcopy(PAGE_BY_SLUG[slug])
    if slug == "solutions":
        from .work_content import get_featured_work_items

        page.update(
            {
                "seo_title": "Product Development, Operational Software & AdTech | Pi Development",
                "meta_description": (
                    "Founder-led product development, operational software and AdTech engineering for useful, maintainable systems."
                ),
                "title": "Three commercial pillars, one direct delivery path.",
                "description": (
                    "Product development, operational software and AdTech engineering for useful systems connected "
                    "to real business processes."
                ),
                "sections": [
                    {
                        "anchor": "product-development",
                        "label": "Product",
                        "title": "Product Development",
                        "description": "Custom web products and lean MVPs built around a useful, maintainable core.",
                        "solves": "A business or product idea needs a working digital system rather than a decorative site.",
                        "for_whom": "Founders and established local businesses improving discovery, lead capture and service delivery.",
                        "builds": "Django and JavaScript applications, structured websites, portals and measured MVPs.",
                        "scope": "Discovery, definition, architecture, implementation, deployment, analytics, QA and maintenance.",
                    },
                    {
                        "anchor": "operational-software",
                        "label": "Operations",
                        "title": "Operational Software",
                        "description": "Purpose-built tools and automation connected to recurring business processes.",
                        "solves": "Important work depends on fragmented tools, manual handoffs or repeated checks.",
                        "for_whom": "Operations teams and businesses digitizing processes that currently happen primarily offline.",
                        "builds": "Internal tools, integrations, dashboards and controlled automation; AI is used only where suitable.",
                        "scope": "Workflow mapping, roles, data, safeguards, implementation, documentation and ongoing improvement.",
                    },
                    {
                        "anchor": "adtech-engineering",
                        "label": "Monetization",
                        "title": "AdTech Engineering",
                        "description": "Publisher technology and monetization workflows with direct technical context.",
                        "solves": "Ad serving, creative QA or revenue operations need clearer systems and evidence-led debugging.",
                        "for_whom": "Publishers, AdOps teams and monetization teams.",
                        "builds": "Google Ad Manager and GPT implementations, Prebid workflows, creative QA and operational tools.",
                        "scope": "Inspection, architecture, implementation, browser-level QA, measurement and documentation.",
                    },
                ],
                "evidence": [
                    {
                        "label": item["category"],
                        "title": item["name"],
                        "href": item["internal_url"],
                    }
                    for item in get_featured_work_items()
                ],
                "faqs": [
                    {
                        "question": "How are hosting and ongoing maintenance handled?",
                        "answer": (
                            "Hosting and maintenance are quoted separately according to actual infrastructure, storage, "
                            "usage, integrations and support requirements. Pi designs for durable systems with lean, "
                            "transparent recurring operating costs."
                        ),
                    },
                    {
                        "question": "Where does AI fit?",
                        "answer": "AI is a capability used within suitable software and automation workflows, with explicit quality and review boundaries.",
                    },
                    {
                        "question": "What makes a project a good fit?",
                        "answer": "A good fit is committed to a useful, maintainable product and to operating it responsibly after launch.",
                    },
                ],
            }
        )
    return page
