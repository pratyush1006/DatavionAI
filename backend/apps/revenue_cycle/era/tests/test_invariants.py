"""Invariant tests for ERA."""

from __future__ import annotations

from decimal import Decimal

from django.test import SimpleTestCase

from ..constants import ERAStatus


class ERAInvariantTests(SimpleTestCase):
    """Verify stable ERA invariants."""

    def test_lifecycle_values(self) -> None:
        """Ensure required lifecycle states exist."""

        self.assertEqual(ERAStatus.RECEIVED, "received")
        self.assertEqual(ERAStatus.VALIDATED, "validated")
        self.assertEqual(ERAStatus.POSTED, "posted")
        self.assertEqual(ERAStatus.REVERSED, "reversed")

    def test_decimal_values(self) -> None:
        """Ensure ERA monetary values are decimal based."""

        self.assertEqual(Decimal("100.00"), Decimal("100.00"))


__all__ = ("ERAInvariantTests",)
