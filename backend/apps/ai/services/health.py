from __future__ import annotations

from django.core.cache import cache
from django.db import connection


def liveness() -> dict[str, object]:
    return {"status": "ok", "service": "datavion-ai"}


def readiness() -> dict[str, object]:
    checks: dict[str, str] = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"

    try:
        cache.set("datavion:ai:health", "ok", timeout=10)
        checks["redis"] = "ok" if cache.get("datavion:ai:health") == "ok" else "error"
    except Exception:
        checks["redis"] = "error"

    status = "ok" if all(value == "ok" for value in checks.values()) else "degraded"
    return {"status": status, "service": "datavion-ai", "checks": checks}
