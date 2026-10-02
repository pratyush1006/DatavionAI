"""
Cache configuration.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.cache.constants import (
    DEFAULT_CACHE_PREFIX,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CacheConfiguration:
    """
    Cache configuration.
    """

    alias: str = "default"

    key_prefix: str = DEFAULT_CACHE_PREFIX

    default_timeout: int | None = None

    version: int | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class CacheOptions:
    """
    Per-operation cache options.
    """

    timeout: int | None = None

    version: int | None = None

    key_prefix: str | None = None


DEFAULT_CACHE_CONFIGURATION: CacheConfiguration = CacheConfiguration()

DEFAULT_CACHE_OPTIONS: CacheOptions = CacheOptions()


__all__: tuple[str, ...] = (
    "CacheConfiguration",
    "CacheOptions",
    "DEFAULT_CACHE_CONFIGURATION",
    "DEFAULT_CACHE_OPTIONS",
)
