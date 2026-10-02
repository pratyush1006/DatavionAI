"""Insurance Verification domain exceptions."""

from __future__ import annotations


class InsuranceVerificationError(Exception):
    """Base Insurance Verification exception."""


class InsuranceVerificationInvariantError(InsuranceVerificationError):
    """Raised when a verification invariant is violated."""


class InsuranceVerificationTransitionError(InsuranceVerificationError):
    """Raised when an invalid lifecycle transition is requested."""


__all__ = (
    "InsuranceVerificationError",
    "InsuranceVerificationInvariantError",
    "InsuranceVerificationTransitionError",
)
