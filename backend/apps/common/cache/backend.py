"""
Cache backend abstraction.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Mapping

from apps.common.cache.lock import CacheLock
from apps.common.cache.types import (
    CacheKey,
    CacheMapping,
    CacheTTL,
    CacheValue,
)


class CacheBackend(ABC):
    """
    Abstract cache backend.

    Defines the contract for all cache backend implementations.
    """

    @abstractmethod
    def get(
        self,
        key: CacheKey,
        default: CacheValue | None = None,
    ) -> CacheValue | None:
        """
        Retrieve a value from the cache.
        """

    @abstractmethod
    def set(
        self,
        key: CacheKey,
        value: CacheValue,
        *,
        timeout: CacheTTL | None = None,
    ) -> bool:
        """
        Store a value in the cache.
        """

    @abstractmethod
    def add(
        self,
        key: CacheKey,
        value: CacheValue,
        *,
        timeout: CacheTTL | None = None,
    ) -> bool:
        """
        Store a value only if the key does not already exist.
        """

    @abstractmethod
    def delete(
        self,
        key: CacheKey,
    ) -> bool:
        """
        Remove a value from the cache.
        """

    @abstractmethod
    def clear(
        self,
    ) -> bool:
        """
        Remove all cached values.
        """

    @abstractmethod
    def has_key(
        self,
        key: CacheKey,
    ) -> bool:
        """
        Return whether the cache contains the given key.
        """

    @abstractmethod
    def touch(
        self,
        key: CacheKey,
        *,
        timeout: CacheTTL | None = None,
    ) -> bool:
        """
        Update the expiration time of a cache entry.
        """

    @abstractmethod
    def get_many(
        self,
        keys: list[CacheKey],
    ) -> CacheMapping:
        """
        Retrieve multiple cache entries.
        """

    @abstractmethod
    def set_many(
        self,
        values: Mapping[CacheKey, CacheValue],
        *,
        timeout: CacheTTL | None = None,
    ) -> bool:
        """
        Store multiple cache entries.
        """

    @abstractmethod
    def delete_many(
        self,
        keys: list[CacheKey],
    ) -> int:
        """
        Delete multiple cache entries.

        Returns:
            Number of deleted keys.
        """

    @abstractmethod
    def increment(
        self,
        key: CacheKey,
        delta: int = 1,
    ) -> int:
        """
        Increment a numeric cache value.
        """

    @abstractmethod
    def decrement(
        self,
        key: CacheKey,
        delta: int = 1,
    ) -> int:
        """
        Decrement a numeric cache value.
        """

    @abstractmethod
    def lock(
        self,
        key: CacheKey,
        *,
        timeout: CacheTTL | None = None,
    ) -> CacheLock:
        """
        Create a distributed lock.
        """


__all__: tuple[str, ...] = ("CacheBackend",)
