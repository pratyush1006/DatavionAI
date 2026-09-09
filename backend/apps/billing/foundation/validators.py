"""Shared Billing validation helpers."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

from .currency import normalize_currency
from .exceptions import BillingValidationError


def validate_currency(currency: str) -> str:
    """Validate and normalize a currency code."""
    try:
        return normalize_currency(currency)
    except ValueError as exc:
        raise BillingValidationError(str(exc)) from exc


def validate_money_amount(
    value: Any, *, field_name: str = "amount", allow_zero: bool = True
) -> Decimal:
    """Validate a finite non-negative Decimal amount."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise BillingValidationError(
            f"{field_name} must be a valid decimal amount."
        ) from exc
    if not amount.is_finite() or amount < Decimal("0"):
        raise BillingValidationError(f"{field_name} must be finite and non-negative.")
    if not allow_zero and amount == Decimal("0"):
        raise BillingValidationError(f"{field_name} must be greater than zero.")
    return amount


def validate_positive_quantity(value: Any, *, field_name: str = "quantity") -> int:
    """Validate a positive integer quantity."""
    if isinstance(value, bool):
        raise BillingValidationError(f"{field_name} must be a positive integer.")
    try:
        quantity = int(value)
    except (TypeError, ValueError) as exc:
        raise BillingValidationError(
            f"{field_name} must be a positive integer."
        ) from exc
    if quantity <= 0:
        raise BillingValidationError(f"{field_name} must be a positive integer.")
    return quantity


__all__ = ["validate_currency", "validate_money_amount", "validate_positive_quantity"]
