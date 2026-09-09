"""Domain exceptions for ERA processing."""

from __future__ import annotations


class ERAError(Exception):
    """Base exception for ERA domain failures."""


class ERAValidationError(ERAError):
    """Raised when ERA data violates a domain invariant."""


class InvalidERATransition(ERAError):
    """Raised when an ERA lifecycle transition is invalid."""


__all__ = ("ERAError", "ERAValidationError", "InvalidERATransition")
