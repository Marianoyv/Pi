# Styles and Assets Inventory

Static source root: `static/web/`.

Production static files are collected into `staticfiles/` during build and served by WhiteNoise from the container image. The `staticfiles/` directory appears generated and should not be treated as the source of truth for edits.

## Global Visual System

Primary file: `static/web/css/base.css`.

Important tokens:

- Color RGB tokens: `--rgb-bg`, `--rgb-surface`, `--rgb-border`, `--rgb-text`, `--rgb-primary`, `--rgb-accent`, etc.
- Color hex tokens: `--color-bg`, `--color-surface`, `--color-text`, `--color-primary`, `--color-secondary`, `--color-accent`, etc.
- Surface tokens: `--surface-overlay`, `--surface-panel`, `--surface-panel-strong`, `--surface-panel-soft`.
- Border/shadow tokens: `--border-subtle`, `--border-strong`, `--shadow-soft`, `--shadow-dark`, `--shadow-focus`.
- Radius tokens: `--radius-lg`, `--radius-md`.
- Layout tokens: `--nav-height`, `--section-space`, `--section-space-tight`.
- Spacing tokens: `--space-4` through `--space-80`.
- Typography tokens: `--font-body`, `--font-body-lg`, `--font-small`, `--font-label`, `--font-button`, `--font-h1` through `--font-h4`.
- Measures: `--measure-text`, `--measure-wide`.

Global patterns:

- Dark color scheme.
- Inter font from Google Fonts.
- Bootstrap 5.3.3 CSS/JS from CDN.
- Font Awesome kit from CDN.
- Pill-shaped `.button-link` pattern.
- Shared `.page-shell`, `.section-header`, `.section-actions`.
- Mobile responsive token override at `max-width: 769px`.

Classification: `CORE_PUBLIC`.

## CSS Files

| File | Main use | Active status | Label |
|---|---|---|---|
| `base.css` | global tokens, reset, typography, buttons, page shell | active | `CORE_PUBLIC` |
| `navbar.css` | top navigation, mobile menu, progress bar | active | `CORE_PUBLIC` |
| `footer.css` | footer layout and links | active | `CORE_PUBLIC` |
| `company.css` | current company home and generic company pages | active | `CORE_PUBLIC` |
| `tools.css` | tools index, live tools, result cards, editorial blocks, related content | active and central | `EXISTING_APP` |
| `content_page.css` | approach, SEO landing, knowledge article content layouts | active | `CORE_PUBLIC` |
| `blog.css` | blog/knowledge listing | active | `CORE_PUBLIC` |
| `portfolio.css` | work page and older portfolio presentation | active/preserved | `CONTENT_ASSET` |
| `services_overview.css` | systems page | active | `CORE_PUBLIC` |
| `policies.css` | policies page | active | `CONTENT_ASSET` |
| `contacto.css` | contact and older contact sections | active/preserved | `CORE_PUBLIC` |
| `hero.css` | older hero template | preserved | `LEGACY_PRESERVE` |
| `servicios.css` | older services template | preserved | `LEGACY_PRESERVE` |
| `proceso.css` | older process template | preserved | `LEGACY_PRESERVE` |
| `herramientas.css` | older tools template | preserved | `LEGACY_PRESERVE` |
| `nosotros.css` | older about template | preserved | `LEGACY_PRESERVE` |

## JavaScript

File: `static/web/js/main.js`.

Behaviors:

- Adds `js-ready` class to document root.
- Optional Vanta Globe initialization for element `#vanta-hero` if `window.VANTA.GLOBE` exists.
- Navbar scroll state, mobile menu toggle, progress bar, hero fade/social effects.
- Older process step reveal animation for `.proceso-step`.
- Live tool submit handling for `[data-analyze-form]`, disabling submit button and setting loading text.
- Copy buttons for `[data-copy-button]` with Clipboard API fallback message.
- Global `handleContact(e)` for contact form WhatsApp message opening and optional `gtag` event.

Dependencies:

- Browser DOM APIs.
- Optional `window.VANTA`.
- Optional `gtag`.
- Clipboard API.
- Contact phone from `body[data-whatsapp-phone]`.

Classification: `CORE_PUBLIC` and `EXISTING_APP` shared dependency.

## Images and Videos

| Asset | Use / notes | Label |
|---|---|---|
| `pi.png` | apple touch icon, default Open Graph image, Organization logo | `CONTENT_ASSET` |
| `piw.png` | navbar logo | `CONTENT_ASSET` |
| `pi.ico` | favicon target | `CONTENT_ASSET` |
| `ico2.ico` | preserved icon asset; current active use not confirmed | `UNKNOWN_REQUIRES_REVIEW` |
| `1.png` to `5.png` | portfolio posters/screenshots | `CONTENT_ASSET` |
| `arcade.mp4`, `arcade1.png`, `arcade2.png`, `arcade3.png` | Arcade World work media | `CONTENT_ASSET` |
| `blogie1.png`, `blogie2.png`, `2.png` | Blog Int Emocional work media | `CONTENT_ASSET` |
| `indices.png`, `indice1.png`, `indice2.png`, `indice3.png` | Indices Argentinos work media | `CONTENT_ASSET` |
| `recetas.png` | Recetas del Sapi work media | `CONTENT_ASSET` |
| `juno.mp4`, `5.png` | Juno Metales work media | `CONTENT_ASSET` |
| `sistemvesta.mp4`, `sistemvesta1.png`, `4.png` | System Vesta work media | `CONTENT_ASSET` |

## Admin Static Assets

The repository includes `static/admin/` with Django admin CSS, JS, images, and vendor assets. These appear to be collected/copied admin static files.

Preservation note: do not remove unless the deployment/static collection strategy is explicitly revised. Admin availability is controlled by `ENABLE_ADMIN`, but static files may still be needed for local or future admin operation.

Classification: `INTERNAL`.

## Duplicate or Legacy-Looking Style Systems

There are two visible design eras:

- Current company/product/tool system: `base.css`, `navbar.css`, `footer.css`, `company.css`, `tools.css`, `content_page.css`, `blog.css`.
- Older sectional system: `hero.css`, `servicios.css`, `portfolio.css`, `proceso.css`, `herramientas.css`, `nosotros.css`, `contacto.css`, plus older templates.

This is not deletion evidence. Older templates and styles may support fallback pages, historical reconstruction context, or future route preservation.

Classification: `POSSIBLE_DUPLICATE` for review only.

## Visual Fragility Notes

- `tools.css` is large and shared by the most operational pages; breaking it affects all live tools, result states, copy/export UI, examples, related links, and SEO content blocks.
- `base.css` defines global tokens used by all page-level styles.
- `main.js` includes both current and older behaviors; removing old selectors without review may break legacy templates.
- Bootstrap and Font Awesome are CDN dependencies; a network or CSP change can affect layout/icons.
- Some media files are large videos; backup and deployment artifact planning should include them explicitly.
