# Route Inventory

All routes are defined by `pi_development/urls.py` and `pi_development/web/urls.py`. Public views are in `pi_development.web.views`. Authentication is open unless noted. Indexation status is based on templates and sitemap code, not live Search Console data.

## Project-Level Routes

| URL | Name | App / view | Template | Auth | Indexation / sitemap | Navigation / links | Purpose and status | Label |
|---|---|---|---|---|---|---|---|---|
| `/health` | `health` | `pi_development.health.health_check` | none | none | not in sitemap; should not be content-indexed | infrastructure only | Plain `ok` health response with `Cache-Control: no-store`; operational | `INTERNAL` |
| `/healthz/` | `healthz` | `pi_development.health.health_check` | none | none | not in sitemap; should not be content-indexed | infrastructure only | Alias health endpoint; operational | `INTERNAL` |
| `/admin/` | Django admin | `django.contrib.admin.site.urls`, inserted only if `settings.ENABLE_ADMIN` | Django admin templates/static | staff/superuser | not in sitemap; should not be indexed | no public nav | Admin for registered model `Servicio`; production availability depends on `ENABLE_ADMIN`; production DB is dummy unless changed | `INTERNAL` |
| all other paths | included URLConf | `pi_development.web.urls` | varies | varies | varies | public app | Main website and tools | varies |

## Static Public Pages

| URL | Name | View | Template | Auth | Indexation / sitemap | Navigation visibility | Internal links pointing to it | Purpose and status | Dependencies | Label |
|---|---|---|---|---|---|---|---|---|---|---|
| `/` | `index` | `index` | `web/company_home.html` | none | `index, follow`; included in `CorePageSitemap` | primary nav, footer, logo | nav logo, Home nav, footer | Corporate home for software, AI systems, automation, AdTech signals; operational | `company_pages.HOME_PAGE`, `WORK_ITEMS`, `base.html`, `company.css`, navbar/footer | `CORE_PUBLIC` |
| `/favicon.ico` | `favicon` | `favicon` | redirect | none | not sitemap | browser asset request | base favicon tags | Permanent redirect to `static/web/img/pi.ico`; operational | `staticfiles_storage` | `CONTENT_ASSET` |
| `/solutions/` | `solutions` | `solutions` | `web/company_page.html` | none | `index, follow`; core sitemap | primary nav, footer | home cards, footer core areas | Corporate solutions page; operational | `company_pages.SOLUTIONS_PAGE`, `company.css`, `tools.css` | `CORE_PUBLIC` |
| `/products/` | `products` | `products` | `web/company_page.html` | none | `index, follow`; core sitemap | primary nav, footer | home CTA/cards, footer | Productized tools overview and product placeholders; operational | `company_pages.PRODUCTS_PAGE`, `tool_catalog.get_tools` | `CORE_PUBLIC` |
| `/adtech/` | `adtech` | `adtech` | `web/company_page.html` | none | `index, follow`; core sitemap | primary nav, footer | home signal, footer | AdTech and publisher tools page; operational | `company_pages.ADTECH_PAGE`, filtered tool catalog | `CORE_PUBLIC` |
| `/labs/` | `labs` | `labs` | `web/company_page.html` | none | `index, follow`; core sitemap | primary nav, footer | product placeholders | Future product/lab concepts; operational content shell | `company_pages.LABS_PAGE` | `EXPERIMENTAL` |
| `/insights/` | `insights` | `insights` | `web/company_page.html` | none | `index, follow`; core sitemap | primary nav, footer | nav/footer; content cards when groups present | Editorial and technical writing landing; operational | `company_pages.INSIGHTS_PAGE`, `knowledge_pages`, `topic_clusters` | `CORE_PUBLIC` |
| `/systems/` | `systems` | `systems` | `web/systems_page.html` | none | `index, follow`; core sitemap | not primary nav in current navbar; linked from legacy redirects and older templates | legacy service redirects, old hero/servicios templates | Architecture/digital systems page; operational | `views.SYSTEMS_PAGE`, `services_overview.css` | `CORE_PUBLIC` |
| `/tools/` | `tools` | `tools` | `web/tools_page.html` | none | `index, follow`; core sitemap | not primary nav directly; Product nav active for `/tools/` paths | Products, AdTech, SEO pages, footer related components | Tool suite index with groups and topic clusters; operational | `tool_catalog`, `topic_clusters`, `schema_utils`, `tools.css` | `EXISTING_APP` |
| `/work/` | `work` | `work` | `web/work_page.html` | none | `index, follow`; core sitemap | not primary nav; linked from older portfolio template and home content | case studies/home sections | Case studies/work overview; operational | `WORK_PAGE`, `WORK_ITEMS`, `portfolio.css` | `CORE_PUBLIC` |
| `/approach/` | `approach` | `approach` | `web/approach_page.html` | none | `index, follow`; core sitemap | not primary nav; linked from older process template | legacy process redirect target | Method/approach page; operational | `APPROACH_PAGE`, `content_page.css` | `CORE_PUBLIC` |
| `/about/` | `about` | `about` | `web/company_page.html` | none | `index, follow`; core sitemap | primary nav, footer | old nosotros template | About page; operational | `company_pages.ABOUT_PAGE` | `CORE_PUBLIC` |
| `/contact/` | `contact` | `contact` | `web/company_page.html` | none | `index, follow`; core sitemap | primary nav, footer, CTAs | CTAs across pages | Contact page; operational | `company_pages.CONTACT_PAGE`, contact env settings | `CORE_PUBLIC` |
| `/blog/` | `blog` | `blog` | `web/blog_page.html` | none | `index, follow`; core sitemap | not primary nav; Insights nav active for `/blog/` paths | knowledge pages back-link, Insights layer | Knowledge article listing; operational | `knowledge_pages`, `topic_clusters`, ItemList schema | `CORE_PUBLIC` |
| `/policies/` | `policies` | `policies` | `web/policies.html` | none | `index, follow` by default; not in sitemap | footer only | footer Core areas | Policies page; operational but not sitemap-listed | `policies.css` | `CONTENT_ASSET` |
| `/robots.txt` | `robots_txt` | `robots_txt` | none | none | robots endpoint; not sitemap item | external crawlers | direct route | Allows all and points to sitemap URL; operational | `settings.SITE_URL`, `reverse("sitemap")` | `INTERNAL` |
| `/sitemap.xml` | `sitemap` | `sitemap_index` | `sitemap_index.xml` via Django template lookup | none | sitemap index | crawlers, robots.txt | robots endpoint | Custom sitemap index for sections; operational check passed, depends on Django package template unless project-local template is added | `sitemaps.py`, Django sitemap framework | `INTERNAL` |
| `/sitemap-<section>.xml` | `sitemap_section` | `django.contrib.sitemaps.views.sitemap` | Django sitemap templates | none | sitemap section endpoint | sitemap index | sitemap index | Section XML for `pages`, `tools`, `seo`, `content`; operational | `CorePageSitemap`, `ToolPageSitemap`, `SeoPageSitemap`, `KnowledgePageSitemap` | `INTERNAL` |

## Live Tool Routes

All tool pages share URL pattern `/tools/<slug>/`, route name `tool_detail`, view `tool_detail`, open access, `index, follow`, `ToolPageSitemap`, and Product nav active state. They are linked from `/tools/`, `/products/`, `/adtech/`, related-tool components, SEO pages, knowledge pages, and topic-cluster blocks.

| URL | Tool | Template | Main service/form | Purpose and status | Dependencies | Label |
|---|---|---|---|---|---|---|
| `/tools/ai-auditor/` | AI Auditor | `web/ai_auditor_page.html` | `AiAuditorForm`, `run_ai_auditor` | Live URL auditor for HTTP/HTML signals, PageSpeed optional data, and optional OpenAI summary | `http_snapshot`, `pagespeed`, `openai_summary`, `insight_utils`, `export_utils` | `EXISTING_APP` |
| `/tools/landing-performance-snapshot/` | Landing Performance Snapshot | `web/landing_snapshot_page.html` | `LandingPerformanceSnapshotForm`, `run_landing_performance_snapshot` | Live short landing snapshot for HTTP, metadata, H1, redirects, and recommendations | `http_snapshot`, `insight_utils`, `export_utils` | `EXISTING_APP` |
| `/tools/adtech-debug-tool/` | AdTech Debug Tool | `web/adtech_debug_tool_page.html` | `AdTechDebugForm`, `run_adtech_debug` | Live AdTech signal detector for GPT, GAM, AdSense, Prebid, wrappers, iframes, slots | `http_snapshot`, pattern definitions, `insight_utils`, `export_utils` | `EXISTING_APP` |
| `/tools/utm-builder/` | UTM Builder | `web/utm_builder_page.html` | `UTMBuilderForm`, `run_utm_builder` | Live URL builder preserving existing query params and adding normalized UTM values | URL parsing utilities, form normalization, `export_utils` | `EXISTING_APP` |
| `/tools/creative-qa-checklist/` | Creative QA Checklist | `web/creative_qa_page.html` | `CreativeQAChecklistForm`, `run_creative_qa` | Live manual QA checklist for creative dimensions, click path, tracking, weight, autoplay, serving context | rule tables, `insight_utils`, `export_utils` | `EXISTING_APP` |
| `/tools/creative-preview-lab/` | Creative Preview Lab | `web/creative_preview_lab_page.html` | `CreativePreviewLabForm`, `run_creative_preview_lab` | Live sandbox preview and technical inspection for HTML creatives and third-party tags | HTML parser, sandbox document builder, macro/frame-busting detection, `insight_utils`, `export_utils` | `EXISTING_APP` |

## Knowledge Article Routes

All knowledge pages share `/blog/<slug>/`, route name `knowledge_page`, view `knowledge_page`, template `web/knowledge_article_page.html`, open access, `index, follow`, `KnowledgePageSitemap`, and links from `/blog/`, `/insights/`, related article chips, SEO pages, and topic-cluster sections.

| URL | Cluster | Purpose and status | Dependencies | Label |
|---|---|---|---|---|
| `/blog/como-validar-una-creatividad-html-antes-de-publicarla/` | `creatividades` | Technical article on validating HTML creatives before publishing; operational | related tools: Creative Preview Lab, Creative QA Checklist; FAQ schema | `CONTENT_ASSET` |
| `/blog/errores-comunes-en-implementaciones-con-google-publisher-tag/` | `adtech` | Technical article on GPT implementation errors; operational | related tools: AdTech Debug Tool, AI Auditor; FAQ schema | `CONTENT_ASSET` |
| `/blog/como-crear-urls-con-parametros-utm-correctamente/` | `tracking` | Technical article on constructing UTM URLs; operational | related tool: UTM Builder; FAQ schema | `CONTENT_ASSET` |

## SEO Landing Page Routes

All SEO pages share catch-all pattern `/<slug>/`, route name `seo_page`, view `seo_page`, template `web/seo_landing_page.html`, open access, `index, follow`, `SeoPageSitemap`, and links from footer discovery hubs, `/tools/`, related SEO chips, knowledge pages, and tool related sections.

Important collision rule: this catch-all appears after explicit routes, so explicit URLs such as `/tools/`, `/blog/`, `/robots.txt`, and `/sitemap.xml` take precedence.

| URL | Primary tool | Topic cluster | Purpose and status | Label |
|---|---|---|---|---|
| `/validar-creatividad-html/` | Creative QA Checklist | `creatividades` | SEO guide for validating HTML creatives before trafficking; operational | `CONTENT_ASSET` |
| `/preview-anuncios-html/` | Creative Preview Lab | `creatividades` | SEO guide for previewing HTML ads in a controlled environment; operational | `CONTENT_ASSET` |
| `/debug-anuncios-web/` | AdTech Debug Tool | `adtech` | SEO guide for debugging visible web ad stack signals; operational | `CONTENT_ASSET` |
| `/debug-gpt-ads/` | AdTech Debug Tool | `adtech` | SEO guide for GPT Ads / Google Publisher Tag debug; operational | `CONTENT_ASSET` |
| `/como-crear-utms/` | UTM Builder | `tracking` | SEO guide for UTM construction; operational | `CONTENT_ASSET` |
| `/auditoria-tecnica-web/` | AI Auditor | `seo-performance` | SEO guide for technical web audits; operational | `CONTENT_ASSET` |
| `/analizar-seo-pagina/` | AI Auditor | `seo-performance` | SEO guide for analyzing page SEO signals; operational | `CONTENT_ASSET` |
| `/errores-creatividades-display/` | Creative QA Checklist | `creatividades` | SEO guide for repeated display creative errors; operational | `CONTENT_ASSET` |
| `/como-validar-tags-publicitarios/` | Creative Preview Lab | `creatividades` | SEO guide for validating ad tags and third-party tags; operational | `CONTENT_ASSET` |
| `/herramientas-adtech/` | AdTech Debug Tool | multi-cluster hub | SEO hub for the full AdTech tool suite; operational | `CORE_PUBLIC` |

## Legacy Redirect Routes

These are route-level compatibility surfaces. They must be preserved unless the owner explicitly approves a redirect strategy change.

| URL | Name | View | Auth | Indexation / sitemap | Navigation / links | Current target | Status | Label |
|---|---|---|---|---|---|---|---|---|
| `/services/` | `services` | `legacy_services` | none | not in sitemap; 301 | not current nav | `/systems/` via route name `systems` | Permanent redirect | `LEGACY_PRESERVE` |
| `/services/web-development/` | `service_page` | `legacy_service_page` | none | not in sitemap; 301 | old service paths | `/systems/` | Permanent redirect for allowed legacy slug | `LEGACY_PRESERVE` |
| `/services/ux-ui/` | `service_page` | `legacy_service_page` | none | not in sitemap; 301 | old service paths | `/systems/` | Permanent redirect for allowed legacy slug | `LEGACY_PRESERVE` |
| `/services/marketing/` | `service_page` | `legacy_service_page` | none | not in sitemap; 301 | old service paths | `/systems/` | Permanent redirect for allowed legacy slug | `LEGACY_PRESERVE` |
| `/services/seo/` | `service_page` | `legacy_service_page` | none | not in sitemap; 301 | old service paths | `/systems/` | Permanent redirect for allowed legacy slug | `LEGACY_PRESERVE` |
| `/services/<unknown>/` | `service_page` | `legacy_service_page` | none | 404 | none | none | Unknown legacy slugs 404 | `UNKNOWN_REQUIRES_REVIEW` |
| `/portfolio/` | `portfolio` | `legacy_portfolio` | none | not in sitemap; 301 | older template links | `/work/` | Permanent redirect | `LEGACY_PRESERVE` |
| `/process/` | `process_page` | `legacy_process` | none | not in sitemap; 301 | older template links | `/approach/` | Permanent redirect | `LEGACY_PRESERVE` |
| `/resources/` | `resources_page` | `legacy_resources` | none | not in sitemap; 301 | older template links | `/tools/` | Permanent redirect | `LEGACY_PRESERVE` |

## Route-Level Fragility Notes

- The catch-all SEO route `/<slug>/` is intentionally broad. Future reconstruction must keep explicit routes above it and must not introduce collisions without tests.
- `/tools/<slug>/` switches templates and services based on `LIVE_TOOL_CONFIG`; adding or renaming slugs affects sitemap, related links, forms, examples, tests, and SEO links.
- Production admin depends on `ENABLE_ADMIN`, but production uses a dummy database. Enabling admin in production without a real database plan is fragile.
- Sitemap index uses `TemplateResponse(..., "sitemap_index.xml")`; no project-local `sitemap_index.xml` was found, so current behavior depends on Django's package template lookup.
- Legacy redirects are covered by tests and should not be removed during public reconstruction.
