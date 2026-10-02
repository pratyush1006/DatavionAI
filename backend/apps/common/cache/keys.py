"""
Cache key utilities.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.cache.constants import (
    DEFAULT_CACHE_PREFIX,
    MAX_CACHE_KEY_LENGTH,
)
from apps.common.cache.exceptions import (
    CacheKeyError,
)
from apps.common.cache.types import (
    CacheKey,
    CachePrefix,
)


def build_cache_key(
    *parts: object,
    prefix: CachePrefix = DEFAULT_CACHE_PREFIX,
) -> CacheKey:
    """
    Build a cache key from the supplied parts.

    Example:
        build_cache_key("patient", patient_id)

    Returns:
        datavion:patient:123
    """

    components: list[str] = []

    if prefix:
        components.append(prefix)

    for part in parts:
        value = str(part).strip()

        if not value:
            raise CacheKeyError(
                "Cache key components cannot be empty.",
            )

        components.append(value)

    key = ":".join(components)

    validate_cache_key(key)

    return key


def validate_cache_key(
    key: CacheKey,
) -> None:
    """
    Validate a cache key.
    """

    if not key:
        raise CacheKeyError(
            "Cache key cannot be empty.",
        )

    if len(key) > MAX_CACHE_KEY_LENGTH:
        raise CacheKeyError(
            (
                f"Cache key exceeds the maximum length "
                f"of {MAX_CACHE_KEY_LENGTH} characters."
            ),
        )


def join_cache_key(
    parts: Iterable[object],
    *,
    prefix: CachePrefix = DEFAULT_CACHE_PREFIX,
) -> CacheKey:
    """
    Build a cache key from an iterable.
    """

    return build_cache_key(
        *parts,
        prefix=prefix,
    )


__all__: tuple[str, ...] = (
    "build_cache_key",
    "join_cache_key",
    "validate_cache_key",
)
