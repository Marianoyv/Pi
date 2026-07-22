from django.conf import settings


REMOTE_URL_TOOL_SLUGS = frozenset(
    {
        "ai-auditor",
        "landing-performance-snapshot",
        "adtech-debug-tool",
    }
)

REMOTE_TOOLS_UNAVAILABLE_MESSAGE = (
    "Este diagnostico esta temporalmente deshabilitado mientras completamos "
    "el hardening tecnico de las solicitudes remotas."
)


class RemoteUrlToolsDisabled(RuntimeError):
    """Raised before any remote diagnostic can perform outbound work."""


def remote_url_tools_enabled():
    return bool(getattr(settings, "ENABLE_REMOTE_URL_TOOLS", False))


def is_remote_url_tool(slug):
    return slug in REMOTE_URL_TOOL_SLUGS


def is_tool_available(slug):
    return not is_remote_url_tool(slug) or remote_url_tools_enabled()


def require_remote_url_tools_enabled():
    if not remote_url_tools_enabled():
        raise RemoteUrlToolsDisabled(REMOTE_TOOLS_UNAVAILABLE_MESSAGE)
