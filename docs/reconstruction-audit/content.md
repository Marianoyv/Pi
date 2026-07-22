# Content Inventory

Most public content is code-defined in Python data structures rather than database rows. This makes the content easy to preserve in Git, but reconstruction must avoid deleting or renaming slugs because routes, sitemaps, related links, and SEO metadata depend on them.

## Company Pages

Source: `pi_development/web/company_pages.py`.

| Slug / route | Content object | Template | Sitemap | Nav exposure | Purpose | Label |
|---|---|---|---|---|---|---|
| `/` | `HOME_PAGE` | `web/company_home.html` | yes | primary nav and footer | Corporate home: software, AI systems, automation, AdTech | `CORE_PUBLIC` |
| `/solutions/` | `SOLUTIONS_PAGE` | `web/company_page.html` | yes | primary nav and footer | Enterprise software, AI automation, AdTech, products/labs solution areas | `CORE_PUBLIC` |
| `/products/` | `PRODUCTS_PAGE` | `web/company_page.html` | yes | primary nav and footer | Live tools and future product placeholders | `CORE_PUBLIC` |
| `/adtech/` | `ADTECH_PAGE` | `web/company_page.html` | yes | primary nav and footer | Publisher tools and AdTech positioning | `CORE_PUBLIC` |
| `/labs/` | `LABS_PAGE` | `web/company_page.html` | yes | primary nav and footer | Future product experiments | `EXPERIMENTAL` |
| `/insights/` | `INSIGHTS_PAGE` | `web/company_page.html` | yes | primary nav and footer | Editorial layer and technical content bridge | `CORE_PUBLIC` |
| `/about/` | `ABOUT_PAGE` | `web/company_page.html` | yes | primary nav and footer | Company positioning | `CORE_PUBLIC` |
| `/contact/` | `CONTACT_PAGE` | `web/company_page.html` | yes | primary nav, footer, CTAs | Contact and project intake framing | `CORE_PUBLIC` |

Common fields:

- `seo_title`
- `meta_description`
- `meta_keywords`
- `eyebrow`
- `title`
- `description`
- `intro_title`
- `intro`
- `support_title`
- `support_text`
- `sections`
- `cta_title`
- `cta_text`

## Additional Static Page Objects in Views

Source: `pi_development/web/views.py`.

| Object / route | Purpose | Template | Label |
|---|---|---|---|
| `SYSTEMS_PAGE` / `/systems/` | Digital architecture and systems overview | `web/systems_page.html` | `CORE_PUBLIC` |
| `WORK_PAGE` / `/work/` | Case studies/work overview | `web/work_page.html` | `CORE_PUBLIC` |
| `APPROACH_PAGE` / `/approach/` | Method page | `web/approach_page.html` | `CORE_PUBLIC` |
| `policies` / `/policies/` | Policy page template | `web/policies.html` | `CONTENT_ASSET` |

`views.py` also contains older content dictionaries such as `HOME_PAGE`, `ABOUT_PAGE`, `CONTACT_PAGE`, and `BLOG_PAGE` that appear to represent an earlier site generation. They are not currently used by the active home/about/contact/blog views, but they must be preserved for owner review.

Classification: `POSSIBLE_DUPLICATE`.

## Tool Catalog Content

Source: `pi_development/web/tool_catalog.py`.

Tool definitions include:

- slug
- name
- tag
- status label/tone
- summary and description
- SEO title, meta description, meta keywords
- page title and page description
- live status
- group key
- CTA label
- recommended use cases
- related slugs
- capabilities
- inputs and outputs
- detail blocks
- editorial analysis/use/results/limitations blocks
- FAQ content for schema

Tool groups:

| Key | Title | Purpose | Label |
|---|---|---|---|
| `diagnostics` | Diagnostico tecnico | URL, landing, AdTech, and technical diagnostics | `EXISTING_APP` |
| `operations` | Operacion y etiquetado | UTM and operational URL utilities | `EXISTING_APP` |
| `qa_preview` | QA y vista previa | Creative QA and preview workflows | `EXISTING_APP` |

## SEO Landing Pages

Source: `pi_development/web/seo_pages.py`.

Each SEO page is rendered at `/<slug>/`, included in `SeoPageSitemap`, and uses `web/seo_landing_page.html`.

| Slug | Primary tool | Cluster | Purpose | Label |
|---|---|---|---|---|
| `validar-creatividad-html` | Creative QA Checklist | `creatividades` | Validate HTML creative before trafficking | `CONTENT_ASSET` |
| `preview-anuncios-html` | Creative Preview Lab | `creatividades` | Preview HTML ads/rich media in sandbox | `CONTENT_ASSET` |
| `debug-anuncios-web` | AdTech Debug Tool | `adtech` | Debug visible ad stack signals | `CONTENT_ASSET` |
| `debug-gpt-ads` | AdTech Debug Tool | `adtech` | Debug GPT Ads / Google Publisher Tag | `CONTENT_ASSET` |
| `como-crear-utms` | UTM Builder | `tracking` | Build UTM URLs correctly | `CONTENT_ASSET` |
| `auditoria-tecnica-web` | AI Auditor | `seo-performance` | Technical web audit guide | `CONTENT_ASSET` |
| `analizar-seo-pagina` | AI Auditor | `seo-performance` | Analyze page SEO signals | `CONTENT_ASSET` |
| `errores-creatividades-display` | Creative QA Checklist | `creatividades` | Common display creative errors | `CONTENT_ASSET` |
| `como-validar-tags-publicitarios` | Creative Preview Lab | `creatividades` | Validate ad tags and third-party tags | `CONTENT_ASSET` |
| `herramientas-adtech` | AdTech Debug Tool | multi-cluster hub | Main AdTech tools hub | `CORE_PUBLIC` |

Common fields:

- `slug`
- `title`
- `meta_description`
- `meta_keywords`
- `eyebrow`
- `h1`
- `description`
- `intro_paragraphs`
- `common_problems`
- `recommended_approach`
- `primary_tool_slug`
- `primary_tool_reason`
- `related_tool_slugs`
- `how_to_use`
- `faqs`
- `related_page_slugs`
- optional `hub_use_cases`
- optional `hub_sections`

## Knowledge Articles

Source: `pi_development/web/knowledge_pages.py`.

Each article is rendered at `/blog/<slug>/`, included in `KnowledgePageSitemap`, and uses `web/knowledge_article_page.html`.

| Slug | Cluster | Related tools | Purpose | Label |
|---|---|---|---|---|
| `como-validar-una-creatividad-html-antes-de-publicarla` | `creatividades` | Creative Preview Lab, Creative QA Checklist | Technical article about creative validation | `CONTENT_ASSET` |
| `errores-comunes-en-implementaciones-con-google-publisher-tag` | `adtech` | AdTech Debug Tool, AI Auditor | Technical article about GPT implementation errors | `CONTENT_ASSET` |
| `como-crear-urls-con-parametros-utm-correctamente` | `tracking` | UTM Builder | Technical article about UTM URL construction | `CONTENT_ASSET` |

Knowledge index fields:

- title
- meta description
- meta keywords
- eyebrow
- h1
- description
- intro and support content
- CTA text and target SEO slug

Article fields:

- slug
- title
- meta description
- meta keywords
- eyebrow
- cluster key
- h1
- description
- summary
- intro paragraphs
- sections and optional bullets
- related tool slugs
- related SEO page slugs
- related knowledge slugs
- FAQs

## Topic Clusters

Source: `pi_development/web/topic_clusters.py`.

| Key | Catalog anchor | Tools | SEO pages | Purpose | Label |
|---|---|---|---|---|---|
| `creatividades` | `qa_preview` | Creative Preview Lab, Creative QA Checklist | validar-creatividad-html, preview-anuncios-html, errores-creatividades-display, como-validar-tags-publicitarios | Creative validation, preview, QA | `CONTENT_ASSET` |
| `adtech` | `diagnostics` | AdTech Debug Tool | debug-anuncios-web, debug-gpt-ads, herramientas-adtech | Monetization diagnostics and GPT stack | `CONTENT_ASSET` |
| `seo-performance` | `diagnostics` | AI Auditor, Landing Performance Snapshot | auditoria-tecnica-web, analizar-seo-pagina | Technical SEO and performance checks | `CONTENT_ASSET` |
| `tracking` | `operations` | UTM Builder | como-crear-utms | Campaign URL tracking | `CONTENT_ASSET` |

Topic clusters connect tools, SEO pages, footer discovery links, tool page related links, SEO hubs, and knowledge pages.

## Portfolio / Work Entries

Source: `WORK_ITEMS`, `PORTFOLIO_WALL_VARIANTS`, and `PORTFOLIO_WALL_SEQUENCE` in `views.py`.

| Slug | Name | Category | Media | External URL | Label |
|---|---|---|---|---|---|
| `arcade-world` | Arcade World | Plataforma de experiencia | `web/img/arcade.mp4`, poster `web/img/1.png`, variants `arcade1.png`, `arcade2.png`, `arcade3.png` | `https://arcade-world.web.app/` | `CONTENT_ASSET` |
| `blog-int-emocional` | Blog Int Emocional | Sistema editorial | `web/img/2.png`, variants `blogie1.png`, `blogie2.png` | `https://blogintemocional.web.app/index.html` | `CONTENT_ASSET` |
| `indices-argentinos` | Indices Argentinos | Interfaz de datos | `web/img/indices.png`, variants `indice1.png`, `indice2.png`, `indice3.png` | `https://indices-argentinos.web.app/` | `CONTENT_ASSET` |
| `recetas-del-sapi` | Recetas del Sapi | Plataforma de contenido | `web/img/recetas.png` | `https://recetasdelsapi.web.app/` | `CONTENT_ASSET` |
| `juno-metales` | Juno Metales | Plataforma industrial | `web/img/juno.mp4`, poster `web/img/5.png` | `https://junometales.com/` | `CONTENT_ASSET` |
| `system-vesta` | System Vesta | Plataforma de servicios | `web/img/sistemvesta.mp4`, poster `web/img/4.png`, variant `sistemvesta1.png` | `https://systemvesta.com/` | `CONTENT_ASSET` |

## Draft / Placeholder Content

| Source | Content | Current exposure | Label |
|---|---|---|---|
| `company_pages.LABS_PAGE` | Operations Copilot, Publisher Systems Console, Evidence Workspace, Automation Blueprints | `/labs/`, nav/footer | `EXPERIMENTAL` |
| `company_pages.PRODUCTS_PAGE` | Operations Copilot, Publisher Systems Console placeholders | `/products/` | `EXPERIMENTAL` |
| older `views.BLOG_PAGE` | planned blog examples | not active in current `blog` view | `POSSIBLE_DUPLICATE` |

## Translations / Language

- Global `<html lang="en">` in `base.html`.
- Open Graph locale is `es_AR`.
- Visible content mixes English company positioning and Spanish technical tool/editorial content.
- No formal i18n translation files were found.
- `LANGUAGE_CODE` is `en-us`; `USE_I18N=True`.

Classification: `UNKNOWN_REQUIRES_REVIEW` for future localization decisions.

## Media Assets

Source: `static/web/img/`.

Images:

- `1.png`, `2.png`, `3.png`, `4.png`, `5.png`
- `arcade1.png`, `arcade2.png`, `arcade3.png`
- `blogie1.png`, `blogie2.png`
- `indices.png`, `indice1.png`, `indice2.png`, `indice3.png`
- `recetas.png`
- `sistemvesta1.png`
- `pi.png`, `piw.png`

Videos:

- `arcade.mp4`
- `juno.mp4`
- `sistemvesta.mp4`

Icons:

- `pi.ico`
- `ico2.ico`

All media must be preserved. Some assets are referenced by active work/home templates and Open Graph/favicon metadata; others may support older templates or future reconstruction.

## Structured Data Content

- Organization schema is hard-coded in `base.html`.
- FAQ schema is built from tool editorials and SEO/knowledge FAQs through `schema_utils.build_faq_schema_json`.
- ItemList schema is used on `/tools/` and `/blog/`.
- Sitemap content is generated from core route names, public tool slugs, public SEO slugs, and public knowledge slugs.
