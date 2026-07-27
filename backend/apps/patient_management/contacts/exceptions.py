"""
Custom exceptions for the Contacts module.
"""

from __future__ import annotations

from apps.common.exceptions import DatavionException
from apps.common.exceptions.codes import ErrorCode


class ContactError(DatavionException):
    """Base exception for contact errors."""

    default_code = ErrorCode.VALIDATION_ERROR
    default_detail = "Contact operation failed."


class DuplicateContactError(ContactError):
    """Raised when a duplicate contact exists."""

    default_detail = "A contact with the same type and value already exists."


class PrimaryContactExistsError(ContactError):
    """Raised when a primary contact already exists."""

    default_detail = "A primary contact already exists for this contact type."


class InvalidContactError(ContactError):
    """Raised when contact data is invalid."""

    default_detail = "The contact information is invalid."


class ContactVerificationError(ContactError):
    """Raised when contact verification fails."""

    default_detail = "Contact verification failed."


__all__ = [
    "ContactError",
    "ContactVerificationError",
    "DuplicateContactError",
    "InvalidContactError",
    "PrimaryContactExistsError",
]
