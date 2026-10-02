from __future__ import annotations

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db import connection

from apps.ai.production import (
    credential_configured,
    production_config,
    validate_production_environment,
)


class Command(BaseCommand):
    help = "Validate DatavionAI production prerequisites"

    def handle(self, *args, **kwargs):
        errors = validate_production_environment()

        if getattr(settings, "DEBUG", False):
            errors.append("DEBUG=True")

        if not getattr(settings, "ALLOWED_HOSTS", []):
            errors.append("ALLOWED_HOSTS is empty")

        redis_url = str(getattr(settings, "REDIS_URL", "")).strip()
        if not redis_url:
            errors.append("Effective REDIS_URL is empty")

        cache_backend = (
            getattr(settings, "CACHES", {}).get("default", {}).get("BACKEND", "")
        )

        if redis_url and cache_backend != "django.core.cache.backends.redis.RedisCache":
            errors.append("Redis is configured but Django cache is not Redis-backed")

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except Exception as exc:
            errors.append(f"Database connectivity failed: {type(exc).__name__}")

        try:
            cache.set("datavion:ai:readiness", "ok", timeout=30)
            if cache.get("datavion:ai:readiness") != "ok":
                errors.append("Cache read/write failed")
        except Exception as exc:
            errors.append(f"Cache connectivity failed: {type(exc).__name__}")

        try:
            runtime = production_config()
            self.stdout.write(f"AI_PROVIDER: {runtime.provider}")
            self.stdout.write(f"AI_MODEL: {runtime.model}")
            self.stdout.write(f"AI_EMBEDDING_PROVIDER: {runtime.embedding_provider}")
            self.stdout.write(f"AI_EMBEDDING_MODEL: {runtime.embedding_model}")
            self.stdout.write(
                "AI CREDENTIALS: CONFIGURED"
                if credential_configured(runtime.provider)
                else "AI CREDENTIALS: NOT DETECTED"
            )
            self.stdout.write(
                "EMBEDDING CREDENTIALS: CONFIGURED"
                if credential_configured(runtime.embedding_provider)
                else "EMBEDDING CREDENTIALS: NOT DETECTED"
            )
        except Exception as exc:
            errors.append(f"AI configuration failed: {type(exc).__name__}")

        if errors:
            self.stdout.write(self.style.ERROR("PRODUCTION READINESS: FAIL"))
            for error in errors:
                self.stdout.write(self.style.ERROR(" - " + error))
            raise SystemExit(2)

        self.stdout.write(self.style.SUCCESS("PRODUCTION READINESS: PASS"))
