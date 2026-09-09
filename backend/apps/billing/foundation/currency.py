"""Billing currency definitions."""

from __future__ import annotations

DEFAULT_CURRENCY = "INR"
SUPPORTED_CURRENCIES = ("INR", "USD", "EUR", "GBP")
CURRENCY_DECIMAL_PLACES = {"INR": 2, "USD": 2, "EUR": 2, "GBP": 2}


def normalize_currency(currency: str) -> str:
    """Normalize and validate a currency code."""
    normalized = currency.strip().upper()
    if normalized not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported billing currency: {currency}")
    return normalized


def decimal_places(currency: str) -> int:
    """Return configured decimal precision."""
    return CURRENCY_DECIMAL_PLACES[normalize_currency(currency)]


__all__ = [
    "CURRENCY_DECIMAL_PLACES",
    "DEFAULT_CURRENCY",
    "SUPPORTED_CURRENCIES",
    "decimal_places",
    "normalize_currency",
]
