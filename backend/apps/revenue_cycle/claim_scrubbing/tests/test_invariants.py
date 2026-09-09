"""Invariant tests for claim scrubbing."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.claim_scrubbing.constants import ScrubStatus


class ClaimScrubbingInvariantTests(SimpleTestCase):
    """Verify core lifecycle invariants without requiring migrations."""

    def test_lifecycle_states_are_explicit(self):
        """Ensure the supported scrub states remain stable."""

        self.assertEqual(
            {choice for choice, _ in ScrubStatus.choices},
            {"pending", "running", "passed", "failed", "overridden"},
        )

    def test_canonical_patient_reference(self):
        """Ensure the aggregate declares the canonical patient model."""

        from apps.revenue_cycle.claim_scrubbing.models import ClaimScrub

        self.assertEqual(
            ClaimScrub._meta.get_field("patient").remote_field.model,
            "patient_core.Patient",
        )


__all__ = ("ClaimScrubbingInvariantTests",)
