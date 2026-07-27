# apps/patient_management/identifiers/exceptions.py

"""
Custom exceptions for the Identifiers module.
"""

from __future__ import annotations

from apps.common.exceptions import DatavionException
from apps.common.exceptions.codes import ErrorCode


class IdentifierError(DatavionException):
    """Base exception for identifier errors."""

    default_code = ErrorCode.VALIDATION_ERROR
    default_detail = "Identifier operation failed."


class DuplicateIdentifierError(IdentifierError):
    """Raised when an identifier already exists."""

    default_detail = "An identifier with the same type and value already exists."


class PrimaryIdentifierExistsError(IdentifierError):
    """Raised when another primary identifier already exists."""

    default_detail = "A primary identifier already exists for this identifier type."


class IdentifierExpiredError(IdentifierError):
    """Raised when an identifier has expired."""

    default_detail = "The identifier has expired."


class IdentifierVerificationError(IdentifierError):
    """Raised when identifier verification fails."""

    default_detail = "Identifier verification failed."


class IdentifierNotVerifiedError(IdentifierError):
    """Raised when a verified identifier is required."""

    default_detail = "The identifier has not been verified."


__all__ = [
    "DuplicateIdentifierError",
    "IdentifierError",
    "IdentifierExpiredError",
    "IdentifierNotVerifiedError",
    "IdentifierVerificationError",
    "PrimaryIdentifierExistsError",
]
