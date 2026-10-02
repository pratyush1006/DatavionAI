"""Domain exceptions for claim scrubbing."""

from __future__ import annotations


class ClaimScrubbingError(Exception):
    """Base exception for claim scrubbing failures."""


class InvalidScrubTransition(ClaimScrubbingError):
    """Raised when a scrub lifecycle transition is invalid."""


class ScrubRuleError(ClaimScrubbingError):
    """Raised when a scrub rule is invalid."""


__all__ = ("ClaimScrubbingError", "InvalidScrubTransition", "ScrubRuleError")
