"""Domain exceptions for patient emergency management."""

from __future__ import annotations


class EmergencyError(Exception):
    """Base exception for patient emergency operations."""


class EmergencyNotFoundError(EmergencyError):
    """Raised when an emergency record cannot be found."""


class EmergencyValidationError(EmergencyError):
    """Raised when emergency data violates a domain invariant."""


class EmergencyPolicyError(EmergencyError):
    """Raised when an actor is not authorized for an operation."""


__all__ = (
    "EmergencyError",
    "EmergencyNotFoundError",
    "EmergencyPolicyError",
    "EmergencyValidationError",
)
