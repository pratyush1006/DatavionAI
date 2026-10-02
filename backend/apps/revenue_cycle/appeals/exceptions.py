"""
Domain exceptions for Revenue Cycle Appeals.
"""

from __future__ import annotations


class AppealError(Exception):
    """Base exception for appeal domain errors."""


class AppealNotFoundError(AppealError):
    """Raised when an appeal is not found in the active tenant scope."""


class InvalidAppealTransition(AppealError):
    """Raised when an appeal lifecycle transition is invalid."""


class AppealInvariantError(AppealError):
    """Raised when an appeal invariant is violated."""


__all__ = (
    "AppealError",
    "AppealInvariantError",
    "AppealNotFoundError",
    "InvalidAppealTransition",
)
