from __future__ import annotations

import os
from dataclasses import dataclass

from django.conf import settings


@dataclass(frozen=True)
class DeploymentStatus:
    environment: str
    debug: bool
    secret_key_configured: bool
    allowed_hosts_configured: bool
    redis_configured: bool
    provider_configured: bool
    secure_cookies: bool
    csrf_protection: bool

    @property
    def production_ready(self) -> bool:
        return (
            not self.debug
            and self.secret_key_configured
            and self.allowed_hosts_configured
            and self.redis_configured
            and self.provider_configured
            and self.secure_cookies
            and self.csrf_protection
        )


def deployment_status() -> DeploymentStatus:
    environment = str(
        getattr(settings, "DJANGO_ENV", "")
        or os.environ.get("DJANGO_ENV", "")
        or "development"
    ).lower()

    debug = bool(getattr(settings, "DEBUG", False))
    secret_key = str(getattr(settings, "SECRET_KEY", "") or "")
    allowed_hosts = list(getattr(settings, "ALLOWED_HOSTS", []) or [])
    redis_url = str(
        getattr(settings, "REDIS_URL", "") or os.environ.get("REDIS_URL", "") or ""
    )
    provider = str(
        getattr(settings, "AI_PROVIDER", "") or os.environ.get("AI_PROVIDER", "") or ""
    )

    secure_cookies = bool(
        getattr(settings, "SESSION_COOKIE_SECURE", False)
        and getattr(settings, "CSRF_COOKIE_SECURE", False)
    )
    csrf_protection = bool(
        getattr(settings, "CSRF_USE_SESSIONS", False)
        or getattr(settings, "CSRF_COOKIE_SECURE", False)
    )

    return DeploymentStatus(
        environment=environment,
        debug=debug,
        secret_key_configured=bool(secret_key and secret_key != "change-me"),
        allowed_hosts_configured=bool(allowed_hosts and "*" not in allowed_hosts),
        redis_configured=bool(redis_url),
        provider_configured=bool(provider),
        secure_cookies=secure_cookies,
        csrf_protection=csrf_protection,
    )


def validate_deployment_environment(*, production: bool = False) -> list[str]:
    status = deployment_status()
    errors: list[str] = []

    if production or status.environment in {"production", "prod"}:
        if status.debug:
            errors.append("DEBUG must be false in production")
        if not status.secret_key_configured:
            errors.append("SECRET_KEY must be configured")
        if not status.allowed_hosts_configured:
            errors.append("ALLOWED_HOSTS must be explicit")
        if not status.redis_configured:
            errors.append("REDIS_URL must be configured")
        if not status.provider_configured:
            errors.append("AI_PROVIDER must be configured")
        if not status.secure_cookies:
            errors.append("Secure session/CSRF cookies must be enabled")
    return errors
