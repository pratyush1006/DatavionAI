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
    Raised when a business rule is violated.
    """

    error_code = ErrorCode.VALIDATION_ERROR
    default_message = "A business rule was violated."
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidWorkflowTransition(
    BusinessRuleViolation,
):
    """
    Raised when an invalid workflow transition is attempted.
    """

    default_message = "Invalid workflow transition."


class DuplicateResourceError(
    BusinessRuleViolation,
):
    """
    Raised when attempting to create a duplicate resource.
    """

    error_code = ErrorCode.DUPLICATE_RESOURCE
    default_message = "Resource already exists."
    status_code = status.HTTP_409_CONFLICT


class ResourceNotEditable(
    BusinessRuleViolation,
):
    """
    Raised when attempting to modify a non-editable resource.
    """

    default_message = "Resource cannot be modified."


__all__ = [
    "BusinessRuleViolation",
    "DuplicateResourceError",
    "InvalidWorkflowTransition",
    "ResourceNotEditable",
]
