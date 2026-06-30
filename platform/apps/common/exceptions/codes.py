"""
Application-wide API error codes.

These codes provide machine-readable identifiers that remain
stable even if error messages change.

Feature applications should reuse these codes instead of
hardcoding error identifiers.
"""

from enum import (
    StrEnum,
    unique,
)


@unique
class ErrorCode(StrEnum):
    """
    Standard API error codes used across Datavion.
    """

    VALIDATION_ERROR = "validation_error"

    AUTHENTICATION_REQUIRED = "authentication_required"

    PERMISSION_DENIED = "permission_denied"

    RESOURCE_NOT_FOUND = "resource_not_found"

    DUPLICATE_RESOURCE = "duplicate_resource"

    INVALID_REQUEST = "invalid_request"

    SERVER_ERROR = "server_error"


__all__ = [
    "ErrorCode",
]
