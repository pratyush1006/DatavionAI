"""
Audit exception hierarchy for DatavionOS.

Provides reusable exceptions for the audit framework.
"""

from __future__ import annotations


class AuditError(
    Exception,
):
    """
    Base exception for audit errors.
    """


class AuditConfigurationError(
    AuditError,
):
    """
    Raised when audit configuration is invalid.
    """


class AuditRecordError(
    AuditError,
):
    """
    Raised when an audit record is invalid.
    """


class AuditRecordingError(
    AuditError,
):
    """
    Raised when audit recording fails.
    """


class AuditStorageError(
    AuditRecordingError,
):
    """
    Raised when audit storage operation fails.
    """


class AuditRegistryError(
    AuditError,
):
    """
    Raised when audit registry operation fails.
    """


class AuditAlreadyRegisteredError(
    AuditRegistryError,
):
    """
    Raised when registering an existing audit handler.
    """


class AuditNotFoundError(
    AuditRegistryError,
):
    """
    Raised when an audit handler cannot be found.
    """


class AuditContextError(
    AuditError,
):
    """
    Raised when audit context is invalid.
    """


__all__: tuple[str, ...] = (
    "AuditAlreadyRegisteredError",
    "AuditConfigurationError",
    "AuditContextError",
    "AuditError",
    "AuditNotFoundError",
    "AuditRecordError",
    "AuditRecordingError",
    "AuditRegistryError",
    "AuditStorageError",
)
