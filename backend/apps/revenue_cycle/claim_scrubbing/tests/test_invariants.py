"""Claim Scrubbing domain invariants."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.revenue_cycle.claim_scrubbing.models import ClaimScrub


class ClaimScrubbingInvariantTests(SimpleTestCase):
    """Verify non-negotiable Claim Scrubbing invariants."""

    def test_canonical_patient_reference(self) -> None:
        """Ensure the aggregate points to canonical patient_core.Patient."""

        field = ClaimScrub._meta.get_field("patient")
        self.assertEqual(
            field.remote_field.model._meta.label,
            "patient_core.Patient",
        )


__all__ = ("ClaimScrubbingInvariantTests",)
