"""Eligibility domain exceptions."""

from __future__ import annotations


class EligibilityDomainError(Exception):
    """Base Eligibility exception."""


class EligibilityInvariantError(EligibilityDomainError):
    """Raised when an Eligibility invariant is violated."""


class EligibilityTransitionError(EligibilityDomainError):
    """Raised when an invalid lifecycle transition is requested."""


__all__ = (
    "EligibilityDomainError",
    "EligibilityInvariantError",
    "EligibilityTransitionError",
)
