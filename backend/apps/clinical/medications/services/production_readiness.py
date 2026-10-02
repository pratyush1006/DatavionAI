from __future__ import annotations

from django.conf import settings
from django.db import connection


def medication_production_readiness() -> dict:
    checks = {
        "debug_disabled": settings.DEBUG is False,
        "secret_key_configured": bool(getattr(settings, "SECRET_KEY", "")),
        "database_configured": bool(connection.settings_dict.get("ENGINE")),
        "event_publisher_configured": bool(
            getattr(settings, "MEDICATION_EVENT_PUBLISHER", "")
        ),
    }
    return {
        "ready": all(checks.values()),
        "checks": checks,
    }
