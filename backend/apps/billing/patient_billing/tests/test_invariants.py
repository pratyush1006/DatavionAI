"""Patient Billing aggregate invariant tests."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.billing.patient_billing.services.responsibility import (
    validate_responsibility_allocation,
)


def _record(
    *,
    party_type: str,
    percentage: str,
    effective_from: date,
    effective_to: date | None = None,
    guarantor_id: object | None = None,
) -> SimpleNamespace:
    """Build a minimal responsibility record for pure invariant testing."""

    return SimpleNamespace(
        party_type=party_type,
        percentage=Decimal(percentage),
        effective_from=effective_from,
        effective_to=effective_to,
        guarantor_id=guarantor_id,
    )


class PatientBillingResponsibilityInvariantTests(SimpleTestCase):
    """Verify financial responsibility allocation invariants."""

    def test_allocations_may_total_one_hundred_percent(self) -> None:
        """Allow a complete allocation across different parties."""

        validate_responsibility_allocation(
            (
                _record(
                    party_type="SELF",
                    percentage="50.00",
                    effective_from=date(2026, 1, 1),
                ),
                _record(
                    party_type="INSURANCE",
                    percentage="50.00",
                    effective_from=date(2026, 1, 1),
                ),
            )
        )

    def test_allocations_cannot_exceed_one_hundred_percent(self) -> None:
        """Reject overlapping allocations above one hundred percent."""

        with self.assertRaises(ValidationError):
            validate_responsibility_allocation(
                (
                    _record(
                        party_type="SELF",
                        percentage="60.00",
                        effective_from=date(2026, 1, 1),
                    ),
                    _record(
                        party_type="INSURANCE",
                        percentage="50.00",
                        effective_from=date(2026, 1, 1),
                    ),
                )
            )

    def test_same_party_cannot_have_overlapping_periods(self) -> None:
        """Reject overlapping responsibility periods for the same payer."""

        with self.assertRaises(ValidationError):
            validate_responsibility_allocation(
                (
                    _record(
                        party_type="SELF",
                        percentage="100.00",
                        effective_from=date(2026, 1, 1),
                        effective_to=date(2026, 3, 31),
                    ),
                    _record(
                        party_type="SELF",
                        percentage="100.00",
                        effective_from=date(2026, 3, 1),
                        effective_to=date(2026, 6, 30),
                    ),
                )
            )

    def test_non_overlapping_periods_are_valid(self) -> None:
        """Allow sequential responsibility periods for the same payer."""

        validate_responsibility_allocation(
            (
                _record(
                    party_type="SELF",
                    percentage="100.00",
                    effective_from=date(2026, 1, 1),
                    effective_to=date(2026, 3, 31),
                ),
                _record(
                    party_type="SELF",
                    percentage="100.00",
                    effective_from=date(2026, 4, 1),
                ),
            )
        )


__all__ = ("PatientBillingResponsibilityInvariantTests",)
