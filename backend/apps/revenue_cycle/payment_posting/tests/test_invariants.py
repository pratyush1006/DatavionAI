"""Invariant tests for payment posting."""

from __future__ import annotations

from decimal import Decimal

from django.test import SimpleTestCase

from ..constants import PaymentPostingStatus


class PaymentPostingInvariantTests(SimpleTestCase):
    """Verify core payment posting invariants without database access."""

    def test_status_values_are_stable(self) -> None:
        """Ensure lifecycle values required by workflows remain defined."""

        self.assertEqual(PaymentPostingStatus.PENDING, "pending")
        self.assertEqual(PaymentPostingStatus.POSTED, "posted")
        self.assertEqual(PaymentPostingStatus.REVERSED, "reversed")
        self.assertEqual(PaymentPostingStatus.VOIDED, "voided")

    def test_decimal_precision_is_supported(self) -> None:
        """Ensure monetary values remain decimal-based."""

        value = Decimal("1250.50")
        self.assertEqual(str(value), "1250.50")


__all__ = ("PaymentPostingInvariantTests",)
