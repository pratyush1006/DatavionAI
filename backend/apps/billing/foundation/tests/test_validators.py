"""Tests for Billing validators."""

from __future__ import annotations

from decimal import Decimal

from django.test import SimpleTestCase

from apps.billing.foundation.exceptions import BillingValidationError
from apps.billing.foundation.validators import (
    validate_money_amount,
    validate_positive_quantity,
)


class BillingValidatorTests(SimpleTestCase):
    """Verify shared validation rules."""

    def test_money_amount(self) -> None:
        """Return Decimal for valid amounts."""
        self.assertEqual(validate_money_amount("125.50"), Decimal("125.50"))

    def test_negative_rejected(self) -> None:
        """Reject negative amounts."""
        with self.assertRaises(BillingValidationError):
            validate_money_amount("-1")

    def test_zero_can_be_disallowed(self) -> None:
        """Reject zero when positive is required."""
        with self.assertRaises(BillingValidationError):
            validate_money_amount("0", allow_zero=False)

    def test_quantity_must_be_positive(self) -> None:
        """Reject non-positive quantity."""
        with self.assertRaises(BillingValidationError):
            validate_positive_quantity(0)


__all__ = ["BillingValidatorTests"]
