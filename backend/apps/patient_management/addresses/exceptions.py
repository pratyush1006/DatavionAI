"""
Custom exceptions for the Addresses module.
"""

from __future__ import annotations

from apps.common.exceptions import DatavionException
from apps.common.exceptions.codes import ErrorCode


class AddressError(DatavionException):
    """Base exception for address errors."""

    default_code = ErrorCode.VALIDATION_ERROR
    default_detail = "Address operation failed."


class DuplicateAddressError(AddressError):
    """Raised when a duplicate address exists."""

    default_detail = "An address with the same details already exists."


class PrimaryAddressExistsError(AddressError):
    """Raised when a primary address already exists."""

    default_detail = "A primary address already exists for this address type."


class InvalidAddressError(AddressError):
    """Raised when address data is invalid."""

    default_detail = "The address is invalid."


__all__ = [
    "AddressError",
    "DuplicateAddressError",
    "InvalidAddressError",
    "PrimaryAddressExistsError",
]
