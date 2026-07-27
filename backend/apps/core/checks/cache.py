"""
Cache system checks.
"""

from __future__ import annotations

from django.core.cache import caches
from django.core.checks import Error, Tags, register


@register(Tags.caches)
def cache_check(
    app_configs,
    **kwargs,
):
    """
    Verify cache backend.
    """

    errors = []

    try:
        cache = caches["default"]

        cache.set(
            "__health__",
            "ok",
            timeout=1,
        )

        cache.get("__health__")

    except Exception as exc:
        errors.append(
            Error(
                "Cache backend is unavailable.",
                hint=str(exc),
                id="datavion.E002",
            ),
        )

    return errors
