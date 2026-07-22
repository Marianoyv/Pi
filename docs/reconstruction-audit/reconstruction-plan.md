# Reconstruction Foundation Plan

Date: 2026-07-12

This plan implements only an isolated institutional preview foundation. It does not replace the production homepage and does not alter existing route behavior, SEO behavior, tools, content slugs, legacy redirects, models, migrations, integrations, or deployment configuration.

## Existing Route to Proposed Route Mapping

| Current route | Current behavior | Proposed future role | This phase |
|---|---|---|---|
| `/` | Current company home | Future institutional home candidate | unchanged |
| `/solutions/` | Current company page | Future capabilities or solutions mapping candidate | unchanged |
| `/products/` | Current products/tools page | Future product overview candidate | unchanged |
| `/adtech/` | Current AdTech page | Future Ad Products candidate | unchanged |
| `/labs/` | Current labs placeholders | Future research/lab candidate | unchanged |
| `/insights/` | Current insights page | Future insights landing candidate | unchanged |
| `/about/` | Current about page | Future about page candidate | unchanged |
| `/contact/` | Current contact page | Future contact page candidate | unchanged |
| `/tools/`, `/tools/<slug>/` | Existing tool suite | Preserved app/tool surface | unchanged |
| `/blog/`, `/blog/<slug>/` | Existing knowledge system | Preserved editorial/content layer | unchanged |
| `/<seo-slug>/` | Existing SEO landing pages | Preserved SEO acquisition layer | unchanged |
| legacy redirects | Existing 301 compatibility routes | Preserved compatibility layer | unchanged |

## Routes That Stay Unchanged

All existing documented routes remain untouched: company pages, six live tools, ten SEO pages, three knowledge articles, work/approach/systems/policies pages, legacy redirects, admin, health, robots, sitemap index, and sitemap sections.

## New Routes

The new institutional foundation is isolated under `/rebuild/`:

- `/rebuild/` -> institutional Home preview
- `/rebuild/studio/` -> Studio preview
- `/rebuild/capabilities/` -> Capabilities preview
- `/rebuild/ad-products/` -> Ad Products preview
- `/rebuild/research/` -> Research preview
- `/rebuild/insights/` -> Insights preview
- `/rebuild/about/` -> About preview
- `/rebuild/contact/` -> Contact preview

These routes are intentionally not added to sitemaps in this phase.

## Route Conflicts

- `/`, `/insights/`, `/about/`, and `/contact/` already exist, so the preview uses `/rebuild/` routes instead.
- Top-level `/studio/`, `/capabilities/`, `/ad-products/`, and `/research/` would pass through the catch-all SEO route and return 404 unless added above it. To avoid SEO risk, they are deferred.
- `/apps/` is not created in this phase because existing tools must remain at `/tools/`.

## Template Inheritance Plan

- New templates live under `pi_development/web/templates/web/rebuild/`.
- `web/rebuild/base.html` is standalone and does not extend `web/base.html`.
- `web/rebuild/page.html` extends only `web/rebuild/base.html`.
- Rebuild header/footer components live under `web/rebuild/components/`.
- Existing templates, current navbar/footer, tool templates, and legacy templates are not modified.

## CSS Isolation Plan

- New CSS lives at `static/web/rebuild/site.css`.
- The stylesheet is loaded only by rebuild templates.
- Selectors are scoped under `.pi-site` where practical.
- Class prefixes use `pi-site-*`, `pi-nav-*`, `pi-hero-*`, `pi-section-*`, and `pi-footer-*`.
- No generic `.card`, `.button`, `.container`, `.hero`, `.nav`, or global body restyling is introduced.
- Existing `tools.css`, `base.css`, `navbar.css`, `footer.css`, and current page CSS remain untouched.

## JavaScript Isolation Plan

- No new JavaScript is introduced.
- Rebuild navigation is plain HTML.
- Existing `main.js` stays attached only to existing templates through their current base.

## Navigation Changes

The preview navigation includes:

- Studio
- Capabilities
- Ad Products
- Research
- Insights
- About
- Primary CTA: Bring a problem

The preview navigation does not promote Tools, Work, Portfolio, Systems, Approach, or Blog. Existing navigation on current pages is unchanged.

## Content Reuse Plan

- Rebuild pages use short structural placeholder copy marked as draft.
- No clients, metrics, products, testimonials, team members, research outcomes, partnerships, case studies, or project media are invented.
- Existing tools, articles, SEO pages, project data, and media remain preserved but are not promoted on the preview homepage.
- Future content approval can map current company pages and knowledge systems into the institutional IA without moving current URLs.

## SEO Impact Assessment

- No sitemap entries are changed.
- No robots behavior is changed.
- No canonical behavior is changed for existing pages.
- No redirects are added or changed.
- No existing metadata is changed.
- No noindex behavior is added to existing pages.
- New `/rebuild/` routes are preview-only and excluded from sitemap generation by omission.

## Rollback Procedure

To roll back this phase:

1. Remove the new `/rebuild/` URL patterns from `pi_development/web/urls.py`.
2. Remove the rebuild view wiring from `pi_development/web/views.py`.
3. Remove `pi_development/web/rebuild_pages.py`.
4. Remove `pi_development/web/templates/web/rebuild/`.
5. Remove `static/web/rebuild/`.
6. Remove the added rebuild regression tests from `pi_development/web/tests.py`.
7. Run `.\.venv\Scripts\python.exe manage.py check` and `.\.venv\Scripts\python.exe manage.py test pi_development.web`.

No database or deployment rollback is needed because this phase adds no migrations, data writes, or deployment changes.

## Files Expected To Be Created

- `docs/reconstruction-audit/reconstruction-plan.md`
- `pi_development/web/rebuild_pages.py`
- `pi_development/web/templates/web/rebuild/base.html`
- `pi_development/web/templates/web/rebuild/page.html`
- `pi_development/web/templates/web/rebuild/components/header.html`
- `pi_development/web/templates/web/rebuild/components/footer.html`
- `static/web/rebuild/site.css`

## Files Expected To Be Modified

- `pi_development/web/views.py`
- `pi_development/web/urls.py`
- `pi_development/web/tests.py`

## Preservation Confirmation

No existing feature will be deleted, moved, renamed, noindexed, redirected, deprecated, or visually refactored in this phase.
