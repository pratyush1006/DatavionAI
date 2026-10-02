"""
Enterprise cache client.
"""

from __future__ import annotations

from apps.common.cache.backend import (
    CacheBackend,
)
from apps.common.cache.config import (
    DEFAULT_CACHE_CONFIGURATION,
    DEFAULT_CACHE_OPTIONS,
    CacheConfiguration,
    CacheOptions,
)
from apps.common.cache.keys import (
    build_cache_key,
)
from apps.common.cache.lock import (
    CacheLock,
)
from apps.common.cache.types import (
    CacheKey,
    CacheTTL,
    CacheValue,
)


class CacheClient:
    """
    Enterprise cache client.

    Provides a consistent cache API independent of the
    underlying backend implementation.
    """

    def __init__(
        self,
        backend: CacheBackend,
        configuration: CacheConfiguration = DEFAULT_CACHE_CONFIGURATION,
    ) -> None:
        """
        Initialize the cache client.
        """

        self._backend = backend
        self._configuration = configuration

    @property
    def backend(
        self,
    ) -> CacheBackend:
        """
        Return the configured cache backend.
        """

        return self._backend

    @property
    def configuration(
        self,
    ) -> CacheConfiguration:
        """
        Return the cache configuration.
        """

        return self._configuration

    def _build_key(
        self,
        key: CacheKey,
        *,
        options: CacheOptions,
    ) -> CacheKey:
        """
        Build the final cache key.
        """

        prefix = (
            options.key_prefix
            if options.key_prefix is not None
            else self._configuration.key_prefix
        )

        return build_cache_key(
            key,
            prefix=prefix,
        )

    def _build_timeout(
        self,
        *,
        options: CacheOptions,
    ) -> CacheTTL:
        """
        Resolve the cache timeout.
        """

        if options.timeout is not None:
            return options.timeout

        return self._configuration.default_timeout

    def get(
        self,
        key: CacheKey,
        *,
        default: CacheValue | None = None,
        options: CacheOptions = DEFAULT_CACHE_OPTIONS,
    ) -> CacheValue | None:
        """
        Retrieve a cached value.
        """

        cache_key = self._build_key(
            key,
            options=options,
        )

        return self._backend.get(
            cache_key,
            default,
        )

    def set(
        self,
        key: CacheKey,
        value: CacheValue,
        *,
        options: CacheOptions = DEFAULT_CACHE_OPTIONS,
    ) -> bool:
        """
        Store a cache value.
        """

        cache_key = self._build_key(
            key,
            options=options,
        )

        timeout = self._build_timeout(
            options=options,
        )

        return self._backend.set(
            cache_key,
            value,
            timeout=timeout,
        )

    def add(
        self,
        key: CacheKey,
        value: CacheValue,
        *,
        options: CacheOptions = DEFAULT_CACHE_OPTIONS,
    ) -> bool:
        """
        Store a cache value if it does not already exist.
        """

        cache_key = self._build_key(
            key,
            options=options,
        )

        timeout = self._build_timeout(
            options=options,
        )

        return self._backend.add(
            cache_key,
            value,
            timeout=timeout,
        )

    def delete(
        self,
        key: CacheKey,
        *,
        options: CacheOptions = DEFAULT_CACHE_OPTIONS,
    ) -> bool:
        """
        Delete a cache entry.
        """

        cache_key = self._build_key(
            key,
            options=options,
        )

        return self._backend.delete(
            cache_key,
        )

    def exists(
        self,
        key: CacheKey,
        *,
        options: CacheOptions = DEFAULT_CACHE_OPTIONS,
    ) -> bool:
        """
        Return whether a cache key exists.
        """

        cache_key = self._build_key(
            key,
            options=options,
        )

        return self._backend.has_key(
            cache_key,
        )

    def touch(
        self,
        key: CacheKey,
        *,
        options: CacheOptions = DEFAULT_CACHE_OPTIONS,
    ) -> bool:
        """
        Refresh the timeout of a cache entry.
        """

        cache_key = self._build_key(
            key,
            options=options,
        )

        timeout = self._build_timeout(
            options=options,
        )

        return self._backend.touch(
            cache_key,
            timeout=timeout,
        )

    def get_many(
        self,
        keys: list[CacheKey],
        *,
        options: CacheOptions | None = None,
    ) -> dict[CacheKey, CacheValue]:
        """
        Retrieve multiple cache entries.
        """

        cache_options = options or DEFAULT_CACHE_OPTIONS

        cache_keys = [
            self._build_key(
                key,
                options=cache_options,
            )
            for key in keys
        ]

        return dict(
            self._backend.get_many(
                cache_keys,
            ),
        )

    def set_many(
        self,
        values: dict[CacheKey, CacheValue],
        *,
        options: CacheOptions | None = None,
    ) -> bool:
        """
        Store multiple cache entries.
        """

        cache_options = options or DEFAULT_CACHE_OPTIONS

        cache_values = {
            self._build_key(
                key,
                options=cache_options,
            ): value
            for key, value in values.items()
        }

        timeout = self._build_timeout(
            options=cache_options,
        )

        return self._backend.set_many(
            cache_values,
            timeout=timeout,
        )

    def delete_many(
        self,
        keys: list[CacheKey],
        *,
        options: CacheOptions | None = None,
    ) -> int:
        """
        Delete multiple cache entries.
        """

        cache_options = options or DEFAULT_CACHE_OPTIONS

        cache_keys = [
            self._build_key(
                key,
                options=cache_options,
            )
            for key in keys
        ]

        return self._backend.delete_many(
            cache_keys,
        )

    def increment(
        self,
        key: CacheKey,
        delta: int = 1,
        *,
        options: CacheOptions | None = None,
    ) -> int:
        """
        Increment a numeric cache value.
        """

        cache_options = options or DEFAULT_CACHE_OPTIONS

        cache_key = self._build_key(
            key,
            options=cache_options,
        )

        return self._backend.increment(
            cache_key,
            delta,
        )

    def decrement(
        self,
        key: CacheKey,
        delta: int = 1,
        *,
        options: CacheOptions | None = None,
    ) -> int:
        """
        Decrement a numeric cache value.
        """

        cache_options = options or DEFAULT_CACHE_OPTIONS

        cache_key = self._build_key(
            key,
            options=cache_options,
        )

        return self._backend.decrement(
            cache_key,
            delta,
        )

    def clear(
        self,
    ) -> bool:
        """
        Remove all cached values.
        """

        return self._backend.clear()

    def lock(
        self,
        key: CacheKey,
        *,
        options: CacheOptions | None = None,
    ) -> CacheLock:
        """
        Create a distributed cache lock.
        """

        cache_options = options or DEFAULT_CACHE_OPTIONS

        cache_key = self._build_key(
            key,
            options=cache_options,
        )

        timeout = self._build_timeout(
            options=cache_options,
        )

        return self._backend.lock(
            cache_key,
            timeout=timeout,
        )


__all__: tuple[str, ...] = ("CacheClient",)
