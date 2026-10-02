"""Invariant tests for claim submission lifecycle."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.claim_submission.constants import SubmissionStatus
from apps.revenue_cycle.claim_submission.services import ALLOWED_TRANSITIONS


class ClaimSubmissionInvariantTests(SimpleTestCase):
    """Verify explicit lifecycle invariants."""

    def test_terminal_states_have_no_transitions(self):
        """Ensure accepted, rejected, and cancelled are terminal."""

        self.assertEqual(ALLOWED_TRANSITIONS[SubmissionStatus.ACCEPTED], set())
        self.assertEqual(ALLOWED_TRANSITIONS[SubmissionStatus.REJECTED], set())
        self.assertEqual(ALLOWED_TRANSITIONS[SubmissionStatus.CANCELLED], set())

    def test_submission_states_are_complete(self):
        """Ensure all declared states have transition definitions."""

        states = {value for value, _ in SubmissionStatus.choices}
        self.assertEqual(states, set(ALLOWED_TRANSITIONS))


__all__ = ("ClaimSubmissionInvariantTests",)
