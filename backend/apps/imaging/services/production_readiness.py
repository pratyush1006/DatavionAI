"""Production readiness contracts for Imaging/Radiology."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.conf import settings
from django.db import connection


@dataclass(frozen=True)
class ReadinessCheck:
    name: str
    ok: bool
    detail: str
    severity: str = "error"


def _configured(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    return bool(value)


def _database_ok() -> tuple[bool, str]:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True, "Configured database connection is reachable."
    except Exception as exc:  # pragma: no cover - defensive runtime boundary
        return False, f"Database readiness check failed: {exc}"


def run_production_readiness_checks(*, strict: bool = False) -> list[ReadinessCheck]:
    """Return deterministic application and infrastructure readiness checks.

    strict=True is intended for the actual production deployment gate.
    Development environments may use strict=False so optional infrastructure
    warnings do not make ordinary local development unusable.
    """
    db_ok, db_detail = _database_ok()
    redis_ok = _configured(getattr(settings, "REDIS_URL", ""))
    publisher_ok = _configured(getattr(settings, "IMAGING_EVENT_PUBLISHER", ""))
    storage_ok = _configured(
        getattr(settings, "DEFAULT_FILE_STORAGE", "")
    ) or _configured(getattr(settings, "STORAGES", {}))

    checks = [
        ReadinessCheck(
            "debug_disabled",
            not bool(getattr(settings, "DEBUG", False)),
            "DEBUG must be False in production.",
        ),
        ReadinessCheck(
            "secret_key",
            _configured(getattr(settings, "SECRET_KEY", "")),
            "SECRET_KEY must be configured.",
        ),
        ReadinessCheck(
            "allowed_hosts",
            _configured(getattr(settings, "ALLOWED_HOSTS", [])),
            "ALLOWED_HOSTS must be explicitly configured.",
        ),
        ReadinessCheck(
            "secure_session_cookie",
            bool(getattr(settings, "SESSION_COOKIE_SECURE", False)),
            "SESSION_COOKIE_SECURE must be True in production.",
        ),
        ReadinessCheck(
            "secure_csrf_cookie",
            bool(getattr(settings, "CSRF_COOKIE_SECURE", False)),
            "CSRF_COOKIE_SECURE must be True in production.",
        ),
        ReadinessCheck(
            "ssl_redirect",
            bool(getattr(settings, "SECURE_SSL_REDIRECT", False)),
            "SECURE_SSL_REDIRECT should be True behind the production TLS boundary.",
            severity="warning",
        ),
        ReadinessCheck(
            "hsts",
            int(getattr(settings, "SECURE_HSTS_SECONDS", 0) or 0) > 0,
            "SECURE_HSTS_SECONDS should be greater than zero in production.",
            severity="warning",
        ),
        ReadinessCheck(
            "database",
            db_ok,
            db_detail,
        ),
        ReadinessCheck(
            "redis",
            redis_ok,
            "REDIS_URL must be configured for distributed cache/Celery/outbox operation.",
            severity="error" if strict else "warning",
        ),
        ReadinessCheck(
            "imaging_event_publisher",
            publisher_ok,
            "IMAGING_EVENT_PUBLISHER must identify a deployable event publisher.",
            severity="error" if strict else "warning",
        ),
        ReadinessCheck(
            "storage",
            storage_ok,
            "A production storage backend must be configured for imaging artifacts.",
            severity="error" if strict else "warning",
        ),
    ]
    return checks


def production_readiness_report(*, strict: bool = False) -> dict[str, Any]:
    """Return a machine-readable readiness report."""
    checks = run_production_readiness_checks(strict=strict)
    blocking = [c for c in checks if not c.ok and c.severity == "error"]
    return {
        "status": "ready" if not blocking else "not_ready",
        "strict": bool(strict),
        "checks": {
            c.name: {
                "ok": c.ok,
                "detail": c.detail,
                "severity": c.severity,
            }
            for c in checks
        },
    }
