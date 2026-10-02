"""Domain exceptions for payment posting."""

from __future__ import annotations


class PaymentPostingError(Exception):
    """Base exception for payment posting domain failures."""


class InvalidPaymentPostingTransition(PaymentPostingError):
    """Raised when a payment posting lifecycle transition is invalid."""


class PaymentPostingValidationError(PaymentPostingError):
    """Raised when payment posting data violates a domain invariant."""


class PaymentPostingNotFound(PaymentPostingError):
    """Raised when a payment posting cannot be found in tenant scope."""


__all__ = (
    "InvalidPaymentPostingTransition",
    "PaymentPostingError",
    "PaymentPostingNotFound",
    "PaymentPostingValidationError",
)
