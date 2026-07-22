#!/usr/bin/env bash

set -euo pipefail

PROJECT_ID="${PROJECT_ID:-pidevelopment}"
SERVICE_NAME="${SERVICE_NAME:-pi-development}"
REGION="${REGION:-us-central1}"
IMAGE_REPO="${IMAGE_REPO:-gcr.io/${PROJECT_ID}/${SERVICE_NAME}}"
IMAGE_TAG="${IMAGE_TAG:-$(date -u +%Y%m%d-%H%M%S)}"
IMAGE_URI="${IMAGE_URI:-${IMAGE_REPO}:${IMAGE_TAG}}"
ENV_FILE="${ENV_FILE:-}"
MODE="${1:-}"

if [[ -n "${MODE}" && "${MODE}" != "--validate-only" ]]; then
  echo "ERROR: argumento no reconocido. Usa --validate-only o ejecuta sin argumentos."
  exit 1
fi

fail() {
  echo "ERROR: $1" >&2
  exit 1
}

validate_secret_name() {
  local variable_name="$1"
  local secret_name="$2"

  if [[ ! "${secret_name}" =~ ^[A-Za-z0-9._/-]+$ ]]; then
    fail "${variable_name} contiene un nombre de recurso no valido"
  fi
}

if [[ -n "${ENV_FILE}" ]]; then
  if [[ ! -f "${ENV_FILE}" ]]; then
    echo "ERROR: no existe ENV_FILE=${ENV_FILE}"
    exit 1
  fi

  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
fi

required_env_vars=(
  "SITE_URL"
  "ALLOWED_HOSTS"
  "CSRF_TRUSTED_ORIGINS"
)

for env_var in "${required_env_vars[@]}"; do
  if [[ -z "${!env_var:-}" ]]; then
    echo "ERROR: falta la variable obligatoria ${env_var}"
    exit 1
  fi
done

if [[ -v SECRET_KEY ]]; then
  fail "SECRET_KEY no puede enviarse como variable plana; elimina esa variable y define SECRET_KEY_SECRET_NAME"
fi

if [[ -z "${SECRET_KEY_SECRET_NAME:-}" ]]; then
  fail "falta la variable obligatoria SECRET_KEY_SECRET_NAME"
fi

validate_secret_name "SECRET_KEY_SECRET_NAME" "${SECRET_KEY_SECRET_NAME}"

if [[ -n "${OPENAI_AUDITOR_MODEL:-}" && -z "${OPENAI_API_KEY_SECRET_NAME:-}" ]]; then
  fail "OPENAI_AUDITOR_MODEL requiere OPENAI_API_KEY_SECRET_NAME"
fi

env_pairs=(
  "SITE_URL=${SITE_URL}"
  "ALLOWED_HOSTS=${ALLOWED_HOSTS}"
  "CSRF_TRUSTED_ORIGINS=${CSRF_TRUSTED_ORIGINS}"
  "LOG_LEVEL=${LOG_LEVEL:-INFO}"
)

optional_env_vars=(
  "CONTACT_EMAIL"
  "CONTACT_PHONE"
  "CONTACT_PHONE_WA"
  "CONTACT_LOCATION"
  "TOOLS_HTTP_TIMEOUT"
  "OPENAI_API_BASE"
  "OPENAI_AUDITOR_MODEL"
  "GOOGLE_ANALYTICS_ID"
  "GOOGLE_SITE_VERIFICATION"
  "ENABLE_REMOTE_URL_TOOLS"
  "ENABLE_ADMIN"
  "SECURE_SSL_REDIRECT"
  "SESSION_COOKIE_SECURE"
  "CSRF_COOKIE_SECURE"
  "SECURE_HSTS_SECONDS"
  "SECURE_HSTS_INCLUDE_SUBDOMAINS"
  "SECURE_HSTS_PRELOAD"
)

for env_var in "${optional_env_vars[@]}"; do
  if [[ -n "${!env_var:-}" ]]; then
    env_pairs+=("${env_var}=${!env_var}")
  fi
done

env_spec="^|^"
for pair in "${env_pairs[@]}"; do
  env_spec+="${pair}|"
done
env_spec="${env_spec%|}"

secret_pairs=("SECRET_KEY=${SECRET_KEY_SECRET_NAME}:latest")

optional_secret_names=(
  "OPENAI_API_KEY"
  "PAGESPEED_API_KEY"
)

for secret_env in "${optional_secret_names[@]}"; do
  secret_name_var="${secret_env}_SECRET_NAME"

  if [[ -v "${secret_env}" ]]; then
    fail "${secret_env} no puede enviarse como variable plana; usa ${secret_name_var}"
  fi

  if [[ -n "${!secret_name_var:-}" ]]; then
    validate_secret_name "${secret_name_var}" "${!secret_name_var}"
    secret_pairs+=("${secret_env}=${!secret_name_var}:latest")
  fi
done

if [[ "${MODE}" == "--validate-only" ]]; then
  echo "OK: preflight valido; los secretos de produccion usan referencias de Secret Manager."
  exit 0
fi

if ! command -v gcloud >/dev/null 2>&1; then
  fail "no se encontro el comando requerido: gcloud"
fi

echo "1. Construyendo imagen con Cloud Build..."
echo "   IMAGE_URI=${IMAGE_URI}"
gcloud builds submit \
  --project "${PROJECT_ID}" \
  --tag "${IMAGE_URI}"

deploy_command=(
  gcloud run deploy "${SERVICE_NAME}"
  --project "${PROJECT_ID}"
  --image "${IMAGE_URI}"
  --platform managed
  --region "${REGION}"
  --allow-unauthenticated
  --update-env-vars "${env_spec}"
)

if [[ -n "${CLOUD_RUN_SERVICE_ACCOUNT:-}" ]]; then
  deploy_command+=(--service-account "${CLOUD_RUN_SERVICE_ACCOUNT}")
fi

if [[ ${#secret_pairs[@]} -gt 0 ]]; then
  secret_spec="$(IFS=,; echo "${secret_pairs[*]}")"
  deploy_command+=(--update-secrets "${secret_spec}")
fi

echo "2. Desplegando en Cloud Run..."
"${deploy_command[@]}"

echo "OK: deploy completado"
