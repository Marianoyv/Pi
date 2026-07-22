# Tools and Applications Inventory

The repository contains a public tools suite under `/tools/` and `/tools/<slug>/`. These are not just content pages: each live tool has forms, service logic, templates, examples, exports, insight scoring, and related SEO/editorial links.

## Tool Architecture

- Catalog source: `pi_development/web/tool_catalog.py`.
- Routing: `path("tools/", views.tools, name="tools")` and `path("tools/<slug:slug>/", views.tool_detail, name="tool_detail")`.
- Live routing switch: `LIVE_TOOL_CONFIG` in `pi_development/web/views.py`.
- Forms: `pi_development/web/forms.py`.
- Services: `pi_development/web/services/tools/`.
- Examples: `pi_development/web/tool_examples.py`.
- Shared result exports: `export_utils.py`.
- Shared insight summaries: `insight_utils.py`.
- Shared UI components: `tool_editorial_content.html`, `tool_example_block.html`, `tool_exports.html`, `tool_insight.html`, `tool_related_tools.html`, `tool_card.html`.
- Main stylesheet: `static/web/css/tools.css`.
- Shared JavaScript: `static/web/js/main.js` handles analyze-form disabling and copy buttons.

## Tools Index

| Name | Route | Group | Template | Live | Navigation exposure | Sitemap | SEO relevance | Independent from corporate site | Label |
|---|---|---|---|---|---|---|---|---|---|
| Tools index | `/tools/` | all groups | `web/tools_page.html` | n/a | linked from Products, SEO pages, topic cluster links; Product nav active | core sitemap | high; CollectionPage/ItemList schema | yes, but uses base/nav/footer and catalog data | `EXISTING_APP` |
| AI Auditor | `/tools/ai-auditor/` | diagnostics | `web/ai_auditor_page.html` | yes | tools index, Products, SEO pages, related tools | tools sitemap | high | yes, with shared base/assets/services | `EXISTING_APP` |
| Landing Performance Snapshot | `/tools/landing-performance-snapshot/` | diagnostics | `web/landing_snapshot_page.html` | yes | tools index, related tools, SEO pages | tools sitemap | high | yes | `EXISTING_APP` |
| AdTech Debug Tool | `/tools/adtech-debug-tool/` | diagnostics | `web/adtech_debug_tool_page.html` | yes | tools index, AdTech page, Products, SEO hub, related tools | tools sitemap | high | yes | `EXISTING_APP` |
| UTM Builder | `/tools/utm-builder/` | operations | `web/utm_builder_page.html` | yes | tools index, AdTech/Products pages, SEO pages | tools sitemap | high | yes | `EXISTING_APP` |
| Creative QA Checklist | `/tools/creative-qa-checklist/` | qa_preview | `web/creative_qa_page.html` | yes | tools index, AdTech/Products pages, SEO pages | tools sitemap | high | yes | `EXISTING_APP` |
| Creative Preview Lab | `/tools/creative-preview-lab/` | qa_preview | `web/creative_preview_lab_page.html` | yes | tools index, AdTech/Products pages, SEO pages | tools sitemap | high | yes | `EXISTING_APP` |

## Individual Tool Details

### AI Auditor

- Route: `/tools/ai-auditor/`.
- Purpose: audit one public URL for status, response, metadata, basic SEO, PageSpeed data when available, and optional AI summary.
- Main files: `tool_catalog.py`, `views.py`, `forms.py`, `ai_auditor.py`, `http_snapshot.py`, `pagespeed.py`, `openai_summary.py`, `ai_auditor_page.html`.
- Form: `AiAuditorForm`, extends URL normalization.
- APIs/external dependencies: target URL via `requests`; optional PageSpeed Insights API; optional OpenAI Chat Completions-compatible endpoint.
- Models: none.
- Current navigation exposure: tools index, Products preview, SEO pages, related tool blocks.
- SEO relevance: high, indexed, in sitemap, FAQ schema via editorial FAQs.
- Independent operation: can operate as an app if `/tools/ai-auditor/`, shared base template, CSS, JS, settings, and service files are preserved.
- Visible technical issues from static inspection: backend-only URL read does not execute JavaScript; PageSpeed and OpenAI are optional and may be unavailable; external URL failures are handled as partial/unavailable results.
- Classification: `EXISTING_APP`.

### Landing Performance Snapshot

- Route: `/tools/landing-performance-snapshot/`.
- Purpose: short technical read of HTTP status, response time, redirects, title, meta description, canonical, robots, and H1 count.
- Main files: `tool_catalog.py`, `forms.py`, `landing_snapshot.py`, `http_snapshot.py`, `landing_snapshot_page.html`.
- Form: `LandingPerformanceSnapshotForm`.
- APIs/external dependencies: target URL via `requests`.
- Models: none.
- Current navigation exposure: tools index, related tool blocks, SEO pages.
- SEO relevance: high, indexed, in sitemap, FAQ schema.
- Independent operation: yes, if shared tool UI and HTTP snapshot service are preserved.
- Visible technical issues from static inspection: backend-only read; no browser runtime, resource waterfall, or Core Web Vitals.
- Classification: `EXISTING_APP`.

### AdTech Debug Tool

- Route: `/tools/adtech-debug-tool/`.
- Purpose: detect visible AdTech monetization signals in the initial HTML response: GPT, Google Ad Manager, AdSense, Prebid, vendors, iframes, slots, refresh/lazy-load/targeting hints.
- Main files: `tool_catalog.py`, `forms.py`, `adtech_debug.py`, `http_snapshot.py`, `adtech_debug_tool_page.html`.
- Form: `AdTechDebugForm`.
- APIs/external dependencies: target URL via `requests`.
- Models: none.
- Current navigation exposure: tools index, AdTech page, Products page, SEO hub, related tool blocks.
- SEO relevance: high, indexed, in sitemap, FAQ schema.
- Independent operation: yes, if route and shared tool dependencies remain intact.
- Visible technical issues from static inspection: no JavaScript execution or network request capture; client-side ad stacks may be invisible; output correctly frames this as a limitation.
- Classification: `EXISTING_APP`.

### UTM Builder

- Route: `/tools/utm-builder/`.
- Purpose: construct campaign URLs with normalized UTM parameters while preserving existing non-UTM query parameters.
- Main files: `tool_catalog.py`, `forms.py`, `utm_builder.py`, `utm_builder_page.html`.
- Form: `UTMBuilderForm`.
- APIs/external dependencies: none beyond Python URL parsing and browser link opening.
- Models: none.
- Current navigation exposure: tools index, Products page, AdTech page, SEO pages, related tool blocks.
- SEO relevance: high, indexed, in sitemap, FAQ schema.
- Independent operation: yes, lowest external dependency among tools.
- Visible technical issues from static inspection: does not enforce team-specific naming taxonomy, presets, persistence, or batch generation.
- Classification: `EXISTING_APP`.

### Creative QA Checklist

- Route: `/tools/creative-qa-checklist/`.
- Purpose: manual input-based technical QA for creatives: dimensions, click path, tracking URLs, weight, device, sound/autoplay, serving context.
- Main files: `tool_catalog.py`, `forms.py`, `creative_qa.py`, `creative_qa_page.html`.
- Form: `CreativeQAChecklistForm`.
- APIs/external dependencies: none.
- Models: none.
- Current navigation exposure: tools index, AdTech page, Products page, SEO pages, related tool blocks.
- SEO relevance: high, indexed, in sitemap, FAQ schema.
- Independent operation: yes.
- Visible technical issues from static inspection: depends on manually entered data; does not inspect binary assets, ad server compatibility, or network behavior.
- Classification: `EXISTING_APP`.

### Creative Preview Lab

- Route: `/tools/creative-preview-lab/`.
- Purpose: render pasted HTML creatives or third-party tags in a sandboxed preview and detect scripts, iframes, links, media, macros, placeholders, external resources, and frame-busting patterns.
- Main files: `tool_catalog.py`, `forms.py`, `creative_preview_lab.py`, `creative_preview_lab_page.html`.
- Form: `CreativePreviewLabForm`.
- APIs/external dependencies: browser iframe rendering of submitted markup; no backend external API.
- Models: none.
- Current navigation exposure: tools index, AdTech page, Products page, SEO pages, related tool blocks.
- SEO relevance: high, indexed, in sitemap, FAQ schema.
- Independent operation: yes, if sandbox template and tool JS/CSS remain.
- Visible technical issues from static inspection: preview is intentionally partial; does not simulate SafeFrame, ad server serving, network tracking, or clicks; frame-busting patterns are blocked.
- Classification: `EXISTING_APP`.

## Other App-Like Surfaces

| Surface | Route | Purpose | Files | Exposure | Label |
|---|---|---|---|---|---|
| Django admin | `/admin/` when enabled | Admin for `Servicio` and Django auth/session models | `admin.py`, `models.py`, Django admin static | no public nav | `INTERNAL` |
| Health check | `/health`, `/healthz/` | Cloud/container health response | `health.py` | no public nav | `INTERNAL` |
| Sitemap system | `/sitemap.xml`, `/sitemap-<section>.xml` | Search engine discovery | `sitemaps.py` | robots.txt | `INTERNAL` |
| Contact WhatsApp handler | `/contact/` page plus JS | Opens WhatsApp message from client-side form handler where present | `main.js`, contact templates, contact settings | contact CTAs | `CORE_PUBLIC` |
| Products/Labs placeholders | `/products/`, `/labs/` | Future product surfaces such as Operations Copilot and Publisher Systems Console | `company_pages.py`, `company_page.html` | primary nav | `EXPERIMENTAL` |

## Preservation Requirements

- Preserve all tool slugs and route names until owner approves a migration strategy.
- Preserve `LIVE_TOOL_CONFIG` behavior, form classes, service modules, templates, tests, and sitemap inclusion for all live tools.
- If future navigation hides tools, keep direct routes accessible and indexed unless a separate SEO decision is approved.
- Do not merge duplicate-looking tool templates without proving no feature-specific fields, context keys, or result blocks are lost.
- Keep `tools.css` and `main.js` behavior available to tool pages even if the corporate site is rebuilt.
