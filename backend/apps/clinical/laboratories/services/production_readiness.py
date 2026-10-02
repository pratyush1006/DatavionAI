from django.conf import settings
from django.db import connection


def run_production_readiness_checks(*, strict=False):
    checks = {
        "debug_disabled": not bool(getattr(settings, "DEBUG", True)),
        "secret_key": bool(getattr(settings, "SECRET_KEY", "")),
        "allowed_hosts": bool(getattr(settings, "ALLOWED_HOSTS", [])),
        "secure_session_cookie": bool(
            getattr(settings, "SESSION_COOKIE_SECURE", False)
        ),
        "secure_csrf_cookie": bool(getattr(settings, "CSRF_COOKIE_SECURE", False)),
    }
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = True
    except Exception:
        checks["database"] = False
    return {
        "status": "ready" if all(checks.values()) else "blocked",
        "checks": checks,
        "strict": strict,
    }
