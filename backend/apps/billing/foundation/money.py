"""Immutable Decimal-based money value object."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from .currency import DEFAULT_CURRENCY, normalize_currency


@dataclass(frozen=True, slots=True)
class Money:
    """Represent a monetary amount with explicit currency."""

    amount: Decimal
    currency: str = DEFAULT_CURRENCY

    def __post_init__(self) -> None:
        """Normalize amount and currency."""
        object.__setattr__(self, "amount", Decimal(str(self.amount)))
        object.__setattr__(self, "currency", normalize_currency(self.currency))

    def _require_same_currency(self, other: Self) -> None:
        """Require matching currencies."""
        if self.currency != other.currency:
            raise ValueError("Cannot perform monetary arithmetic across currencies.")

    def add(self, other: Self) -> Self:
        """Add two same-currency amounts."""
        self._require_same_currency(other)
        return Self(self.amount + other.amount, self.currency)

    def subtract(self, other: Self) -> Self:
        """Subtract two same-currency amounts."""
        self._require_same_currency(other)
        return Self(self.amount - other.amount, self.currency)

    def multiply(self, factor: int | Decimal) -> Self:
        """Multiply an amount by a numeric factor."""
        return Self(self.amount * Decimal(str(factor)), self.currency)

    def is_zero(self) -> bool:
        """Return whether amount is zero."""
        return self.amount == Decimal("0")

    def is_positive(self) -> bool:
        """Return whether amount is positive."""
        return self.amount > Decimal("0")

    def is_negative(self) -> bool:
        """Return whether amount is negative."""
        return self.amount < Decimal("0")


ZERO_MONEY = Money(Decimal("0"))
__all__ = ["Money", "ZERO_MONEY"]
