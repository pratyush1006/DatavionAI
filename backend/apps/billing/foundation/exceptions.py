"""Billing domain exceptions."""

from __future__ import annotations


class BillingDomainError(Exception):
    """Base Billing domain failure."""


class BillingConfigurationError(BillingDomainError):
    """Invalid Billing configuration."""


class BillingIntegrityError(BillingDomainError):
    """A financial invariant would be violated."""


class BillingNotFoundError(BillingDomainError):
    """A required Billing aggregate was not found."""


class BillingPermissionError(BillingDomainError):
    """A Billing operation is unauthorized."""


class BillingStateError(BillingDomainError):
    """A financial state transition is invalid."""


class BillingValidationError(BillingDomainError):
    """Billing domain validation failed."""


__all__ = [
    "BillingConfigurationError",
    "BillingDomainError",
    "BillingIntegrityError",
    "BillingNotFoundError",
    "BillingPermissionError",
    "BillingStateError",
    "BillingValidationError",
]
