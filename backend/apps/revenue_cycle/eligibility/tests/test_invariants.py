"""Eligibility invariant tests."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.eligibility.constants import CoverageStatus, EligibilityStatus
from apps.revenue_cycle.eligibility.services.eligibility import _ALLOWED_TRANSITIONS


class EligibilityInvariantTests(SimpleTestCase):
    """Verify strict Eligibility state invariants."""

    def test_pending_cannot_skip_to_verified(self):
        """Pending requests must enter processing before verification."""
        self.assertNotIn(
            EligibilityStatus.VERIFIED.value,
            _ALLOWED_TRANSITIONS[EligibilityStatus.PENDING.value],
        )

    def test_coverage_status_is_finite(self):
        """Coverage status is a finite canonical set."""
        self.assertEqual(
            {x.value for x in CoverageStatus},
            {"active", "inactive", "unknown", "not_found"},
        )


__all__ = ("EligibilityInvariantTests",)
