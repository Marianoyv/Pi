# SEO Inventory

This inventory documents SEO behavior visible from code. It does not use live crawl data, Search Console, Analytics, or production logs.

## Robots

There are two relevant robots sources:

- Repository root `robots.txt`: static file with allow-all and sitemap reference.
- Dynamic Django route `/robots.txt`: `views.robots_txt`, which returns:
  - `User-agent: *`
  - `Allow: /`
  - `Sitemap: <SITE_URL>/sitemap.xml` or request absolute URI fallback

The dynamic route is the active Django route when traffic is served through the app. Keep both preserved until deployment behavior is verified.

Classification: `INTERNAL`.

## XML Sitemap

Routes:

- `/sitemap.xml`: custom sitemap index view `sitemap_index`.
- `/sitemap-<section>.xml`: Django sitemap section view.

Sitemap sections:

| Section | Class | Items | Label |
|---|---|---|---|
| `pages` | `CorePageSitemap` | index, solutions, products, adtech, labs, insights, systems, tools, blog, work, approach, about, contact | `CORE_PUBLIC` |
| `tools` | `ToolPageSitemap` | all public tool slugs from `get_public_tool_slugs()` | `EXISTING_APP` |
| `seo` | `SeoPageSitemap` | all public SEO slugs from `get_public_seo_page_slugs()` | `CONTENT_ASSET` |
| `content` | `KnowledgePageSitemap` | all public knowledge slugs from `get_public_knowledge_slugs()` | `CONTENT_ASSET` |

Sitemap properties:

- Protocol/domain derived from `settings.SITE_URL` when available.
- Core pages priority `0.8`, changefreq `monthly`.
- Tool pages priority `0.9`, changefreq `weekly`.
- SEO pages priority `0.8`, changefreq `monthly`.
- Knowledge pages priority `0.7`, changefreq `monthly`.

Fragility:

- No project-local `sitemap_index.xml` was found; current custom sitemap index depends on Django template lookup.
- `/policies/`, health endpoints, admin, favicon, robots, and legacy redirects are not sitemap-listed.

## Canonical Handling

Source: `pi_development/context_processors.py` and `base.html`.

- `site_settings` computes `canonical_url` as `SITE_URL.rstrip("/") + request.path` when `SITE_URL` exists.
- Fallback is `request.build_absolute_uri(request.path)`.
- `base.html` emits `<link rel="canonical" href="...">` through a block.
- Tests assert canonical tags for tools and SEO pages.

Preservation requirement: any new base template must preserve canonical block behavior or explicitly replace it with an equivalent.

## Indexation Defaults

- `base.html` emits `<meta name="robots" content="index, follow">` by default.
- No route-specific noindex logic was found.
- Legacy redirect routes return 301 and are not sitemap-listed.
- Admin and health are not sitemap-listed but also do not appear to have explicit noindex headers/meta because they are not regular content pages.

Classification: `CORE_PUBLIC` for public pages, `INTERNAL` for infrastructure.

## Metadata

Global defaults in `base.html`:

- meta description
- meta keywords
- canonical
- Open Graph site name/type/locale/title/description/image/url
- Twitter card/title/description/image
- title tag
- Google site verification when configured

Page-level sources:

- Company pages: `seo_title`, `meta_description`, `meta_keywords`.
- Tool pages: `seo_title`, `meta_description`, `meta_keywords`, editorial FAQs.
- SEO landing pages: `title`, `meta_description`, `meta_keywords`, FAQs.
- Knowledge pages: `title`, `meta_description`, `meta_keywords`, FAQs.
- Tools index: `TOOLS_INDEX_PAGE` metadata.
- Knowledge index: `KNOWLEDGE_INDEX_PAGE` metadata.

Potential issue:

- Some Spanish strings appear mojibake-encoded in source/output examples, likely inherited file encoding/content. This should be reviewed before reconstruction but not corrected during this audit.

## Open Graph and Twitter

Source: `base.html`.

- Default image: `static/web/img/pi.png` combined with `site_url`.
- Default OG type: `website`.
- Knowledge article template tests expect `og:type` as `article`.
- `og:locale` is `es_AR`.
- Twitter card is `summary_large_image`.

Preservation requirement: keep default image, site name, URL, and page override blocks.

## Structured Data

| Schema | Source | Pages | Label |
|---|---|---|---|
| Organization | hard-coded in `base.html` | all pages extending base | `CORE_PUBLIC` |
| FAQPage | `schema_utils.build_faq_schema_json` | tool pages, SEO pages, knowledge pages with FAQs | `CONTENT_ASSET` |
| ItemList | `schema_utils.build_item_list_schema_json` | `/tools/`, `/blog/` | `CORE_PUBLIC` |

Tests cover schema presence for tools, SEO pages, and tools index.

## Language Alternates

- No `hreflang` or language alternate tags were found.
- No translation files were found.
- Site mixes English and Spanish content with `<html lang="en">` and `og:locale` of `es_AR`.

Classification: `UNKNOWN_REQUIRES_REVIEW`.

## Redirects

Permanent redirects:

- `/favicon.ico` -> static favicon URL.
- `/services/` -> `/systems/`.
- `/services/web-development/` -> `/systems/`.
- `/services/ux-ui/` -> `/systems/`.
- `/services/marketing/` -> `/systems/`.
- `/services/seo/` -> `/systems/`.
- `/portfolio/` -> `/work/`.
- `/process/` -> `/approach/`.
- `/resources/` -> `/tools/`.

Preservation requirement: do not remove redirects during reconstruction. If URL strategy changes, map old routes to explicit replacement targets and test them.

## Pagination

- Sitemap sections support pagination through Django sitemap paginator and custom sitemap index query `?p=<page>`.
- No public article/tool listing pagination was found.

## Article SEO

Knowledge articles:

- Have title, meta description, meta keywords, h1, description, sections, related tools, related SEO pages, related knowledge pages, FAQs, and schema.
- Included in content sitemap.
- Linked from `/blog/`, `/insights/` content sections, related chips, and topic clusters.

Classification: `CONTENT_ASSET`.

## Tool SEO

Tool pages:

- Have SEO title, meta description, meta keywords, single H1 according to tests, FAQ schema, canonical, sitemap inclusion, related tools, related SEO guides, topic-cluster links, examples, and editorial content.
- Tool index has collection/item list schema and grouped anchors.

Classification: `EXISTING_APP`.

## Duplicate or Broken Metadata Detectable From Code

- Root `robots.txt` and dynamic `/robots.txt` duplicate the same general role; verify deployment source before removing either.
- `base.html` hard-codes Organization `url` and `logo` as `https://pidevelopment.web.app` even though `SITE_URL` is configurable elsewhere.
- Language/locale consistency should be reviewed: `<html lang="en">`, `LANGUAGE_CODE="en-us"`, `og:locale="es_AR"`, mixed English/Spanish content.
- Some source strings show mojibake; do not rewrite without owner-approved content/encoding pass.
