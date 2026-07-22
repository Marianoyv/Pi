# Rebuild Visual System

## Scope

This document covers only the isolated `/rebuild/` institutional website. It does not authorize changes to the production homepage, production templates, tools, SEO pages, articles, redirects, sitemaps, robots, models, migrations, integrations, or deployment configuration.

## Visual Concept

Concept: structured intelligence.

The rebuild should communicate precision, technical rigor, independent thinking, restraint, systems thinking, applied research, and serious ambition. The implementation avoids generic startup imagery, agency-style feature cards, AI cliches, cyberpunk styling, fake dashboards, product mockups, testimonials, metrics, client logos, and decorative proof.

## Design Principles

- Hierarchy before decoration: pages rely on labels, H1s, H2s, section numbers, lists, and links.
- One idea per section: each section has a clear entry, body, and exit.
- Controlled density: spacing is generous but compact enough to avoid cinematic emptiness.
- Visible structure: selected sections use fine rules, numbers, grid alignment, and minimal system diagrams.
- Functional motion: motion is limited to small state transitions and subtle reveal.

## Color Tokens

Defined in `static/web/rebuild/site.css` under `.pi-site`:

- `--pi-bg`
- `--pi-bg-subtle`
- `--pi-surface`
- `--pi-surface-strong`
- `--pi-text`
- `--pi-text-muted`
- `--pi-border`
- `--pi-border-strong`
- `--pi-accent`
- `--pi-accent-contrast`
- `--pi-focus`
- `--pi-error`

Temporary accent: `--pi-accent: #8f4f2a`. This is a restrained warm technical accent and remains subject to owner approval because no final institutional color system has been approved.

## Typography

The rebuild uses performance-safe system fonts only:

- Primary sans: Arial, Helvetica, sans-serif.
- Optional technical mono: SFMono-Regular, Consolas, Liberation Mono, monospace.

Type roles:

- Display: H1 via `.pi-hero-title`.
- Section title: `.pi-section-header h2`.
- Body large: `.pi-hero-text`.
- Body: section and paragraph text.
- Small label: `.pi-site-eyebrow`, `.pi-section-label`.
- Technical/mono label: section numbers, item numbers, diagram labels, mobile menu label.

Sizing uses `clamp()` for major display roles. Body copy is constrained to approximately 62-72 characters through measure tokens.

## Layout Grid

The rebuild uses a scoped responsive layout:

- Max shell: `min(1240px, calc(100% - 48px))`.
- Desktop grid: 12 columns.
- Tablet grid: 8 columns.
- Mobile grid: 4 columns.
- Minimum mobile horizontal padding: 20px.
- Editorial measure: `--pi-measure` and `--pi-measure-narrow`.

Sections use `.pi-section-layout`, `.pi-section-meta`, and `.pi-section-body` for consistent alignment without making every page visually identical.

## Spacing Scale

Spacing tokens:

- `--pi-space-1: 4px`
- `--pi-space-2: 8px`
- `--pi-space-3: 12px`
- `--pi-space-4: 16px`
- `--pi-space-5: 24px`
- `--pi-space-6: 32px`
- `--pi-space-7: 48px`
- `--pi-space-8: 64px`
- `--pi-space-9: 88px`
- `--pi-space-10: 112px`

These tokens keep sections substantial without forcing excessive scroll.

## Components

Rebuild-only components/classes now include:

- `SiteHeader`: `.pi-site-header`, `.pi-site-header-inner`.
- `MobileNavigation`: `.pi-menu-toggle`, `.pi-nav`, `.pi-site-menu-open`.
- `SiteFooter`: `.pi-footer`, `.pi-footer-links`.
- `PageHero`: `.pi-page-hero`, `.pi-page-hero-grid`.
- `SectionIntro`: `.pi-section-header`.
- `SectionNumber`: `.pi-section-meta`, `.pi-item-number`.
- `TextLink`: `.pi-text-link`.
- `PrimaryAction`: `.pi-button-primary`.
- `SecondaryAction`: `.pi-button-secondary`.
- `CapabilityColumns`: `.pi-capability-columns`, `.pi-capability-item`.
- `ProcessSequence`: `.pi-process-sequence`.
- `TechnicalList`: `.pi-technical-list`.
- `ResearchFormats`: interior principle grids on Research.
- `EditorialEmptyState`: `.pi-editorial-empty`.
- `ContactPanel`: `.pi-contact-panel`, `.pi-form-panel`.
- `SystemDiagram`: `.pi-system-diagram`, `.pi-ad-diagram`.
- `Divider`: section borders and fine rules.
- `Container`: `.pi-site-shell`.

No generic card component was introduced.

## Motion Rules

Allowed motion:

- Header border/background state on scroll and focus.
- Mobile menu open/close display state.
- Button and link hover/focus states.
- Small section reveal.

Durations are 160-220ms. Motion uses opacity, transform, and color/border changes only. There is no scroll-jacking, parallax, cursor replacement, loading intro, looping animation, WebGL, canvas, or animation library.

`prefers-reduced-motion: reduce` is respected.

## Accessibility Decisions

Implemented:

- Skip-to-content link targeting `#main-content`.
- Main landmark with focus target.
- Header navigation landmark.
- Mobile menu button with `aria-controls` and `aria-expanded`.
- Active navigation link with `aria-current="page"`.
- Escape closes mobile navigation.
- Body scroll is locked only while the mobile menu is open.
- Visible `:focus-visible` styles.
- Clear button and link states.
- Contact labels appear above controls.
- Required field notation is visible.
- Server-side form validation remains active.
- Error summary uses `role="alert"`.
- Field errors render near fields.
- Success message uses `role="status"`.
- Reduced motion support.

Manual checks still recommended:

- Screen reader pass on the mobile navigation.
- Keyboard pass on all responsive breakpoints.
- Contrast verification with final approved accent.
- Visual overflow review on real devices.

## Performance Decisions

- No frontend framework added.
- No animation library added.
- No icon library added.
- No background video added.
- No raster hero image added.
- No third-party scripts added.
- Rebuild JavaScript is limited to mobile navigation and header state.
- Core content remains server-rendered and works without JavaScript; on no-JS mobile, the navigation remains visible instead of hidden.

Asset sizes from source files:

- `static/web/rebuild/site.css`: 19,989 bytes.
- `static/web/rebuild/site.js`: 1,534 bytes.

Both are unminified source sizes. Gzip sizes were not measured in this phase.

## Responsive Behavior

CSS breakpoints:

- Desktop default.
- `max-width: 1024px`: tablet grid, mobile navigation behavior, stacked complex systems.
- `max-width: 640px`: mobile grid, reduced section spacing, single-column form and diagrams.
- `max-width: 360px`: tighter shell and wordmark wrapping.

Target widths to manually verify:

- 320px
- 375px
- 430px
- 768px
- 1024px
- 1280px
- 1440px

Automated browser checks were not added because no Playwright, Puppeteer, or Selenium dependency exists in the repository, and this phase does not add large browser-testing dependencies. A Browser plugin smoke pass was attempted against a local Django server, but `manage.py runserver 127.0.0.1:8123 --noreload` failed in this environment with a venv launcher error before a page could be loaded. No environment or venv repair was performed.

## JavaScript

File: `static/web/rebuild/site.js`.

Responsibilities:

- Adds `.pi-site-js` enhancement class.
- Toggles accessible mobile navigation.
- Updates `aria-expanded`.
- Closes menu on Escape.
- Closes menu after nav link clicks.
- Adds a subtle header scrolled state.

It does not implement client-side routing, analytics sending, SPA behavior, heavy scroll observers, custom cursors, canvas, WebGL, or external dependencies.

## Analytics Readiness

Semantic `data-pi-event` attributes were added for future analytics mapping only. No events are sent.

Proposed future mapping:

- `nav_logo`: logo click.
- `nav_click`: primary navigation click.
- `primary_cta`: primary CTA click.
- `secondary_cta`: secondary CTA click.
- `capability_link`: capabilities link click.
- `ad_products_link`: Ad Products link click.
- `research_link`: research link click.
- `text_link`: supporting text link click.
- `contact_form`: contact form start or view.
- `contact_submit`: contact submit attempt.

Any event sending should reuse the existing analytics architecture only after approval.

## Deviations

- Browser automation was not run because no browser automation dependency exists and adding one would expand the phase beyond the requested lightweight visual pass.
- The temporary Pi accent is not final brand color.
- The hero diagram uses HTML/CSS rather than SVG because it can be scoped, responsive, accessible, and lightweight without adding assets.

## Preservation Confirmation

This visual system is loaded only by the rebuild base template. Existing production templates, `tools.css`, `main.js`, sitemap generation, robots, canonicals, routes, content slugs, models, migrations, integrations, and deployment files are intentionally untouched by this visual layer.
