"""Exceptions for the Patient Documents bounded context."""

from __future__ import annotations


class PatientDocumentError(Exception):
    """Base exception for Patient Documents."""


class PatientDocumentNotFoundError(PatientDocumentError):
    """Raised when a patient document cannot be resolved."""


class PatientDocumentValidationError(PatientDocumentError):
    """Raised when a patient document violates a domain rule."""


__all__ = (
    "PatientDocumentError",
    "PatientDocumentNotFoundError",
    "PatientDocumentValidationError",
)
