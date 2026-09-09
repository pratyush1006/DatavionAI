"""
Domain exceptions for Patient Portal.
"""

from __future__ import annotations


class PatientPortalError(Exception):
    """Base exception for Patient Portal operations."""


class PortalLifecycleError(PatientPortalError):
    """Raised when an account lifecycle transition is invalid."""


class PortalOrganizationError(PatientPortalError):
    """Raised when an account violates organization or tenant boundaries."""


__all__ = (
    "PatientPortalError",
    "PortalLifecycleError",
    "PortalOrganizationError",
)
