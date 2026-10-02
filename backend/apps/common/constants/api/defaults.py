"""
DatavionAI API Default Configuration Constants.

Centralized operational defaults used throughout the DatavionAI platform.

This module defines default values for request handling, uploads,
downloads, payload sizes, idempotency, caching, retries, pagination,
and API gateway behavior.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No business logic
- Environment values should override these defaults
- Safe to import everywhere
"""

from __future__ import annotations

from typing import Final

###############################################################################
# Request Timeouts (seconds)
###############################################################################

DEFAULT_REQUEST_TIMEOUT: Final[int] = 30

DEFAULT_CONNECT_TIMEOUT: Final[int] = 10

DEFAULT_READ_TIMEOUT: Final[int] = 30

DEFAULT_WRITE_TIMEOUT: Final[int] = 30

###############################################################################
# Upload Limits
###############################################################################

DEFAULT_MAX_UPLOAD_SIZE_BYTES: Final[int] = 25 * 1024 * 1024

DEFAULT_MAX_DOWNLOAD_SIZE_BYTES: Final[int] = 100 * 1024 * 1024

DEFAULT_MAX_REQUEST_BODY_SIZE_BYTES: Final[int] = 10 * 1024 * 1024

###############################################################################
# Payload Limits
###############################################################################

DEFAULT_MAX_JSON_DEPTH: Final[int] = 25

DEFAULT_MAX_ARRAY_ITEMS: Final[int] = 1000

DEFAULT_MAX_OBJECT_PROPERTIES: Final[int] = 500

###############################################################################
# API Gateway
###############################################################################

DEFAULT_MAX_REQUESTS_PER_SECOND: Final[int] = 100

DEFAULT_MAX_CONCURRENT_REQUESTS: Final[int] = 1000

###############################################################################
# Retry Policy
###############################################################################

DEFAULT_MAX_RETRIES: Final[int] = 3

DEFAULT_INITIAL_RETRY_DELAY_SECONDS: Final[int] = 1

DEFAULT_MAX_RETRY_DELAY_SECONDS: Final[int] = 30

DEFAULT_RETRY_BACKOFF_MULTIPLIER: Final[float] = 2.0

###############################################################################
# Idempotency
###############################################################################

DEFAULT_IDEMPOTENCY_TTL_SECONDS: Final[int] = 24 * 60 * 60

###############################################################################
# Cache
###############################################################################

DEFAULT_CACHE_TTL_SECONDS: Final[int] = 300

DEFAULT_SHORT_CACHE_TTL_SECONDS: Final[int] = 60

DEFAULT_LONG_CACHE_TTL_SECONDS: Final[int] = 3600

###############################################################################
# Rate Limiting
###############################################################################

DEFAULT_RATE_LIMIT_WINDOW_SECONDS: Final[int] = 60

DEFAULT_RATE_LIMIT_REQUESTS: Final[int] = 100

###############################################################################
# Pagination
###############################################################################

DEFAULT_PAGE_SIZE: Final[int] = 20

DEFAULT_MAX_PAGE_SIZE: Final[int] = 100

DEFAULT_CURSOR_PAGE_SIZE: Final[int] = 50

###############################################################################
# Bulk Operations
###############################################################################

DEFAULT_BULK_OPERATION_SIZE: Final[int] = 100

DEFAULT_IMPORT_BATCH_SIZE: Final[int] = 500

DEFAULT_EXPORT_BATCH_SIZE: Final[int] = 1000

###############################################################################
# Response Compression
###############################################################################

DEFAULT_ENABLE_GZIP: Final[bool] = True

DEFAULT_ENABLE_ETAG: Final[bool] = True

###############################################################################
# Reserved Defaults
###############################################################################

DEFAULT_HTTP_PORT: Final[int] = 80

DEFAULT_HTTPS_PORT: Final[int] = 443

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper())
