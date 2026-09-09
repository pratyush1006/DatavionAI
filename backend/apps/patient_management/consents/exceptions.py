"""
Patient Consent domain exceptions.

Domain-specific exceptions for consent validation and lifecycle handling.
"""

from __future__ import annotations


class PatientConsentError(Exception):
    """
    Base exception for Patient Consent domain errors.
    """


class PatientConsentValidationError(PatientConsentError):
    """
    Raised when Patient Consent data fails domain validation.
    """


class PatientConsentNotFoundError(PatientConsentError):
    """
    Raised when a requested Patient Consent cannot be found.
    """


__all__ = (
    "PatientConsentError",
    "PatientConsentValidationError",
    "PatientConsentNotFoundError",
)
