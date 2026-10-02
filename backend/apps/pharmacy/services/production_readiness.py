from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


@dataclass(frozen=True)
class ReadinessCheck:
    name: str
    ok: bool
    detail: str
    severity: str = "error"


def _has_storage_backend() -> bool:
    legacy = getattr(settings, "DEFAULT_FILE_STORAGE", "")
    if legacy:
        return True
    storages = getattr(settings, "STORAGES", {}) or {}
    default = storages.get("default", {}) if isinstance(storages, dict) else {}
    return bool(default.get("BACKEND"))


def _has_redis() -> bool:
    return bool(getattr(settings, "REDIS_URL", ""))


def _has_event_publisher() -> bool:
    return bool(getattr(settings, "PHARMACY_EVENT_PUBLISHER", ""))


def run_production_readiness_checks(*, strict: bool = False) -> list[ReadinessCheck]:
    checks = [
        ReadinessCheck(
            "debug_disabled",
            not bool(getattr(settings, "DEBUG", False)),
            "DEBUG must be False for production.",
        ),
        ReadinessCheck(
            "secret_key",
            bool(getattr(settings, "SECRET_KEY", "")),
            "SECRET_KEY must be configured.",
        ),
        ReadinessCheck(
            "allowed_hosts",
            bool(getattr(settings, "ALLOWED_HOSTS", [])),
            "ALLOWED_HOSTS must contain at least one production host.",
        ),
        ReadinessCheck(
            "secure_session_cookie",
            bool(getattr(settings, "SESSION_COOKIE_SECURE", False)),
            "SESSION_COOKIE_SECURE must be True for HTTPS production.",
        ),
        ReadinessCheck(
            "secure_csrf_cookie",
            bool(getattr(settings, "CSRF_COOKIE_SECURE", False)),
            "CSRF_COOKIE_SECURE must be True for HTTPS production.",
        ),
        ReadinessCheck(
            "storage_backend",
            _has_storage_backend(),
            "A production default storage backend must be configured.",
        ),
        ReadinessCheck(
            "redis",
            _has_redis(),
            "REDIS_URL must be configured for distributed workers/events.",
        ),
        ReadinessCheck(
            "pharmacy_event_publisher",
            _has_event_publisher(),
            "PHARMACY_EVENT_PUBLISHER must point to a production broker adapter.",
        ),
    ]
    if strict:
        failures = [
            check for check in checks if not check.ok and check.severity == "error"
        ]
        if failures:
            detail = "; ".join(f"{c.name}: {c.detail}" for c in failures)
            raise ImproperlyConfigured(detail)
    return checks


def production_readiness_report(*, strict: bool = False) -> dict:
    checks = run_production_readiness_checks(strict=strict)
    failures = [c for c in checks if not c.ok]
    return {
        "status": "ready" if not failures else "not_ready",
        "checks": {c.name: {"ok": c.ok, "detail": c.detail} for c in checks},
    }


__all__ = (
    "ReadinessCheck",
    "run_production_readiness_checks",
    "production_readiness_report",
)
