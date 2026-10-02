"""Insurance Verification invariant tests."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.insurance_verification.constants import (
    VerificationOutcome,
    VerificationStatus,
)
from apps.revenue_cycle.insurance_verification.services.insurance_verification import (
    _ALLOWED_TRANSITIONS,
)


class InsuranceVerificationInvariantTests(SimpleTestCase):
    """Verify strict Insurance Verification state invariants."""

    def test_pending_cannot_skip_to_verified(self):
        """Pending verification must enter processing first."""

        self.assertNotIn(
            VerificationStatus.VERIFIED.value,
            _ALLOWED_TRANSITIONS[VerificationStatus.PENDING.value],
        )

    def test_inactive_is_terminal(self):
        """Inactive verification cannot transition to another state."""

        self.assertEqual(
            _ALLOWED_TRANSITIONS[VerificationStatus.INACTIVE.value],
            set(),
        )

    def test_outcome_set_is_finite(self):
        """Outcome values remain a finite canonical set."""

        self.assertEqual(
            {item.value for item in VerificationOutcome},
            {"active", "inactive", "not_found", "unknown"},
        )


__all__ = ("InsuranceVerificationInvariantTests",)
