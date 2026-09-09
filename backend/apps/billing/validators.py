"""
Billing Core validation helpers.
"""

from __future__ import annotations

from decimal import Decimal

from apps.billing.exceptions import BillingFinancialInvariantError


def validate_invoice_amounts(
    *,
    total_amount: Decimal,
    paid_amount: Decimal,
    balance_amount: Decimal,
) -> None:
    """Validate the invoice financial equation."""
    if total_amount < Decimal("0.00"):
        raise BillingFinancialInvariantError(
            "Invoice total cannot be negative.",
        )
    if paid_amount < Decimal("0.00"):
        raise BillingFinancialInvariantError(
            "Invoice paid amount cannot be negative.",
        )
    if paid_amount > total_amount:
        raise BillingFinancialInvariantError(
            "Invoice paid amount cannot exceed invoice total.",
        )
    if balance_amount != total_amount - paid_amount:
        raise BillingFinancialInvariantError(
            "Invoice balance must equal total minus paid amount.",
        )


__all__ = ("validate_invoice_amounts",)
