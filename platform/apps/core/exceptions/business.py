"""
Business exceptions for the Datavion AI platform.
"""

from __future__ import annotations

from apps.core.exceptions.base import DatavionError


class BusinessRuleViolation(
    DatavionError,
):
    """
    Raised when a business rule is violated.
    """


class InvalidWorkflowTransition(
    BusinessRuleViolation,
):
    """
    Raised when an invalid workflow transition is attempted.
    """


class DuplicateResourceError(
    BusinessRuleViolation,
):
    """
    Raised when attempting to create a duplicate resource.
    """


class ResourceNotEditable(
    BusinessRuleViolation,
):
    """
    Raised when attempting to modify a non-editable resource.
    """


__all__ = [
    "BusinessRuleViolation",
    "DuplicateResourceError",
    "InvalidWorkflowTransition",
    "ResourceNotEditable",
]
