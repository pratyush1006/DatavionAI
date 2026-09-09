"""Patient Communication domain exceptions."""

from __future__ import annotations


class PatientCommunicationError(Exception):
    """Base exception for Patient Communication errors."""


class PatientCommunicationValidationError(PatientCommunicationError):
    """Raised when communication data violates domain rules."""


class PatientCommunicationNotFoundError(PatientCommunicationError):
    """Raised when a communication cannot be found."""


__all__ = (
    "PatientCommunicationError",
    "PatientCommunicationValidationError",
    "PatientCommunicationNotFoundError",
)
