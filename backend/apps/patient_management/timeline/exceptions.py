"""
Domain exceptions for Patient Timeline.
"""

from __future__ import annotations


class TimelineError(Exception):
    """Base exception for Timeline domain errors."""


class TimelineNotFoundError(TimelineError):
    """Raised when a requested timeline entry cannot be found."""


class TimelineValidationError(TimelineError):
    """Raised when timeline input violates domain rules."""


__all__ = (
    "TimelineError",
    "TimelineNotFoundError",
    "TimelineValidationError",
)
