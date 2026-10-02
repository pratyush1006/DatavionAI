"""Patient Billing domain exceptions."""

from __future__ import annotations


class PatientBillingError(Exception):
    """Base Patient Billing exception."""


class PatientBillingValidationError(PatientBillingError):
    """Raised when a Patient Billing invariant is violated."""


class PatientBillingLifecycleError(PatientBillingValidationError):
    """Raised for an invalid Patient Billing lifecycle transition."""


class PatientBillingOrganizationError(PatientBillingValidationError):
    """Raised when related records cross an organization boundary."""


__all__ = (
    "PatientBillingError",
    "PatientBillingLifecycleError",
    "PatientBillingOrganizationError",
    "PatientBillingValidationError",
)
