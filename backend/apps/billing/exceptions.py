"""
Billing Core domain exceptions.
"""

from __future__ import annotations


class BillingError(Exception):
    """Base Billing Core exception."""


class BillingNotFoundError(BillingError):
    """Requested tenant-scoped record does not exist."""


class BillingValidationError(BillingError):
    """Billing domain validation failure."""


class BillingOrganizationError(BillingValidationError):
    """Related records cross an organization boundary."""


class BillingFinancialInvariantError(BillingValidationError):
    """Financial aggregate invariant was violated."""


class BillingLifecycleError(BillingValidationError):
    """Invalid financial lifecycle transition."""


__all__ = (
    "BillingError",
    "BillingFinancialInvariantError",
    "BillingLifecycleError",
    "BillingNotFoundError",
    "BillingOrganizationError",
    "BillingValidationError",
)
