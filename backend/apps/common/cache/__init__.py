"""
DatavionAI cache framework.

Provides reusable cache abstractions, configuration,
backend interfaces, distributed locking, key generation,
and cache client utilities.
"""

from __future__ import annotations

from apps.common.cache.backend import (
    CacheBackend,
)
from apps.common.cache.client import (
    CacheClient,
)
from apps.common.cache.config import (
    DEFAULT_CACHE_CONFIGURATION,
    DEFAULT_CACHE_OPTIONS,
    CacheConfiguration,
    CacheOptions,
)
from apps.common.cache.constants import (
    API_CACHE_PREFIX,
    CONFIGURATION_CACHE_PREFIX,
    DEFAULT_CACHE_PREFIX,
    DEFAULT_CACHE_TTL,
    DEFAULT_ENCODING,
    DEFAULT_LOCK_BLOCKING_TIMEOUT,
    DEFAULT_LOCK_TIMEOUT,
    FEATURE_FLAG_CACHE_PREFIX,
    LONG_CACHE_TTL,
    MAX_CACHE_KEY_LENGTH,
    MEDIUM_CACHE_TTL,
    ORGANIZATION_CACHE_PREFIX,
    PERMISSION_CACHE_PREFIX,
    SESSION_CACHE_PREFIX,
    SHORT_CACHE_TTL,
    TENANT_CACHE_PREFIX,
    USER_CACHE_PREFIX,
    VERY_LONG_CACHE_TTL,
)
from apps.common.cache.exceptions import (
    CacheConfigurationError,
    CacheConnectionError,
    CacheError,
    CacheKeyError,
    CacheLockError,
    CacheOperationError,
    CacheSerializationError,
)
from apps.common.cache.keys import (
    build_cache_key,
    join_cache_key,
    validate_cache_key,
)
from apps.common.cache.lock import (
    CacheLock,
)
from apps.common.cache.types import (
    CacheKey,
    CacheMapping,
    CachePrefix,
    CacheTTL,
    CacheValue,
)

__all__: tuple[str, ...] = (
    # Client
    "CacheClient",
    "CacheBackend",
    # Configuration
    "CacheConfiguration",
    "CacheOptions",
    "DEFAULT_CACHE_CONFIGURATION",
    "DEFAULT_CACHE_OPTIONS",
    # Lock
    "CacheLock",
    # Keys
    "build_cache_key",
    "join_cache_key",
    "validate_cache_key",
    # Types
    "CacheKey",
    "CacheMapping",
    "CachePrefix",
    "CacheTTL",
    "CacheValue",
    # Constants
    "API_CACHE_PREFIX",
    "CONFIGURATION_CACHE_PREFIX",
    "DEFAULT_CACHE_PREFIX",
    "DEFAULT_CACHE_TTL",
    "DEFAULT_ENCODING",
    "DEFAULT_LOCK_BLOCKING_TIMEOUT",
    "DEFAULT_LOCK_TIMEOUT",
    "FEATURE_FLAG_CACHE_PREFIX",
    "LONG_CACHE_TTL",
    "MAX_CACHE_KEY_LENGTH",
    "MEDIUM_CACHE_TTL",
    "ORGANIZATION_CACHE_PREFIX",
    "PERMISSION_CACHE_PREFIX",
    "SESSION_CACHE_PREFIX",
    "SHORT_CACHE_TTL",
    "TENANT_CACHE_PREFIX",
    "USER_CACHE_PREFIX",
    "VERY_LONG_CACHE_TTL",
    # Exceptions
    "CacheConfigurationError",
    "CacheConnectionError",
    "CacheError",
    "CacheKeyError",
    "CacheLockError",
    "CacheOperationError",
    "CacheSerializationError",
)
