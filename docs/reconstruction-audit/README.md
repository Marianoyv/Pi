# Reconstruction Audit

Date: 2026-07-12

This directory is a preservation-first inventory for the existing Pi Development repository before any public website reconstruction. It documents the current system without authorizing deletion, renaming, route changes, SEO changes, model changes, deployment changes, or code rewrites.

## Safety Rules Applied

- Production code was not edited.
- Routes, templates, styles, static assets, models, migrations, deployment files, SEO behavior, and Git history are preserved.
- Secrets and environment variable values are not copied into this audit.
- Environment variables are listed by name only.
- Unlinked, duplicate-looking, legacy, or redirected items are not treated as obsolete.
- Any future removal requires repository owner approval.

## Repository Overview

- Framework: Django 5.2 from `requirements.txt`.
- Runtime: Python app served by Gunicorn.
- Django project: `pi_development`.
- Django app: `pi_development.web`.
- Public entrypoint: `pi_development.web.urls`.
- Local database: SQLite via `pi_development/settings/local.py`.
- Production database: dummy backend in `pi_development/settings/production.py`, with signed-cookie sessions.
- Static serving: WhiteNoise in production, collected into the container image.
- Hosting path: Firebase Hosting rewrites all traffic to Cloud Run service `pi-development` in `us-central1`.
- Current public site: company pages, product/tool suite, SEO landing pages, knowledge articles, work/portfolio content, policies, robots, and sitemaps.
- Admin: Django admin can be inserted at `/admin/` when `ENABLE_ADMIN` is true.
- Model inventory: `Servicio` with `nombre`, `descripcion`, and `precio`.

## Main Source Areas

- URL routing: `pi_development/urls.py`, `pi_development/web/urls.py`.
- Views and page wiring: `pi_development/web/views.py`.
- Tool catalog: `pi_development/web/tool_catalog.py`.
- Tool forms: `pi_development/web/forms.py`.
- Tool service logic: `pi_development/web/services/tools/`.
- Company page data: `pi_development/web/company_pages.py`.
- SEO landing page data: `pi_development/web/seo_pages.py`.
- Knowledge article data: `pi_development/web/knowledge_pages.py`.
- Topic clusters: `pi_development/web/topic_clusters.py`.
- Sitemap logic: `pi_development/web/sitemaps.py`.
- Templates: `pi_development/web/templates/web/`.
- Static assets: `static/web/`.
- Deployment: `Dockerfile`, `deploy.sh`, `firebase.json`, `.firebaserc`, `DEPLOY_PRODUCTION.md`.

## Classification Legend

- `CORE_PUBLIC`: primary public website route or content.
- `EXISTING_APP`: operational tool, app-like feature, or service surface.
- `CONTENT_ASSET`: article, SEO content, metadata, portfolio item, image, video, or static content object.
- `INTERNAL`: admin, health, deployment, or infrastructure-only behavior.
- `EXPERIMENTAL`: lab placeholder, future product concept, or not-yet-productized feature.
- `LEGACY_PRESERVE`: legacy route/template/content that must remain preserved.
- `POSSIBLE_DUPLICATE`: duplicate-looking system that must not be deleted without review.
- `REMOVAL_CANDIDATE_REVIEW_REQUIRED`: could be hidden or reviewed, but deletion is not authorized.
- `UNKNOWN_REQUIRES_REVIEW`: insufficient evidence to classify safely.

## Validation Status

- `.\.venv\Scripts\python.exe manage.py check` was run during audit exploration and returned no Django system check issues.
- Git status could not be read because Git reported this repository as a dubious ownership/safe-directory case for the current user. This audit does not change global Git config.

## Audit Files

- `routes.md`: complete route and generated-page inventory.
- `tools-and-apps.md`: live tool inventory and dependencies.
- `content.md`: static content, editorial content, topic clusters, portfolio, metadata, and media.
- `templates-and-components.md`: template architecture and reusable components.
- `styles-and-assets.md`: CSS, JavaScript, image, video, icon, and visual-system inventory.
- `integrations.md`: hosting, external services, env vars by name, logging, storage, and deployment.
- `seo.md`: robots, sitemap, canonical, metadata, schema, redirects, and indexation behavior.
- `dependency-map.md`: shared dependencies across pages, tools, content, and infrastructure.
- `preservation-plan.md`: future separation plan and pre-reconstruction backup requirements.
- `open-questions.md`: owner decisions and unresolved operational questions.
