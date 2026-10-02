"""
Core business exceptions for the Datavion AI platform.
"""

from __future__ import annotations

from rest_framework import status

from apps.common.exceptions import (
    DatavionException,
    ErrorCode,
)


class BusinessRuleViolation(
    DatavionException,
):
    """
    Base exception for business rule violations.

    Used when a domain rule, business invariant,
    or application policy prevents an operation.
    """

    code = ErrorCode.BUSINESS_RULE_VIOLATION
    default_message = "A business rule was violated."
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidWorkflowTransition(
    BusinessRuleViolation,
):
    """
    Raised when an invalid workflow transition is attempted.
    """

    code = ErrorCode.INVALID_STATE
    default_message = "Invalid workflow transition."


class DuplicateResourceError(
    BusinessRuleViolation,
):
    """
    Raised when attempting to create an existing resource.
    """

    code = ErrorCode.RESOURCE_ALREADY_EXISTS
    default_message = "Resource already exists."
    status_code = status.HTTP_409_CONFLICT


class ResourceNotEditable(
    BusinessRuleViolation,
):
    """
    Raised when attempting to modify a non-editable resource.
    """

    code = ErrorCode.OPERATION_NOT_ALLOWED
    default_message = "Resource cannot be modified."


class ResourceArchivedError(
    BusinessRuleViolation,
):
    """
    Raised when attempting to access or modify an archived resource.
    """

    code = ErrorCode.RESOURCE_ARCHIVED
    default_message = "Resource has been archived."
    status_code = status.HTTP_409_CONFLICT


class PermissionDeniedError(
    BusinessRuleViolation,
):
    """
    Raised when user permission is insufficient.
    """

    code = ErrorCode.PERMISSION_DENIED
    default_message = "You do not have permission to perform this operation."
    status_code = status.HTTP_403_FORBIDDEN


__all__ = [
    "BusinessRuleViolation",
    "DuplicateResourceError",
    "InvalidWorkflowTransition",
    "PermissionDeniedError",
    "ResourceArchivedError",
    "ResourceNotEditable",
]
