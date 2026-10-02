"""
DatavionAI Exception Messages.

Centralized default error messages used throughout the DatavionAI platform.

Design Principles
-----------------
- Framework agnostic
- Immutable
- Human readable
- Overrideable by exception classes
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

from .codes import ErrorCode

###############################################################################
# Default Error Messages
###############################################################################

DEFAULT_ERROR_MESSAGE: Final[str] = "An unexpected error occurred."

ERROR_MESSAGES: Final[MappingProxyType[ErrorCode, str]] = MappingProxyType(
    {
        # ------------------------------------------------------------------
        # Generic
        # ------------------------------------------------------------------
        ErrorCode.UNKNOWN_ERROR: "An unknown error occurred.",
        ErrorCode.INTERNAL_SERVER_ERROR: "An internal server error occurred.",
        ErrorCode.SERVICE_UNAVAILABLE: "The service is temporarily unavailable.",
        ErrorCode.NOT_IMPLEMENTED: "This feature is not implemented.",
        # ------------------------------------------------------------------
        # Request
        # ------------------------------------------------------------------
        ErrorCode.BAD_REQUEST: "The request is invalid.",
        ErrorCode.VALIDATION_ERROR: "Validation failed.",
        ErrorCode.INVALID_INPUT: "Invalid input provided.",
        ErrorCode.INVALID_REQUEST: "The request is invalid.",
        ErrorCode.MALFORMED_REQUEST: "The request payload is malformed.",
        ErrorCode.UNSUPPORTED_MEDIA_TYPE: "Unsupported media type.",
        # ------------------------------------------------------------------
        # Authentication
        # ------------------------------------------------------------------
        ErrorCode.UNAUTHENTICATED: "Authentication is required.",
        ErrorCode.INVALID_CREDENTIALS: "Invalid credentials.",
        ErrorCode.ACCOUNT_LOCKED: "The account is locked.",
        ErrorCode.ACCOUNT_DISABLED: "The account is disabled.",
        ErrorCode.ACCOUNT_INACTIVE: "The account is inactive.",
        ErrorCode.TOKEN_EXPIRED: "Authentication token has expired.",
        ErrorCode.TOKEN_INVALID: "Authentication token is invalid.",
        ErrorCode.TOKEN_REVOKED: "Authentication token has been revoked.",
        ErrorCode.MFA_REQUIRED: "Multi-factor authentication is required.",
        ErrorCode.MFA_INVALID: "Invalid multi-factor authentication code.",
        # ------------------------------------------------------------------
        # Authorization
        # ------------------------------------------------------------------
        ErrorCode.PERMISSION_DENIED: "Permission denied.",
        ErrorCode.ACCESS_DENIED: "Access denied.",
        ErrorCode.FORBIDDEN: "You do not have permission to perform this action.",
        # ------------------------------------------------------------------
        # Resources
        # ------------------------------------------------------------------
        ErrorCode.RESOURCE_NOT_FOUND: "Requested resource was not found.",
        ErrorCode.RESOURCE_ALREADY_EXISTS: "Resource already exists.",
        ErrorCode.RESOURCE_CONFLICT: "Resource conflict detected.",
        ErrorCode.RESOURCE_LOCKED: "Resource is locked.",
        ErrorCode.RESOURCE_ARCHIVED: "Resource has been archived.",
        # ------------------------------------------------------------------
        # Business Rules
        # ------------------------------------------------------------------
        ErrorCode.BUSINESS_RULE_VIOLATION: "Business rule violation.",
        ErrorCode.OPERATION_NOT_ALLOWED: "Operation is not allowed.",
        ErrorCode.PRECONDITION_FAILED: "Precondition failed.",
        # ------------------------------------------------------------------
        # Organization / Tenant
        # ------------------------------------------------------------------
        ErrorCode.ORGANIZATION_NOT_FOUND: "Organization not found.",
        ErrorCode.TENANT_NOT_FOUND: "Tenant not found.",
        ErrorCode.TENANT_MISMATCH: "Tenant mismatch detected.",
        # ------------------------------------------------------------------
        # Database
        # ------------------------------------------------------------------
        ErrorCode.DATABASE_ERROR: "Database operation failed.",
        ErrorCode.DATABASE_TIMEOUT: "Database operation timed out.",
        ErrorCode.DATABASE_CONSTRAINT_ERROR: "Database constraint violation.",
        # ------------------------------------------------------------------
        # Cache
        # ------------------------------------------------------------------
        ErrorCode.CACHE_ERROR: "Cache operation failed.",
        ErrorCode.CACHE_TIMEOUT: "Cache operation timed out.",
        # ------------------------------------------------------------------
        # External Services
        # ------------------------------------------------------------------
        ErrorCode.EXTERNAL_SERVICE_ERROR: "External service error.",
        ErrorCode.EXTERNAL_SERVICE_TIMEOUT: "External service timed out.",
        # ------------------------------------------------------------------
        # Rate Limiting
        # ------------------------------------------------------------------
        ErrorCode.RATE_LIMIT_EXCEEDED: "Rate limit exceeded.",
        # ------------------------------------------------------------------
        # Files
        # ------------------------------------------------------------------
        ErrorCode.FILE_NOT_FOUND: "File not found.",
        ErrorCode.FILE_TOO_LARGE: "File exceeds the allowed size.",
        ErrorCode.INVALID_FILE: "Invalid file.",
        ErrorCode.FILE_UPLOAD_FAILED: "File upload failed.",
        # ------------------------------------------------------------------
        # Configuration
        # ------------------------------------------------------------------
        ErrorCode.CONFIGURATION_ERROR: "Configuration error.",
        ErrorCode.FEATURE_DISABLED: "This feature is currently disabled.",
        # ------------------------------------------------------------------
        # Workflow
        # ------------------------------------------------------------------
        ErrorCode.WORKFLOW_ERROR: "Workflow execution failed.",
        ErrorCode.INVALID_STATE: "Invalid workflow state.",
        # ------------------------------------------------------------------
        # Integration
        # ------------------------------------------------------------------
        ErrorCode.INTEGRATION_ERROR: "Integration failed.",
        # ------------------------------------------------------------------
        # Audit
        # ------------------------------------------------------------------
        ErrorCode.AUDIT_ERROR: "Audit operation failed.",
    }
)

###############################################################################
# Helper Functions
###############################################################################


def get_error_message(
    code: ErrorCode,
) -> str:
    """
    Return the default message for an error code.
    """

    return ERROR_MESSAGES.get(
        code,
        DEFAULT_ERROR_MESSAGE,
    )


###############################################################################
# Public Exports
###############################################################################

__all__ = (
    "DEFAULT_ERROR_MESSAGE",
    "ERROR_MESSAGES",
    "get_error_message",
)
