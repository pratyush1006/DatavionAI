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
    """
    Standard machine-readable API error codes for Datavion AI.

    Rules:
    - Never rename existing codes.
    - Never remove existing codes.
    - Only add new codes.
    - Clients should rely on these values instead of messages.
    """

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    VALIDATION_ERROR = "validation_error"
    INVALID_REQUEST = "invalid_request"

    # ------------------------------------------------------------------
    # Authentication & Authorization
    # ------------------------------------------------------------------

    AUTHENTICATION_REQUIRED = "authentication_required"
    PERMISSION_DENIED = "permission_denied"

    # ------------------------------------------------------------------
    # Resources
    # ------------------------------------------------------------------

    RESOURCE_NOT_FOUND = "resource_not_found"
    DUPLICATE_RESOURCE = "duplicate_resource"

    # ------------------------------------------------------------------
    # Organization / Multi-tenancy
    # ------------------------------------------------------------------

    ORGANIZATION_NOT_FOUND = "organization_not_found"
    ORGANIZATION_ACCESS_DENIED = "organization_access_denied"

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    CONFIGURATION_NOT_FOUND = "configuration_not_found"
    FEATURE_DISABLED = "feature_disabled"

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------

    FILE_NOT_FOUND = "file_not_found"
    INVALID_FILE_TYPE = "invalid_file_type"
    FILE_TOO_LARGE = "file_too_large"

    # ------------------------------------------------------------------
    # Rate Limiting
    # ------------------------------------------------------------------

    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

    # ------------------------------------------------------------------
    # External Services
    # ------------------------------------------------------------------

    EXTERNAL_SERVICE_ERROR = "external_service_error"
    SERVICE_UNAVAILABLE = "service_unavailable"

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------

    SERVER_ERROR = "server_error"


__all__ = [
    "ErrorCode",
]
