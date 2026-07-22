# Open Questions

These questions require repository owner or production operator input. They should be answered before reconstruction, deletion, route migration, or deployment changes.

## Owner Decisions

- Which current corporate routes must remain primary navigation items after reconstruction?
- Should tools remain under `/tools/`, or should `/apps/` be introduced with redirects?
- Should `/blog/` remain the article route, or should articles eventually move under `/insights/`?
- Should SEO landing pages remain top-level slugs such as `/herramientas-adtech/`?
- Should Labs placeholders remain public, hidden from nav, or rewritten as internal roadmap content?
- Should Work/portfolio items remain public, become case studies, or move to a legacy archive?
- Should older templates and CSS be preserved only in Git or kept available through routed pages?

## Operational Status Unknowns

- Which production URLs currently receive traffic from search, ads, or external links?
- Which tool pages are actively used by users?
- Are PageSpeed and OpenAI integrations configured in production?
- Is Google Analytics currently active in production?
- Is Google Search Console verification active and owned?
- Are there production logs showing 404s for legacy or SEO slugs?
- Is `/admin/` intentionally disabled in production?
- Does any production data exist outside this repo?

## Git and Baseline Questions

- The local `git status` command reported a dubious ownership/safe-directory warning. Should the owner approve adding this path to Git safe.directory before future Git operations?
- What exact backup branch name should be used before reconstruction?
- What exact baseline tag name should be used?
- Should the current local `db.sqlite3` be considered meaningful content or only development data?

## Content and SEO Questions

- Should the site use English, Spanish, or a formal multilingual strategy?
- Should `<html lang="en">`, `LANGUAGE_CODE="en-us"`, and `og:locale="es_AR"` be aligned?
- Should mojibake-looking text in source strings be corrected in a separate content/encoding task?
- Should root `robots.txt` remain when the dynamic `/robots.txt` route exists?
- Should a project-local `sitemap_index.xml` be added to remove reliance on Django package template lookup?
- Should `/policies/` be added to the sitemap?
- Should health endpoints include explicit noindex headers or remain infrastructure-only?

## Tool Product Questions

- Should live tool outputs be saved in future, or remain stateless?
- Should tools require authentication in any future version?
- Should Creative Preview Lab continue allowing arbitrary submitted markup in an iframe sandbox?
- Should URL-fetching tools add browser/headless rendering in a future version?
- Should UTM Builder support presets, naming rules, or batch generation?
- Should tools be separated from corporate styling into a stable app shell?

## Infrastructure Questions

- Is Cloud Run plus Firebase Hosting the long-term target architecture?
- Should a real production database be introduced?
- Should media storage move to cloud object storage if uploads are added?
- Should secrets be moved fully to Secret Manager references instead of direct env values?
- Should CI/CD workflows be added under `.github/workflows/`?
- Should dependency updates be handled before or after reconstruction?
- Should production deployment use immutable image tags tied to Git commit SHAs?

## Deletion Approval Questions

No deletion is approved by this audit. Owner approval is required before removing:

- Legacy redirects.
- Older templates.
- Older CSS files.
- Unlinked media assets.
- Admin static assets.
- Duplicate-looking content objects in `views.py`.
- `Servicio` model or migration.
- Root `robots.txt`.
- Any SEO page, knowledge article, tool, route, or sitemap entry.
