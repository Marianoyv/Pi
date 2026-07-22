# Templates and Components Inventory

Template root: `pi_development/web/templates/web/`.

The active site uses Django templates with `web/base.html` as the shared document shell. Page templates add CSS through `{% block head %}` and content through `{% block content %}`. Shared navigation and footer are component includes.

## Shared Base

| Template | Purpose | Depends on | Label |
|---|---|---|---|
| `base.html` | HTML shell, metadata, canonical, OG/Twitter tags, Organization schema, favicon, Google Analytics, font/bootstrap/fontawesome/static CSS, shared scripts | `context_processors.site_settings`, `base.css`, `navbar.css`, `footer.css`, `main.js`, Bootstrap CDN, Font Awesome kit, Google Fonts | `CORE_PUBLIC` |
| `components/navbar.html` | Top navigation and progress bar | route names: index, solutions, products, adtech, labs, insights, about, contact; logo `piw.png`; `main.js` mobile menu | `CORE_PUBLIC` |
| `components/footer.html` | Footer navigation, core areas, policies, discovery SEO hubs, contact and social links | `footer_seo_hubs`, contact settings, footer CSS, Font Awesome | `CORE_PUBLIC` |

## Active Page Templates

| Template | Routes | Purpose | CSS | Label |
|---|---|---|---|---|
| `company_home.html` | `/` | Current corporate home | `company.css` | `CORE_PUBLIC` |
| `company_page.html` | `/solutions/`, `/products/`, `/adtech/`, `/labs/`, `/insights/`, `/about/`, `/contact/` | Generic company page renderer for code-defined page objects | `company.css`, `tools.css` | `CORE_PUBLIC` |
| `systems_page.html` | `/systems/` | Architecture/systems overview | `services_overview.css` | `CORE_PUBLIC` |
| `tools_page.html` | `/tools/` | Tool catalog, featured tool, groups, topic clusters | `tools.css` | `EXISTING_APP` |
| `tool_detail_page.html` | non-live fallback tool detail pages | Tool detail fallback for catalog items without live config | `tools.css` | `EXISTING_APP` |
| `ai_auditor_page.html` | `/tools/ai-auditor/` | Live AI Auditor form/result page | `tools.css` | `EXISTING_APP` |
| `landing_snapshot_page.html` | `/tools/landing-performance-snapshot/` | Live Landing Performance Snapshot page | `tools.css` | `EXISTING_APP` |
| `adtech_debug_tool_page.html` | `/tools/adtech-debug-tool/` | Live AdTech Debug Tool page | `tools.css` | `EXISTING_APP` |
| `utm_builder_page.html` | `/tools/utm-builder/` | Live UTM Builder page | `tools.css` | `EXISTING_APP` |
| `creative_qa_page.html` | `/tools/creative-qa-checklist/` | Live Creative QA page | `tools.css` | `EXISTING_APP` |
| `creative_preview_lab_page.html` | `/tools/creative-preview-lab/` | Live Creative Preview Lab page | `tools.css` | `EXISTING_APP` |
| `seo_landing_page.html` | `/<seo-slug>/` | SEO landing pages and AdTech hub | `content_page.css`, `tools.css` | `CONTENT_ASSET` |
| `blog_page.html` | `/blog/` | Knowledge article listing | `blog.css`, `tools.css` | `CORE_PUBLIC` |
| `knowledge_article_page.html` | `/blog/<slug>/` | Knowledge article detail | `content_page.css`, `tools.css` | `CONTENT_ASSET` |
| `work_page.html` | `/work/` | Work/case overview | `portfolio.css` | `CORE_PUBLIC` |
| `approach_page.html` | `/approach/` | Method page | `content_page.css` | `CORE_PUBLIC` |
| `policies.html` | `/policies/` | Policies page | `policies.css` | `CONTENT_ASSET` |
| `404.html` | error handler if configured by Django | 404 page | unknown from static inspection | `CONTENT_ASSET` |

## Component Templates

| Template | Used by | Purpose | Label |
|---|---|---|---|
| `components/tool_card.html` | tools/catalog/company product surfaces | Tool card with CTA | `EXISTING_APP` |
| `components/tool_editorial_content.html` | tool detail/live pages | Editorial analysis, use, results, limitations, FAQs | `EXISTING_APP` |
| `components/tool_example_block.html` | live tool pages | Example submission CTA/form control | `EXISTING_APP` |
| `components/tool_exports.html` | live result pages | Copy/export result blocks | `EXISTING_APP` |
| `components/tool_insight.html` | live result pages | Insight score/status summary | `EXISTING_APP` |
| `components/tool_related_tools.html` | tool pages | Related tools, related SEO guides, topic-cluster links | `EXISTING_APP` |
| `components/seo_hub_group.html` | SEO hub pages | Topic cluster / hub section cards | `CONTENT_ASSET` |
| `components/portfolio_media.html` | portfolio/work views | Image/video rendering for portfolio items | `CONTENT_ASSET` |
| `components/navbar.html` | page templates | Shared primary navigation | `CORE_PUBLIC` |
| `components/footer.html` | page templates | Shared footer navigation and contact | `CORE_PUBLIC` |

## Older or Legacy-Looking Templates

These files are present and must not be removed. Some appear to belong to an earlier site design or section system and are referenced by older templates or legacy concepts.

| Template | Notes | Label |
|---|---|---|
| `index.html` | Older multi-section home template; references hero, servicios, portfolio, proceso, herramientas, nosotros, contacto CSS | `LEGACY_PRESERVE` |
| `hero.html` | Older hero partial; links tools/systems and social profiles | `LEGACY_PRESERVE` |
| `servicios.html` | Older services partial; links systems | `LEGACY_PRESERVE` |
| `portfolio.html` | Older portfolio partial; links work and external projects | `LEGACY_PRESERVE` |
| `proceso.html` | Older process partial; links approach | `LEGACY_PRESERVE` |
| `herramientas.html` | Older tools partial; links tools | `LEGACY_PRESERVE` |
| `nosotros.html` | Older about partial; links about | `LEGACY_PRESERVE` |
| `contacto.html` | Older contact template/partial | `LEGACY_PRESERVE` |
| `about_page.html` | Separate about page template not used by current `about` view | `POSSIBLE_DUPLICATE` |
| `contact_page.html` | Separate contact page template not used by current `contact` view | `POSSIBLE_DUPLICATE` |

## Navigation Exposure

Primary navbar:

- Home -> `/`
- Solutions -> `/solutions/`
- Products -> `/products/`; active for `/products/` and `/tools/` paths
- AdTech -> `/adtech/`
- Labs -> `/labs/`
- Insights -> `/insights/`; active for `/insights/` and `/blog/` paths
- About -> `/about/`
- Contact -> `/contact/`

Footer:

- Home, Solutions, Products, AdTech, Labs, Insights, About, Contact
- Core areas: Enterprise Software, AI & Automation, AdTech & Publisher Tools, Products & Labs, Policies
- Technical guide discovery pages from `get_discovery_seo_hub_pages()`
- Contact email, WhatsApp, GitHub, LinkedIn, Instagram

Not primary-nav exposed but routed:

- `/systems/`
- `/tools/`
- `/work/`
- `/approach/`
- `/blog/`
- `/policies/`
- SEO landing pages
- legacy redirects

## Template Fragility Notes

- `base.html` controls SEO metadata site-wide. Rebuilding the corporate site without preserving block behavior can break canonical, OG/Twitter, Organization schema, Google verification, and Analytics.
- `company_page.html` renders multiple company pages from structured dictionaries; changing expected fields affects Solutions, Products, AdTech, Labs, Insights, About, and Contact together.
- Tool templates share context keys but each live page expects a specific result object name such as `audit_result`, `landing_result`, `debug_result`, `utm_result`, `qa_result`, or `preview_result`.
- Older templates may be unused by active views but still document previous structure and contain links to preserved current routes.
