# Rebuild Content Implementation

## Scope

This phase implemented the English institutional website content only inside the isolated `/rebuild/` environment. The production homepage, existing company pages, tools, SEO pages, knowledge articles, legacy redirects, sitemap behavior, robots behavior, templates, stylesheets, JavaScript, models, migrations, media, and deployment configuration were not intentionally removed, renamed, moved, redirected, noindexed, or replaced.

## Files Created

- `pi_development/web/rebuild_forms.py`
- `pi_development/web/rebuild_pages.py`
- `pi_development/web/templates/web/rebuild/page.html`
- `static/web/rebuild/site.js`
- `docs/reconstruction-audit/rebuild-content-implementation.md`
- `docs/reconstruction-audit/rebuild-visual-system.md`

## Files Modified

- `pi_development/web/views.py`
- `pi_development/web/templates/web/rebuild/base.html`
- `pi_development/web/templates/web/rebuild/page.html`
- `pi_development/web/templates/web/rebuild/components/header.html`
- `pi_development/web/templates/web/rebuild/components/footer.html`
- `static/web/rebuild/site.css`
- `pi_development/web/tests.py`

Existing rebuild foundation files remain in use:

- `pi_development/web/templates/web/rebuild/base.html`
- `pi_development/web/templates/web/rebuild/components/header.html`

## Content Implemented

The rebuild now uses English public content and `<html lang="en">`.

Implemented routes:

- `/rebuild/`
- `/rebuild/studio/`
- `/rebuild/capabilities/`
- `/rebuild/ad-products/`
- `/rebuild/research/`
- `/rebuild/insights/`
- `/rebuild/about/`
- `/rebuild/contact/`

The rebuild navigation is limited to:

- Studio
- Capabilities
- Ad Products
- Research
- Insights
- About
- Bring a problem

The Pi logo links to `/rebuild/`. The rebuild footer includes Pi Development, the studio descriptor, institutional rebuild links, Contact, and the closing line "Think clearly. Build what matters."

The visual implementation adds a rebuild-only skip link, main landmark target, sticky header state, accessible mobile navigation button, section numbering, structural system diagrams, contact error summary, and future analytics-ready `data-pi-event` attributes. These additions do not send analytics events and do not alter production templates.

## Existing Content Reused

No existing Spanish knowledge articles were displayed on `/rebuild/insights/` because the rebuild is English-only in this phase and the available article set would conflict with the requested editorial positioning. The insights page therefore renders the supplied heading and introduction without fake or empty placeholders.

The existing `CONTACT_EMAIL` setting is reused for contact notification when configured. No database model, migration, or persistent lead-storage schema was added.

## Contact Behavior

The `/rebuild/contact/` route uses a rebuild-only Django form with server-side validation and CSRF protection. Fields implemented:

- Name
- Email
- Company or organization
- Role
- Project type
- Problem or opportunity
- Current situation
- Desired outcome
- Timeline
- Budget range
- Relevant links

Project type options:

- Software system
- MVP
- AI or automation
- Internal tool
- AdTech solution
- Technical research
- Product collaboration
- Other

Successful submissions attempt to send an email through Django's existing email channel when `CONTACT_EMAIL` is configured, then render the requested success message. A mailto handoff link is provided when `CONTACT_EMAIL` is available. Invalid fields render server-side errors and `aria-invalid="true"`. A privacy notice is included. No irreversible model or database change was made.

The visual pass added an error summary with `role="alert"`, visible required notation, and a focused two-column desktop contact layout that collapses to one column on mobile.

Spam protection was not added because no existing spam-protection service or shared form protection was identified for safe reuse during this isolated phase.

## Tests Added

Regression coverage was added for:

- Every rebuild route returning successfully.
- Correct rebuild template usage.
- English document language.
- Correct rebuild navigation links and exclusion of legacy nav items from rebuild navigation.
- Required home section headings.
- Absence of unsupported proof content on the rebuild homepage.
- Contact form field rendering.
- Contact form server-side validation.
- Contact form success behavior using the existing email channel.
- Rebuild CSS isolation.
- Rebuild JavaScript isolation.
- Skip link, main landmark, mobile navigation controls, and current-page navigation state.
- Existing routes continuing to resolve.
- All six live tools continuing to resolve with `tools.css`.
- Rebuild routes remaining outside production sitemaps.
- SEO, knowledge, robots, health, and legacy redirect coverage already present in the suite.

## Test Results

Commands run:

- `.\.venv\Scripts\python.exe manage.py check`
- `.\.venv\Scripts\python.exe manage.py test pi_development.web`

Results:

- Django system check passed with no issues.
- `pi_development.web` test suite passed: 64 tests.

## Visual System

See `docs/reconstruction-audit/rebuild-visual-system.md`.

Implemented visual direction:

- Concept: structured intelligence.
- Scoped color tokens under `.pi-site`.
- System font typography with display, section, body, label, and mono technical roles.
- Responsive 12/8/4 column layout.
- Rebuild-only components for header, mobile navigation, page hero, section intro, section numbers, capability columns, process sequence, technical lists, editorial empty state, contact panel, and system diagrams.
- Minimal motion with reduced-motion support.

Asset sizes from source files:

- `static/web/rebuild/site.css`: 19,989 bytes.
- `static/web/rebuild/site.js`: 1,534 bytes.

No Playwright, Puppeteer, or Selenium dependency exists in the repository, so browser visual smoke tests were not added as test dependencies in this phase. A Browser plugin smoke pass was attempted against a local Django server, but `manage.py runserver 127.0.0.1:8123 --noreload` failed in this environment with a venv launcher error before a page could be loaded. No environment or venv repair was performed.

## Copy Deviations

The supplied page copy was implemented without intentional marketing expansion. Additional functional form support text was added for contact usability, privacy notice, validation, and email handoff behavior. The visual pass added short structural labels in the hero and Ad Products diagrams plus the honest editorial empty state required for Insights.

The insights article listing was intentionally left empty because no safe English article reuse was available without changing the existing content system or inventing articles.

## Technical Assumptions

- `/rebuild/` remains a preview and foundation environment, not the approved production public architecture.
- Existing production sitemap and canonical behavior must remain unchanged until the route map is approved.
- Email notification through `CONTACT_EMAIL` is acceptable as safe contact infrastructure reuse.
- Persistent lead storage requires a future owner decision because adding durable storage would require model and migration decisions.

## Items Deferred

- Production homepage replacement.
- Moving or renaming any existing route.
- `/apps/` route or tool relocation.
- English article migration or editorial publishing workflow.
- Persistent lead storage.
- Spam protection beyond existing infrastructure.
- Production sitemap inclusion for rebuild routes.
- Canonical URLs for future top-level institutional routes.
- Deployment.

## Preservation Confirmation

No existing route, tool, page, slug, stylesheet, JavaScript file, media asset, model, migration, integration, deployment configuration, sitemap inclusion, robots rule, canonical behavior, noindex behavior, or legacy redirect was intentionally deleted, moved, renamed, noindexed, redirected, or replaced in this phase.
