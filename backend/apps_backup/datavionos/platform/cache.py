"""
Platform cache contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import (
    Any,
    Protocol,
    TypeVar,
    runtime_checkable,
)

T = TypeVar("T")


@dataclass(
    frozen=True,
    slots=True,
)
class CacheOptions:
    """
    Cache storage options.
    """

    ttl: timedelta | None = None

    namespace: str | None = None

    tags: tuple[str, ...] = ()

    tenant_id: str | None = None

    organization_id: str | None = None


@runtime_checkable
class CacheProvider(
    Protocol,
):
    """
    Platform cache abstraction.
    """

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Determine whether a key exists.
        """

    def get(
        self,
        key: str,
        default: T | None = None,
    ) -> T | None:
        """
        Return a cached value.
        """

    def set(
        self,
        key: str,
        value: Any,
        *,
        options: CacheOptions | None = None,
    ) -> None:
        """
        Store a cache value.
        """

    def add(
        self,
        key: str,
        value: Any,
        *,
        options: CacheOptions | None = None,
    ) -> bool:
        """
        Store only if key does not exist.
        """

    def replace(
        self,
        key: str,
        value: Any,
        *,
        options: CacheOptions | None = None,
    ) -> bool:
        """
        Replace only if key exists.
        """

    def remove(
        self,
        key: str,
    ) -> bool:
        """
        Remove a cache entry.
        """

    def clear(
        self,
        *,
        namespace: str | None = None,
    ) -> None:
        """
        Clear cache.

        When namespace is supplied,
        only that namespace is cleared.
        """

    def get_many(
        self,
        keys: list[str],
    ) -> dict[str, Any]:
        """
        Retrieve multiple entries.
        """

    def set_many(
        self,
        values: dict[str, Any],
        *,
        options: CacheOptions | None = None,
    ) -> None:
        """
        Store multiple entries.
        """

    def remove_many(
        self,
        keys: list[str],
    ) -> None:
        """
        Remove multiple entries.
        """

    def invalidate_tag(
        self,
        tag: str,
    ) -> None:
        """
        Invalidate every cache entry
        associated with a tag.
        """

    def invalidate_tenant(
        self,
        tenant_id: str,
    ) -> None:
        """
        Invalidate all cache entries
        belonging to a tenant.
        """


@runtime_checkable
class CacheLock(
    Protocol,
):
    """
    Distributed cache lock.
    """

    def acquire(
        self,
    ) -> bool:
        """
        Acquire the lock.
        """

    def release(
        self,
    ) -> None:
        """
        Release the lock.
        """

    def __enter__(
        self,
    ) -> CacheLock: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: Any,
    ) -> None: ...


__all__ = [
    "CacheOptions",
    "CacheProvider",
    "CacheLock",
]
