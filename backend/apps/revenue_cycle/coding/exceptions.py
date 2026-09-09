from __future__ import annotations

"""Domain exceptions for Revenue Cycle Coding."""


class CodingError(Exception):
    """Base exception for Coding domain failures."""


class CodingValidationError(CodingError):
    """Raised when Coding data violates a domain invariant."""


class CodingTransitionError(CodingError):
    """Raised when an invalid Coding lifecycle transition is requested."""


class CodingAuthorizationError(CodingError):
    """Raised when a caller is not authorized for a Coding operation."""


__all__ = (
    "CodingAuthorizationError",
    "CodingError",
    "CodingTransitionError",
    "CodingValidationError",
)
