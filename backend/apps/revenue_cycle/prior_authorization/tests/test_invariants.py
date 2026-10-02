"""Prior Authorization invariant tests."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.prior_authorization.constants import (
    AuthorizationOutcome,
    AuthorizationStatus,
)
from apps.revenue_cycle.prior_authorization.services.prior_authorization import (
    _ALLOWED_TRANSITIONS,
)


class PriorAuthorizationInvariantTests(SimpleTestCase):
    """Verify strict Prior Authorization state invariants."""

    def test_pending_cannot_skip_to_approved(self):
        """Pending authorization must enter review before approval."""

        self.assertNotIn(
            AuthorizationStatus.APPROVED.value,
            _ALLOWED_TRANSITIONS[AuthorizationStatus.PENDING.value],
        )

    def test_inactive_is_terminal(self):
        """Inactive authorization cannot transition to another state."""

        self.assertEqual(
            _ALLOWED_TRANSITIONS[AuthorizationStatus.INACTIVE.value],
            set(),
        )

    def test_outcome_set_is_finite(self):
        """Outcome values remain a finite canonical set."""

        self.assertEqual(
            {item.value for item in AuthorizationOutcome},
            {"approved", "denied", "pended", "not_required", "unknown"},
        )


__all__ = ("PriorAuthorizationInvariantTests",)
