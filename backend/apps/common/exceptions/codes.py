"""
Application-wide API error codes.

These machine-readable codes remain stable even if
human-readable error messages change. Feature applications
should reuse these codes instead of hardcoding identifiers.
"""

from __future__ import annotations

from enum import StrEnum, unique


@unique
class ErrorCode(StrEnum):
    VALIDATION_ERROR = "validation_error"

    INVALID_REQUEST = "invalid_request"

    AUTHENTICATION_REQUIRED = "authentication_required"

    PERMISSION_DENIED = "permission_denied"

    RESOURCE_NOT_FOUND = "resource_not_found"

    DUPLICATE_RESOURCE = "duplicate_resource"

    CONFIGURATION_NOT_FOUND = "configuration_not_found"

    FEATURE_DISABLED = "feature_disabled"

    FILE_NOT_FOUND = "file_not_found"

    INVALID_FILE_TYPE = "invalid_file_type"

    FILE_TOO_LARGE = "file_too_large"

    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

    EXTERNAL_SERVICE_ERROR = "external_service_error"

    SERVICE_UNAVAILABLE = "service_unavailable"

    SERVER_ERROR = "server_error"


__all__ = [
    "ErrorCode",
]
