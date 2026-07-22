# Infrastructure and Integrations Inventory

This file lists external services, deployment resources, storage behavior, logging, and environment variables by name only. No secret values are included.

## Runtime and Hosting

| Area | Current implementation | Files | Label |
|---|---|---|---|
| Django runtime | Django 5.2 app with `pi_development.settings.production` in WSGI/ASGI | `requirements.txt`, `wsgi.py`, `asgi.py` | `INTERNAL` |
| Web server | Gunicorn bound to `${PORT:-8080}` | `Dockerfile` | `INTERNAL` |
| Container | `python:3.11-slim`, installs requirements, copies app/static, runs collectstatic, starts Gunicorn | `Dockerfile` | `INTERNAL` |
| Static serving | WhiteNoise middleware in production | `production.py`, `Dockerfile` | `INTERNAL` |
| Firebase Hosting | rewrites all traffic to Cloud Run service `pi-development` in `us-central1` | `firebase.json`, `.firebaserc` | `INTERNAL` |
| Google Cloud Run | managed service target, unauthenticated deployment through `deploy.sh` | `deploy.sh`, `DEPLOY_PRODUCTION.md` | `INTERNAL` |
| Cloud Build | image build through `gcloud builds submit` | `deploy.sh` | `INTERNAL` |

## Database and Storage

| Area | Current implementation | Notes | Label |
|---|---|---|---|
| Local DB | SQLite database `db.sqlite3` | Used by `local.py`; contains local state if migrated | `INTERNAL` |
| Production DB | Django dummy database backend | `production.py` states Cloud Run remains stateless until a real production DB is introduced | `INTERNAL` |
| Sessions local/base | DB-backed sessions in base settings | Production overrides this | `INTERNAL` |
| Sessions production | Signed-cookie sessions | Avoids production DB dependency | `INTERNAL` |
| Message storage production | Cookie storage | Avoids DB dependency | `INTERNAL` |
| Default file storage | local filesystem storage | `MEDIA_ROOT = BASE_DIR / "media"`; no active media upload model found | `INTERNAL` |
| Static source | `static/web` via `STATICFILES_DIRS` | Source assets | `CONTENT_ASSET` |
| Static output | `staticfiles` via `STATIC_ROOT` | Build artifact / generated static | `INTERNAL` |

## External APIs and Services

| Service | Use | Files | Required? | Failure behavior | Label |
|---|---|---|---|---|---|
| PageSpeed Insights | Optional performance/SEO enrichment for AI Auditor | `pagespeed.py`, `ai_auditor.py` | optional | Returns unavailable/invalid/empty status; tool continues with HTTP/HTML data | `EXISTING_APP` |
| OpenAI-compatible Chat Completions | Optional AI summary for AI Auditor | `openai_summary.py`, `ai_auditor.py` | optional | Returns unconfigured/error status; tool continues without AI summary | `EXISTING_APP` |
| Public target URLs | URL-based tools fetch external pages | `http_snapshot.py`, `adtech_debug.py`, `landing_snapshot.py`, `ai_auditor.py` | per tool execution | Returns partial/unavailable results on request errors | `EXISTING_APP` |
| Google Analytics / gtag | Optional page analytics and contact event | `base.html`, `main.js` | optional | Script omitted when ID absent | `INTERNAL` |
| Google Search Console verification | Optional meta verification tag | `base.html` | optional | Tag omitted when value absent | `INTERNAL` |
| WhatsApp | Contact message link | `main.js`, footer/contact templates | optional public UX | Opens `wa.me` with configured phone | `CORE_PUBLIC` |
| GitHub / LinkedIn / Instagram | Social links | footer and older hero | public links | outbound only | `CONTENT_ASSET` |
| Google Fonts | Inter font | `base.html` | external asset | fallback fonts if unavailable | `CORE_PUBLIC` |
| Bootstrap CDN | CSS/JS framework | `base.html` | external asset | layout/JS behavior may degrade if unavailable | `CORE_PUBLIC` |
| Font Awesome kit | icons | `base.html`, nav/footer/older hero | external asset | icons may disappear if unavailable | `CORE_PUBLIC` |

## Forms and Spam Protection

- No backend contact form submission endpoint was found.
- `main.js` defines `handleContact(e)` to validate name/email/project fields client-side and open WhatsApp.
- Tool forms use Django forms and CSRF middleware.
- No CAPTCHA or spam protection integration was found.

Classification: `UNKNOWN_REQUIRES_REVIEW` for future contact-form strategy.

## Authentication and Admin

- `django.contrib.auth` and `django.contrib.admin` are installed.
- Admin route is inserted only when `settings.ENABLE_ADMIN` is true.
- Registered model: `Servicio`.
- Production uses dummy database and signed-cookie sessions, so production admin is not operational unless production data storage is changed.

Classification: `INTERNAL`.

## Logging and Monitoring

- Django logging is configured to console through `LOGGING` in `base.py`.
- `LOG_LEVEL` controls root and Django logger levels.
- `django.request` logs errors.
- Cloud Run logs can be read through `gcloud run services logs read ...` as documented in `DEPLOY_PRODUCTION.md`.
- No explicit APM, error reporting, uptime monitor, or custom metrics integration was found.

Classification: `INTERNAL`.

## CI/CD

- `.github/` directory exists but no workflow file was found during audit inspection.
- Deployment is script-driven through `deploy.sh`.
- Firebase Hosting deploy is only needed when `firebase.json` or Firebase hosting configuration changes.

Classification: `UNKNOWN_REQUIRES_REVIEW`.

## Environment Variable Names

Required in production settings/deploy flow:

- `SECRET_KEY`
- `SITE_URL`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

Deployment/config names:

- `PROJECT_ID`
- `SERVICE_NAME`
- `REGION`
- `IMAGE_REPO`
- `IMAGE_TAG`
- `IMAGE_URI`
- `ENV_FILE`
- `CLOUD_RUN_SERVICE_ACCOUNT`

Optional application names:

- `CONTACT_EMAIL`
- `CONTACT_PHONE`
- `CONTACT_PHONE_WA`
- `CONTACT_LOCATION`
- `TOOLS_HTTP_TIMEOUT`
- `OPENAI_API_BASE`
- `OPENAI_AUDITOR_MODEL`
- `OPENAI_API_KEY`
- `PAGESPEED_API_KEY`
- `PAGESPEED_API_ENDPOINT`
- `GOOGLE_ANALYTICS_ID`
- `GOOGLE_SITE_VERIFICATION`
- `ENABLE_ADMIN`
- `LOG_LEVEL`
- `SECURE_SSL_REDIRECT`
- `SESSION_COOKIE_SECURE`
- `CSRF_COOKIE_SECURE`
- `SECURE_HSTS_SECONDS`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `SECURE_HSTS_PRELOAD`

Secret indirection names supported by deploy script:

- `SECRET_KEY_SECRET_NAME`
- `OPENAI_API_KEY_SECRET_NAME`
- `PAGESPEED_API_KEY_SECRET_NAME`

## Infrastructure Fragility Notes

- Production is intentionally stateless; adding admin, user data, saved tool histories, uploads, or content editing requires a real database/storage plan.
- `deploy.sh` can pass secrets directly as env vars or map them from Secret Manager names. Future docs should prefer secret references.
- Tool execution depends on outbound HTTP access from Cloud Run.
- PageSpeed and OpenAI are optional but should be monitored if they become product-critical.
- Firebase Hosting rewrites all paths to Cloud Run; route preservation lives in Django, not Firebase path rules.
