"""Prior Authorization domain exceptions."""

from __future__ import annotations


class PriorAuthorizationError(Exception):
    """Base Prior Authorization exception."""


class PriorAuthorizationInvariantError(PriorAuthorizationError):
    """Raised when a verification invariant is violated."""


class PriorAuthorizationTransitionError(PriorAuthorizationError):
    """Raised when an invalid lifecycle transition is requested."""


__all__ = (
    "PriorAuthorizationError",
    "PriorAuthorizationInvariantError",
    "PriorAuthorizationTransitionError",
)
