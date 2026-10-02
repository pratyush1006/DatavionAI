"""
Cache constants.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Final

###############################################################################
# Default Time-to-Live (TTL)
###############################################################################

DEFAULT_CACHE_TTL: Final = timedelta(minutes=5)

SHORT_CACHE_TTL: Final = timedelta(minutes=1)

MEDIUM_CACHE_TTL: Final = timedelta(minutes=15)

LONG_CACHE_TTL: Final = timedelta(hours=1)

VERY_LONG_CACHE_TTL: Final = timedelta(hours=24)

###############################################################################
# Cache Key Prefixes
###############################################################################

DEFAULT_CACHE_PREFIX: Final[str] = "datavion"

USER_CACHE_PREFIX: Final[str] = "user"

TENANT_CACHE_PREFIX: Final[str] = "tenant"

ORGANIZATION_CACHE_PREFIX: Final[str] = "organization"

SESSION_CACHE_PREFIX: Final[str] = "session"

CONFIGURATION_CACHE_PREFIX: Final[str] = "configuration"

API_CACHE_PREFIX: Final[str] = "api"

FEATURE_FLAG_CACHE_PREFIX: Final[str] = "feature_flag"

PERMISSION_CACHE_PREFIX: Final[str] = "permission"

###############################################################################
# Distributed Lock
###############################################################################

DEFAULT_LOCK_TIMEOUT: Final = timedelta(seconds=30)

DEFAULT_LOCK_BLOCKING_TIMEOUT: Final = timedelta(seconds=10)

###############################################################################
# Serialization
###############################################################################

DEFAULT_ENCODING: Final[str] = "utf-8"

###############################################################################
# Limits
###############################################################################

MAX_CACHE_KEY_LENGTH: Final[int] = 250

###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
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
)
