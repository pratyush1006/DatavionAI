"""Redis system checks for the DatavionOS platform.

Validates Redis configuration and connectivity.
"""

from __future__ import annotations

from django.conf import settings
from django.core.checks import Error, Tags, Warning, register


@register(Tags.caches)
def redis_check(
    app_configs,
    **kwargs,
):
    """
    Validate Redis configuration and availability.

    The check validates the actual configured REDIS_URL.
    It does not substitute another endpoint.
    """

    messages = []

    redis_url = str(
        getattr(
            settings,
            "REDIS_URL",
            "",
        )
        or ""
    ).strip()

    if not redis_url:
        messages.append(
            Warning(
                "REDIS_URL is not configured.",
                hint=(
                    "Configure REDIS_URL for Redis-backed "
                    "cache, Celery and distributed services."
                ),
                id="datavion.W003",
            )
        )

        return messages

    try:
        import redis

        client = redis.Redis.from_url(
            redis_url,
            socket_connect_timeout=5,
            socket_timeout=5,
        )

        client.ping()
        client.close()

    except Exception as exc:
        messages.append(
            Error(
                "Redis connection failed.",
                hint=(
                    "The configured Redis endpoint did not "
                    "respond within the canonical 5-second "
                    "connection/read timeout. "
                    f"{type(exc).__name__}: {exc}"
                ),
                id="datavion.E005",
            )
        )

    return messages
