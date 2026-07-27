"""
HTTP constants.

Provides reusable HTTP-related constants for DatavionAI.
"""

from __future__ import annotations

from typing import Final

DEFAULT_TIMEOUT: Final[float] = 30.0

DEFAULT_CONNECT_TIMEOUT: Final[float] = 10.0

DEFAULT_READ_TIMEOUT: Final[float] = 30.0

DEFAULT_WRITE_TIMEOUT: Final[float] = 30.0

DEFAULT_POOL_TIMEOUT: Final[float] = 10.0


DEFAULT_MAX_RETRIES: Final[int] = 3

DEFAULT_BACKOFF_FACTOR: Final[float] = 0.5


DEFAULT_USER_AGENT: Final[str] = "DatavionAI/1.0"


JSON_CONTENT_TYPE: Final[str] = "application/json"

FORM_CONTENT_TYPE: Final[str] = "application/x-www-form-urlencoded"

MULTIPART_CONTENT_TYPE: Final[str] = "multipart/form-data"


APPLICATION_JSON_ACCEPT: Final[str] = "application/json"


DEFAULT_ENCODING: Final[str] = "utf-8"


__all__: tuple[str, ...] = (
    "APPLICATION_JSON_ACCEPT",
    "DEFAULT_BACKOFF_FACTOR",
    "DEFAULT_CONNECT_TIMEOUT",
    "DEFAULT_ENCODING",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_POOL_TIMEOUT",
    "DEFAULT_READ_TIMEOUT",
    "DEFAULT_TIMEOUT",
    "DEFAULT_USER_AGENT",
    "DEFAULT_WRITE_TIMEOUT",
    "FORM_CONTENT_TYPE",
    "JSON_CONTENT_TYPE",
    "MULTIPART_CONTENT_TYPE",
)
