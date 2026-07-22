# Dependency Map

This file maps shared dependencies so a future corporate-site reconstruction does not accidentally break existing tools, content, SEO pages, or infrastructure.

## Shared App Dependencies

| Dependency | Used by | Risk if changed | Preserve strategy |
|---|---|---|---|
| `web/base.html` | all active public templates | breaks metadata, global assets, schema, scripts, favicon | keep block contract or provide compatible replacement |
| `components/navbar.html` | public pages | breaks primary nav and active states | preserve or deliberately replace with route-compatible nav |
| `components/footer.html` | public pages | breaks footer, policies link, discovery SEO hubs, contact/social links | preserve footer SEO hub logic |
| `context_processors.site_settings` | base/footer/canonical/contact/analytics | breaks canonical, contact data, analytics, footer SEO links | preserve context keys |
| `static/web/css/base.css` | all pages | breaks design tokens and global UI | keep tokens or migrate consumers |
| `static/web/css/tools.css` | all tool pages, tools index, SEO/article related blocks | breaks live tool UI | keep available to tools independent of corporate design |
| `static/web/js/main.js` | nav, contact, tool forms, copy buttons, older animations | breaks tool submit/copy UX and nav | preserve behavior or split safely |

## Route and Sitemap Dependencies

| Source | Downstream dependencies |
|---|---|
| `pi_development/web/urls.py` | route names used by templates, redirects, sitemaps, tests, related links |
| `tool_catalog.get_public_tool_slugs()` | `ToolPageSitemap`, `/tools/`, related tools, topic clusters |
| `seo_pages.get_public_seo_page_slugs()` | `SeoPageSitemap`, footer discovery hubs, related SEO links, topic clusters |
| `knowledge_pages.get_public_knowledge_slugs()` | `KnowledgePageSitemap`, `/blog/`, related knowledge links |
| `topic_clusters.TOPIC_CLUSTERS` | tools page groups, tool related guide links, SEO hub sections, footer discovery hubs |
| catch-all route `/<slug>/` | all SEO landing pages; sensitive to new top-level route collisions |

## Tool Service Dependencies

| Tool | Forms | Services | Shared utilities | External services |
|---|---|---|---|---|
| AI Auditor | `AiAuditorForm` | `run_ai_auditor` | `http_snapshot`, `pagespeed`, `openai_summary`, `insight_utils`, `export_utils` | target URLs, optional PageSpeed, optional OpenAI |
| Landing Performance Snapshot | `LandingPerformanceSnapshotForm` | `run_landing_performance_snapshot` | `http_snapshot`, `insight_utils`, `export_utils` | target URLs |
| AdTech Debug Tool | `AdTechDebugForm` | `run_adtech_debug` | `http_snapshot`, `insight_utils`, `export_utils` | target URLs |
| UTM Builder | `UTMBuilderForm` | `run_utm_builder` | URL normalization, `export_utils` | none |
| Creative QA Checklist | `CreativeQAChecklistForm` | `run_creative_qa` | `insight_utils`, `export_utils` | none |
| Creative Preview Lab | `CreativePreviewLabForm` | `run_creative_preview_lab` | HTML parser, sandbox builder, `insight_utils`, `export_utils` | browser iframe execution |

## Public Page Dependencies

| Page group | Data source | Template | CSS | Shared links |
|---|---|---|---|---|
| Corporate home | `company_pages.HOME_PAGE`, `views.WORK_ITEMS` | `company_home.html` | `company.css` | Products, Contact, AdTech, Solutions, external work URLs |
| Company pages | `company_pages.PAGE_BY_SLUG` | `company_page.html` | `company.css`, `tools.css` | tool catalog, knowledge groups, contact |
| Systems | `views.SYSTEMS_PAGE` | `systems_page.html` | `services_overview.css` | Contact |
| Work | `views.WORK_PAGE`, `views.WORK_ITEMS` | `work_page.html` | `portfolio.css` | external work URLs |
| Approach | `views.APPROACH_PAGE` | `approach_page.html` | `content_page.css` | Contact |
| Blog index | `knowledge_pages`, `topic_clusters` | `blog_page.html` | `blog.css`, `tools.css` | knowledge articles, AdTech hub |
| Knowledge articles | `knowledge_pages`, `tool_catalog`, `seo_pages`, `topic_clusters` | `knowledge_article_page.html` | `content_page.css`, `tools.css` | related tools/pages/articles |
| SEO pages | `seo_pages`, `tool_catalog`, `topic_clusters` | `seo_landing_page.html` | `content_page.css`, `tools.css` | primary tools, related tools, hub groups |
| Policies | template content | `policies.html` | `policies.css` | footer |

## Content Interlinking

Tools link to:

- related tools by `related_slugs`
- related SEO pages by topic cluster
- catalog anchors by topic cluster
- examples by `tool_examples`

SEO pages link to:

- primary tool
- related tools
- related SEO pages
- topic cluster catalog anchors
- hub sections where configured

Knowledge pages link to:

- related tools
- related SEO pages
- related knowledge pages
- topic cluster catalog anchors
- `/blog/`
- `/herramientas-adtech/`

Footer links to:

- primary company routes
- `/policies/`
- discovery SEO hub pages from the first page in each topic cluster
- contact/social URLs

## Authentication and Admin Dependencies

| Dependency | Used by | Notes |
|---|---|---|
| `django.contrib.auth` | admin/auth stack | installed globally |
| `django.contrib.admin` | optional `/admin/` | route inserted when `ENABLE_ADMIN` true |
| `Servicio` model | admin | only custom model registered |
| local SQLite | admin/local data | active in local settings |
| production dummy DB | production app | admin/data persistence not viable without DB change |

## Deployment Dependencies

| Resource | Depends on | Notes |
|---|---|---|
| Docker image | requirements, manage.py, project, static source | `collectstatic` runs at build time |
| Cloud Run service | image, env vars, optional secrets | `deploy.sh` deploys unauthenticated |
| Firebase Hosting | Cloud Run service ID and region | rewrites all traffic to Cloud Run |
| Static assets | `static/web`, admin static, WhiteNoise | no separate Firebase static hosting in current architecture |

## Fragile Shared Seams

- `company_page.html` renders many different page objects; field changes affect several routes at once.
- `tools.css` is shared by tools and content pages; visual reconstruction should not remove it from tool surfaces.
- `main.js` mixes current and legacy behaviors. Splitting it requires testing nav, copy buttons, analyze forms, contact, and older templates.
- The production database is dummy; adding any persistent feature is an infrastructure change, not a template-only change.
- The catch-all SEO route should be reviewed before adding new top-level corporate pages.
