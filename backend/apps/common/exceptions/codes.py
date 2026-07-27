"""
DatavionAI Exception Error Codes.

Centralized error codes used throughout the DatavionAI platform.

Design Principles
-----------------
- Immutable
- Framework agnostic
- Stable API contract
- Machine readable
- Human friendly
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final


class ErrorCode(StrEnum):
    """
    Canonical platform error codes.
    """

    # ------------------------------------------------------------------
    # Generic
    # ------------------------------------------------------------------

    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"

    # ------------------------------------------------------------------
    # Request
    # ------------------------------------------------------------------

    BAD_REQUEST = "BAD_REQUEST"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"
    INVALID_REQUEST = "INVALID_REQUEST"
    MALFORMED_REQUEST = "MALFORMED_REQUEST"
    UNSUPPORTED_MEDIA_TYPE = "UNSUPPORTED_MEDIA_TYPE"

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    UNAUTHENTICATED = "UNAUTHENTICATED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    ACCOUNT_INACTIVE = "ACCOUNT_INACTIVE"

    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"
    TOKEN_REVOKED = "TOKEN_REVOKED"

    MFA_REQUIRED = "MFA_REQUIRED"
    MFA_INVALID = "MFA_INVALID"

    # ------------------------------------------------------------------
    # Authorization
    # ------------------------------------------------------------------

    PERMISSION_DENIED = "PERMISSION_DENIED"
    ACCESS_DENIED = "ACCESS_DENIED"
    FORBIDDEN = "FORBIDDEN"

    # ------------------------------------------------------------------
    # Resource
    # ------------------------------------------------------------------

    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
    RESOURCE_LOCKED = "RESOURCE_LOCKED"
    RESOURCE_ARCHIVED = "RESOURCE_ARCHIVED"

    # ------------------------------------------------------------------
    # Business Rules
    # ------------------------------------------------------------------

    BUSINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"
    OPERATION_NOT_ALLOWED = "OPERATION_NOT_ALLOWED"
    PRECONDITION_FAILED = "PRECONDITION_FAILED"

    # ------------------------------------------------------------------
    # Organization / Tenant
    # ------------------------------------------------------------------

    ORGANIZATION_NOT_FOUND = "ORGANIZATION_NOT_FOUND"
    TENANT_NOT_FOUND = "TENANT_NOT_FOUND"
    TENANT_MISMATCH = "TENANT_MISMATCH"

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    DATABASE_ERROR = "DATABASE_ERROR"
    DATABASE_TIMEOUT = "DATABASE_TIMEOUT"
    DATABASE_CONSTRAINT_ERROR = "DATABASE_CONSTRAINT_ERROR"

    # ------------------------------------------------------------------
    # Cache
    # ------------------------------------------------------------------

    CACHE_ERROR = "CACHE_ERROR"
    CACHE_TIMEOUT = "CACHE_TIMEOUT"

    # ------------------------------------------------------------------
    # External Services
    # ------------------------------------------------------------------

    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    EXTERNAL_SERVICE_TIMEOUT = "EXTERNAL_SERVICE_TIMEOUT"

    # ------------------------------------------------------------------
    # Rate Limiting
    # ------------------------------------------------------------------

    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

    # ------------------------------------------------------------------
    # File
    # ------------------------------------------------------------------

    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    INVALID_FILE = "INVALID_FILE"
    FILE_UPLOAD_FAILED = "FILE_UPLOAD_FAILED"

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    FEATURE_DISABLED = "FEATURE_DISABLED"

    # ------------------------------------------------------------------
    # Workflow
    # ------------------------------------------------------------------

    WORKFLOW_ERROR = "WORKFLOW_ERROR"
    INVALID_STATE = "INVALID_STATE"

    # ------------------------------------------------------------------
    # Integration
    # ------------------------------------------------------------------

    INTEGRATION_ERROR = "INTEGRATION_ERROR"

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    AUDIT_ERROR = "AUDIT_ERROR"


SUPPORTED_ERROR_CODES: Final[tuple[str, ...]] = tuple(code.value for code in ErrorCode)

CLIENT_ERROR_CODES: Final[frozenset[str]] = frozenset(
    {
        ErrorCode.BAD_REQUEST.value,
        ErrorCode.VALIDATION_ERROR.value,
        ErrorCode.INVALID_INPUT.value,
        ErrorCode.INVALID_REQUEST.value,
        ErrorCode.UNAUTHENTICATED.value,
        ErrorCode.PERMISSION_DENIED.value,
        ErrorCode.RESOURCE_NOT_FOUND.value,
        ErrorCode.RESOURCE_ALREADY_EXISTS.value,
        ErrorCode.RESOURCE_CONFLICT.value,
    }
)

SERVER_ERROR_CODES: Final[frozenset[str]] = frozenset(
    {
        ErrorCode.INTERNAL_SERVER_ERROR.value,
        ErrorCode.SERVICE_UNAVAILABLE.value,
        ErrorCode.DATABASE_ERROR.value,
        ErrorCode.CACHE_ERROR.value,
        ErrorCode.EXTERNAL_SERVICE_ERROR.value,
        ErrorCode.AUDIT_ERROR.value,
    }
)

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "ErrorCode",
)
