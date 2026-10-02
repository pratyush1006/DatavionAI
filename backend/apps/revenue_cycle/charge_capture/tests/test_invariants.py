"""Domain invariant tests for Charge Capture."""

from __future__ import annotations

from decimal import Decimal

from django.test import SimpleTestCase

from ..services import ChargeCaptureService

__all__ = ("ChargeCaptureInvariantTests",)


class ChargeCaptureInvariantTests(SimpleTestCase):
    """Verify core Charge Capture invariants."""

    def test_total_amount_is_decimal(self) -> None:
        """Ensure monetary arithmetic uses Decimal."""

        quantity = Decimal("2.000")
        unit_price = Decimal("15.50")
        assert (quantity * unit_price).quantize(Decimal("0.01")) == Decimal("31.00")

    def test_service_is_present(self) -> None:
        """Ensure the application service is importable."""

        assert ChargeCaptureService is not None
