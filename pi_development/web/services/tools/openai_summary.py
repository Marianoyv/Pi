from django.conf import settings
import requests

from pi_development.web.tool_availability import require_remote_url_tools_enabled


def generate_ai_summary(diagnosis):
    require_remote_url_tools_enabled()
    if not settings.OPENAI_API_KEY or not settings.OPENAI_AUDITOR_MODEL:
        return {
            "available": False,
            "status": "unconfigured",
            "text": "",
            "message": "OpenAI no está configurado para enriquecer este análisis todavía.",
        }

    prompt = _build_prompt(diagnosis)
    payload = {
        "model": settings.OPENAI_AUDITOR_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Resume auditorías técnicas web en español, con tono sobrio, útil y directo.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.3,
        "max_tokens": 220,
    }

    try:
        response = requests.post(
            f"{settings.OPENAI_API_BASE.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=settings.TOOLS_HTTP_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        text = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
        if not text:
            raise ValueError("OpenAI no devolvio contenido util.")
        return {
            "available": True,
            "status": "ok",
            "text": text,
            "message": "Resumen asistido generado por OpenAI.",
        }
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as exc:
        return {
            "available": False,
            "status": "error",
            "text": "",
            "message": "La capa OpenAI esta preparada, pero no pudo responder en esta ejecucion.",
            "error": str(exc),
        }


def _build_prompt(diagnosis):
    opportunities = ", ".join(diagnosis.get("opportunities") or [])
    technical = ", ".join(diagnosis.get("technical_observations") or [])
    recommendation = diagnosis.get("recommendation") or ""
    return (
        f"URL analizada: {diagnosis.get('target_url')}. "
        f"Estado general: {diagnosis.get('overview', {}).get('label')}. "
        f"Resumen: {diagnosis.get('overview', {}).get('summary')}. "
        f"Observaciones tecnicas: {technical}. "
        f"Oportunidades: {opportunities}. "
        f"Recomendacion actual: {recommendation}. "
        "Devuelve un resumen breve en 3 a 4 frases sin marketing."
    )
