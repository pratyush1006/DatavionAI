"""
Cache exception hierarchy.
"""

from __future__ import annotations


class CacheError(Exception):
    """
    Base exception for all cache-related errors.
    """


class CacheConfigurationError(CacheError):
    """
    Raised when the cache configuration is invalid.
    """


class CacheConnectionError(CacheError):
    """
    Raised when a cache backend cannot be reached.
    """


class CacheOperationError(CacheError):
    """
    Raised when a cache operation fails.
    """


class CacheSerializationError(CacheOperationError):
    """
    Raised when a cache value cannot be serialized or deserialized.
    """


class CacheKeyError(CacheOperationError):
    """
    Raised when a cache key is invalid.
    """


class CacheLockError(CacheOperationError):
    """
    Raised when a distributed lock operation fails.
    """


__all__: tuple[str, ...] = (
    "CacheConfigurationError",
    "CacheConnectionError",
    "CacheError",
    "CacheKeyError",
    "CacheLockError",
    "CacheOperationError",
    "CacheSerializationError",
)
