"""Domain exceptions for Patient Preferences."""

from __future__ import annotations


class PatientPreferenceError(Exception):
    """Base exception for Patient Preferences."""


class PreferenceOrganizationError(PatientPreferenceError):
    """Raised when patient and organization boundaries do not match."""


class PreferenceLifecycleError(PatientPreferenceError):
    """Raised when a preference lifecycle operation is invalid."""


class PreferenceValidationError(PatientPreferenceError):
    """Raised when preference data violates domain rules."""


__all__ = (
    "PatientPreferenceError",
    "PreferenceLifecycleError",
    "PreferenceOrganizationError",
    "PreferenceValidationError",
)
