"""Revenue Cycle currency definitions."""

from __future__ import annotations

from enum import StrEnum

from apps.revenue_cycle.exceptions import RevenueCycleValidationError


class Currency(StrEnum):
    """Supported accounting currencies."""

    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


SUPPORTED_CURRENCIES = tuple(currency.value for currency in Currency)


def validate_currency(value: str) -> str:
    """Validate and normalize a supported currency."""
    normalized = str(value).strip().upper()

    if normalized not in SUPPORTED_CURRENCIES:
        raise RevenueCycleValidationError(f"Unsupported currency: {normalized}.")

    return normalized


__all__ = (
    "Currency",
    "SUPPORTED_CURRENCIES",
    "validate_currency",
)
