"""Shared Revenue Cycle validators."""

from __future__ import annotations

from decimal import Decimal

from apps.revenue_cycle.exceptions import RevenueCycleValidationError


def validate_non_negative_amount(
    value: Decimal | int | float | str,
) -> Decimal:
    """Validate a finite non-negative amount."""
    amount = Decimal(str(value))

    if not amount.is_finite():
        raise RevenueCycleValidationError("Amount must be finite.")

    if amount < Decimal("0"):
        raise RevenueCycleValidationError("Amount cannot be negative.")

    return amount


def validate_percentage(
    value: Decimal | int | float | str,
) -> Decimal:
    """Validate a percentage from zero through one hundred."""
    percentage = Decimal(str(value))

    if not percentage.is_finite():
        raise RevenueCycleValidationError("Percentage must be finite.")

    if percentage < Decimal("0") or percentage > Decimal("100"):
        raise RevenueCycleValidationError("Percentage must be between 0 and 100.")

    return percentage


__all__ = (
    "validate_non_negative_amount",
    "validate_percentage",
)
