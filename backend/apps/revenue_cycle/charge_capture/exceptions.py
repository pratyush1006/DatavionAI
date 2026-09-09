"""Domain exceptions for Revenue Cycle Charge Capture."""

from __future__ import annotations

__all__ = (
    "ChargeCaptureError",
    "ChargeNotFoundError",
    "ChargeValidationError",
)


class ChargeCaptureError(Exception):
    """Base exception for Charge Capture domain failures."""


class ChargeNotFoundError(ChargeCaptureError):
    """Raised when a requested charge cannot be found."""


class ChargeValidationError(ChargeCaptureError):
    """Raised when a charge violates a domain invariant."""
