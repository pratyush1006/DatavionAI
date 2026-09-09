"""Revenue Cycle domain exceptions."""

from __future__ import annotations


class RevenueCycleError(Exception):
    """Base Revenue Cycle exception."""


class RevenueCycleValidationError(RevenueCycleError):
    """Raised for domain validation failures."""


class RevenueCycleAuthorizationError(RevenueCycleError):
    """Raised for authorization failures."""


class RevenueCycleTenantContextError(RevenueCycleError):
    """Raised for tenant or organization context failures."""


class RevenueCycleConcurrencyError(RevenueCycleError):
    """Raised for concurrency failures."""


class RevenueCycleIdempotencyError(RevenueCycleError):
    """Raised for idempotency failures."""


__all__ = (
    "RevenueCycleError",
    "RevenueCycleValidationError",
    "RevenueCycleAuthorizationError",
    "RevenueCycleTenantContextError",
    "RevenueCycleConcurrencyError",
    "RevenueCycleIdempotencyError",
)
