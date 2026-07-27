"""
Custom exceptions for the Patient Consents module.
"""

from __future__ import annotations

from apps.common.exceptions import DatavionException
from apps.common.exceptions.codes import ErrorCode


class ConsentError(DatavionException):
    """
    Base consent exception.
    """

    default_code = ErrorCode.VALIDATION_ERROR
    default_detail = "Consent operation failed."


class DuplicateConsentError(ConsentError):
    """
    Raised when a duplicate consent exists.
    """

    default_detail = "An active consent already exists."


class ConsentExpiredError(ConsentError):
    """
    Raised when a consent has expired.
    """

    default_detail = "The consent has expired."


class ConsentRevokedError(ConsentError):
    """
    Raised when a consent has been revoked.
    """

    default_detail = "The consent has been revoked."


class InvalidConsentError(ConsentError):
    """
    Raised when a consent is invalid.
    """

    default_detail = "The consent is invalid."


__all__ = [
    "ConsentError",
    "ConsentExpiredError",
    "ConsentRevokedError",
    "DuplicateConsentError",
    "InvalidConsentError",
]
