"""Tests for Billing money."""

from __future__ import annotations

from decimal import Decimal

from django.test import SimpleTestCase

from apps.billing.foundation.money import Money


class MoneyTests(SimpleTestCase):
    """Verify Decimal money arithmetic."""

    def test_addition(self) -> None:
        """Add same-currency amounts."""
        self.assertEqual(
            Money(Decimal("10")).add(Money(Decimal("2"))).amount, Decimal("12")
        )

    def test_mixed_currency_rejected(self) -> None:
        """Reject mixed-currency arithmetic."""
        with self.assertRaises(ValueError):
            Money(Decimal("10"), "INR").add(Money(Decimal("10"), "USD"))


__all__ = ["MoneyTests"]
