"""
Redis system checks for the DatavionOS platform.

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
    """

    messages = []

    redis_url = getattr(
        settings,
        "REDIS_URL",
        None,
    )

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
            socket_connect_timeout=2,
        )

        client.ping()

    except Exception as exc:
        messages.append(
            Error(
                "Redis connection failed.",
                hint=str(exc),
                id="datavion.E005",
            )
        )

    return messages
