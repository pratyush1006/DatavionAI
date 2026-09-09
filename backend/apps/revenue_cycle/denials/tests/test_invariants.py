"""Denial lifecycle invariant tests."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.denials.constants import DENIAL_TRANSITIONS, DenialStatus


class DenialLifecycleInvariantTests(SimpleTestCase):
    """Protect terminal lifecycle invariants."""

    def test_terminal_states_are_terminal(self):
        """Resolved and written-off states have no outgoing transitions."""
        self.assertEqual(DENIAL_TRANSITIONS[DenialStatus.RESOLVED], set())
        self.assertEqual(DENIAL_TRANSITIONS[DenialStatus.WRITTEN_OFF], set())


__all__ = ("DenialLifecycleInvariantTests",)
