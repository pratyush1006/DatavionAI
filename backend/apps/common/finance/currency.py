"""
DatavionOS shared currency infrastructure.

Currency is a cross-domain financial primitive and therefore belongs
in the common layer rather than inside Finance, Revenue Cycle, or
SaaS Billing.

Consumers:
    - apps.billing.finance
    - apps.revenue_cycle
    - apps.platform.saas_billing

Design principles:
    - Single canonical currency definition
    - Domain-neutral
    - Deterministic normalization
    - Explicit supported currencies
    - Fixed decimal precision configuration
    - No Django model dependency
    - No dependency on higher-level application domains
"""

from __future__ import annotations

from enum import StrEnum


class Currency(StrEnum):
    """ISO-style currency codes supported by DatavionOS."""

    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


DEFAULT_CURRENCY = Currency.INR.value

SUPPORTED_CURRENCIES = tuple(currency.value for currency in Currency)

CURRENCY_DECIMAL_PLACES = {
    Currency.INR.value: 2,
    Currency.USD.value: 2,
    Currency.EUR.value: 2,
    Currency.GBP.value: 2,
}


def normalize_currency(currency: str) -> str:
    """
    Normalize and validate a currency code.

    Args:
        currency: Currency code supplied by a caller.

    Returns:
        Normalized uppercase currency code.

    Raises:
        ValueError: If the supplied currency is unsupported.
    """
    normalized = str(currency).strip().upper()

    if normalized not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported currency: {currency}")

    return normalized


def validate_currency(currency: str) -> str:
    """
    Validate and normalize a currency code.

    This function is intentionally equivalent to normalize_currency()
    so domain-specific callers can use the terminology most natural
    to their validation layer.
    """
    return normalize_currency(currency)


def decimal_places(currency: str) -> int:
    """
    Return the configured decimal precision for a currency.

    Args:
        currency: Currency code.

    Returns:
        Number of supported decimal places.
    """
    return CURRENCY_DECIMAL_PLACES[normalize_currency(currency)]


__all__ = (
    "Currency",
    "DEFAULT_CURRENCY",
    "SUPPORTED_CURRENCIES",
    "CURRENCY_DECIMAL_PLACES",
    "normalize_currency",
    "validate_currency",
    "decimal_places",
)
