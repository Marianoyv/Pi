# Deploy De Produccion En Cloud Run

## Arquitectura final

- El contenedor sirve Django y los archivos estaticos con WhiteNoise.
- Cloud Run corre con `pi_development.settings.production`.
- Firebase Hosting solo reescribe trafico hacia Cloud Run.
- No se usa `GOOGLE_APPLICATION_CREDENTIALS`.
- Si el servicio necesita acceder a APIs de Google en el futuro, debe hacerlo con ADC de la service account de Cloud Run.

## Variables obligatorias

- `SITE_URL`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `SECRET_KEY_SECRET_NAME`: nombre del recurso de Secret Manager que se montara como `SECRET_KEY`.

## Variables opcionales

- `CONTACT_EMAIL`
- `CONTACT_PHONE`
- `CONTACT_PHONE_WA`
- `CONTACT_LOCATION`
- `TOOLS_HTTP_TIMEOUT`
- `OPENAI_API_BASE`
- `OPENAI_AUDITOR_MODEL`
- `OPENAI_API_KEY_SECRET_NAME`: obligatorio cuando se configura `OPENAI_AUDITOR_MODEL`.
- `PAGESPEED_API_KEY_SECRET_NAME`: usar solo si PageSpeed necesita una clave.
- `ENABLE_REMOTE_URL_TOOLS`: `false` por defecto en produccion; habilitar solo despues del hardening de red.
- `ENABLE_ADMIN`
- `LOG_LEVEL`
- `SECURE_SSL_REDIRECT`
- `SESSION_COOKIE_SECURE`
- `CSRF_COOKIE_SECURE`
- `SECURE_HSTS_SECONDS`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `SECURE_HSTS_PRELOAD`
- `CLOUD_RUN_SERVICE_ACCOUNT`

`SECRET_KEY`, `OPENAI_API_KEY` y `PAGESPEED_API_KEY` no son entradas validas del deploy. El script rechaza esas variables aunque esten vacias para impedir que un secreto llegue a `--update-env-vars`.

Los nombres de ejemplo deben ser placeholders, por ejemplo:

```dotenv
SECRET_KEY_SECRET_NAME=your-django-secret
OPENAI_API_KEY_SECRET_NAME=your-openai-secret
PAGESPEED_API_KEY_SECRET_NAME=your-pagespeed-secret
```

Nunca escribas payloads de secretos en el repositorio ni en argumentos de comandos.

## Preflight sin build ni deploy

```bash
ENV_FILE=.env.prod ./deploy.sh --validate-only
```

Este modo valida la configuracion y termina antes de comprobar `gcloud`, iniciar Cloud Build o modificar Cloud Run.

## Deploy

Con variables exportadas:

```bash
./deploy.sh
```

Con archivo local:

```bash
ENV_FILE=.env.prod ./deploy.sh
```

`deploy.sh` construye la imagen con Cloud Build y despliega a Cloud Run. No sube estaticos por separado ni usa helpers locales.

## Logs

```bash
gcloud run services logs read pi-development --region us-central1 --project pidevelopment --limit=100
```

## Firebase Hosting

No hace falta correr `firebase deploy --only hosting` en cada release del backend.
Solo hace falta si cambias `firebase.json` o la configuracion del proyecto Firebase.
