"""Architecture tests for claim submission."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class ClaimSubmissionArchitectureTests(SimpleTestCase):
    """Verify critical claim submission architecture boundaries."""

    def test_canonical_patient(self):
        """Ensure the model uses the canonical patient aggregate."""

        source = Path(__file__).resolve().parents[1] / "models" / "claim_submission.py"
        self.assertIn('"patient_core.Patient"', source.read_text(encoding="utf-8"))

    def test_platform_rbac(self):
        """Ensure policy delegates to platform RBAC."""

        source = Path(__file__).resolve().parents[1] / "policies.py"
        self.assertIn(
            "apps.platform.rbac.resolvers", source.read_text(encoding="utf-8")
        )

    def test_row_locking(self):
        """Ensure mutation selectors use row locking."""

        source = Path(__file__).resolve().parents[1] / "selectors.py"
        self.assertIn("select_for_update", source.read_text(encoding="utf-8"))

    def test_after_commit_events(self):
        """Ensure services dispatch events after commit."""

        source = Path(__file__).resolve().parents[1] / "services.py"
        self.assertIn("publish_after_commit", source.read_text(encoding="utf-8"))


__all__ = ("ClaimSubmissionArchitectureTests",)
