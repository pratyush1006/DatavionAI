"""Immutable Revenue Cycle monetary value object."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from apps.revenue_cycle.exceptions import RevenueCycleValidationError
from apps.revenue_cycle.foundation.currency import validate_currency

QUANTUM = Decimal("0.01")


@dataclass(frozen=True, slots=True)
class Money:
    """Represent a validated non-negative monetary value."""

    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        """Normalize and validate the monetary value."""
        amount = Decimal(str(self.amount)).quantize(
            QUANTUM,
            rounding=ROUND_HALF_UP,
        )
        currency = validate_currency(self.currency)

        if not amount.is_finite():
            raise RevenueCycleValidationError("Money amount must be finite.")

        if amount < Decimal("0"):
            raise RevenueCycleValidationError("Money amount cannot be negative.")

        object.__setattr__(self, "amount", amount)
        object.__setattr__(self, "currency", currency)

    def add(self, other: Money) -> Money:
        """Return the sum of two same-currency values."""
        self._ensure_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: Money) -> Money:
        """Return a non-negative difference."""
        self._ensure_currency(other)
        result = self.amount - other.amount

        if result < Decimal("0"):
            raise RevenueCycleValidationError("Money subtraction cannot be negative.")

        return Money(result, self.currency)

    def _ensure_currency(self, other: Money) -> None:
        """Ensure both values use the same currency."""
        if self.currency != other.currency:
            raise RevenueCycleValidationError(
                "Money values must use the same currency."
            )


__all__ = ("Money",)
