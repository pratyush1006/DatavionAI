"""Domain exceptions for claim submission."""

from __future__ import annotations


class ClaimSubmissionError(Exception):
    """Base exception for claim submission failures."""


class InvalidSubmissionTransition(ClaimSubmissionError):
    """Raised when a submission lifecycle transition is invalid."""


class SubmissionValidationError(ClaimSubmissionError):
    """Raised when a claim cannot be submitted."""


__all__ = (
    "ClaimSubmissionError",
    "InvalidSubmissionTransition",
    "SubmissionValidationError",
)
