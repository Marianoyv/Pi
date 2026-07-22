# Preservation Plan for Future Reconstruction

This is a proposal only. Do not implement these route, navigation, or structure changes without a separate owner-approved reconstruction task.

## Separation Strategy

| Area | Proposed future role | Current routes to preserve | Notes |
|---|---|---|---|
| New institutional website | Primary corporate experience | `/`, `/solutions/`, `/products/`, `/adtech/`, `/labs/`, `/insights/`, `/about/`, `/contact/` | Can be redesigned later, but route names and redirects need a compatibility plan |
| Existing tools and applications | Independent operational app suite | `/tools/`, `/tools/<slug>/` | Keep direct access even if removed from primary nav; preserve sitemap unless SEO decision changes |
| Editorial content / insights | Technical content layer | `/insights/`, `/blog/`, `/blog/<slug>/` | Can be reframed as Insights; keep article slugs and related links |
| Research / future content | New content family if needed | potential `/research/` | No current route found; add only after collision review with SEO catch-all |
| SEO landing pages | Search/content acquisition layer | `/<seo-slug>/` | Preserve current top-level slugs or map explicit redirects |
| Legacy pages | Compatibility archive/redirect layer | `/services/`, `/services/<slug>/`, `/portfolio/`, `/process/`, `/resources/` | Preserve existing 301 behavior unless owner approves change |
| Internal/admin functionality | Operational/admin layer | `/admin/`, `/health`, `/healthz/`, sitemaps, robots | Keep isolated from public navigation |

## Recommended Future URL Model

Preferred conceptual structure:

- Corporate website: `/`
- Tools and applications: keep `/tools/` and `/tools/<slug>/`; consider `/apps/` only if redirects and sitemap migration are planned.
- Insights/editorial: keep `/insights/`, `/blog/`, and `/blog/<slug>/`; consider future `/insights/<slug>/` only with redirects from existing blog slugs.
- Research: add `/research/` only when actual research content exists.
- Legacy content: preserve current redirects or create a controlled archive with explicit owner approval.

Do not move live tools just to simplify navigation. A tool can be hidden from the main navbar while remaining routed, linked from relevant pages, and indexed.

## Navigation Preservation Rules

- Hiding from primary navigation is safer than removing routes.
- Footer can preserve utility access even when the main nav becomes more corporate.
- If Products becomes a pure corporate product page, keep a clear path to `/tools/`.
- If Insights becomes the editorial hub, keep `/blog/` and article routes live or redirect them deliberately.
- Never remove a top-level SEO slug without a redirect and owner approval.

## Pre-Reconstruction Git Requirements

Before any future reconstruction:

- Create a named backup branch, for example `backup/pre-reconstruction-2026-07-12`.
- Create a tagged baseline, for example `baseline/pre-reconstruction-2026-07-12`.
- Resolve the current Git safe-directory warning before relying on local Git status/branches.
- Do not create branches, tags, commits, or pushes as part of this audit.

## Backup Requirements

Database:

- Local: copy `db.sqlite3` before migrations or model changes.
- Production: currently dummy DB/stateless; if a real production DB is introduced later, take a provider-level backup/snapshot before reconstruction.
- Admin/user/session data: confirm whether any real production data exists before enabling admin or replacing storage.

Media/static:

- Archive `static/web/` source assets.
- Archive any `media/` directory if present in the future.
- Preserve large videos and portfolio screenshots.
- Treat `staticfiles/` as generated, but optionally archive the current deployed artifact for rollback.

Environment/deployment:

- Record environment variable names and secret references, not secret values.
- Export Cloud Run service configuration before deployment changes.
- Keep current `firebase.json`, `.firebaserc`, `Dockerfile`, and `deploy.sh` in the baseline.

## Rollback Plan

Minimum rollback package:

- Baseline Git tag/branch.
- Static/media archive.
- Database backup if a real DB is involved.
- Cloud Run service configuration export.
- Last known working container image URI.
- Firebase Hosting configuration baseline.

Rollback sequence:

1. Re-deploy the baseline container image or rebuild from the baseline tag.
2. Restore Firebase Hosting rewrite if changed.
3. Restore database/media backups if schema or storage changed.
4. Verify `/health`, `/`, `/tools/`, representative tool pages, `/blog/`, one SEO page, `/robots.txt`, and `/sitemap.xml`.

## What Can Be Hidden From Navigation Later

These may be hidden from primary nav if direct routes and relevant footer/context links remain:

- `/tools/` and tool pages, if Products or AdTech still links to them clearly.
- `/work/`.
- `/approach/`.
- `/systems/`.
- `/blog/`, if `/insights/` becomes the visible editorial entry and links to articles.
- `/policies/`, as footer-only.

This does not authorize route removal or noindex.

## What Requires Owner Approval

- Deleting any route, template, stylesheet, JavaScript file, media asset, migration, model, deployment file, or content object.
- Renaming any URL slug.
- Moving `/tools/<slug>/` to a new path.
- Changing sitemap inclusion.
- Adding noindex or canonical changes.
- Removing legacy redirects.
- Enabling admin in production.
- Introducing a production database.
- Replacing Firebase Hosting / Cloud Run architecture.

## Immediate Preservation Priority

1. Preserve live tools and `/tools/<slug>/` routes.
2. Preserve SEO landing slugs and catch-all behavior.
3. Preserve knowledge article slugs.
4. Preserve nav/footer route names or redirect them explicitly.
5. Preserve static assets used by portfolio, favicon, OG image, and templates.
6. Preserve deployment files until a new deployment architecture is approved.
