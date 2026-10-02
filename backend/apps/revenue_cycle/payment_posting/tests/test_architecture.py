"""Architecture tests for payment posting."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase

BASE = Path(__file__).resolve().parents[1]


class PaymentPostingArchitectureTests(SimpleTestCase):
    """Verify critical Revenue Cycle architecture boundaries."""

    def test_canonical_patient_reference(self) -> None:
        """Ensure payment posting references the canonical Patient model."""

        text = (BASE / "models" / "payment_posting.py").read_text(encoding="utf-8")
        self.assertIn('"patient_core.Patient"', text)
        self.assertNotIn("apps.clinical.patients", text)

    def test_platform_rbac_reference(self) -> None:
        """Ensure authorization delegates to the platform RBAC engine."""

        text = (BASE / "policies.py").read_text(encoding="utf-8")
        self.assertIn("apps.platform.rbac.resolvers", text)

    def test_row_locking_exists(self) -> None:
        """Ensure mutation selectors use database row locking."""

        text = (BASE / "selectors.py").read_text(encoding="utf-8")
        self.assertIn("select_for_update", text)

    def test_after_commit_event_dispatch_exists(self) -> None:
        """Ensure workflows publish events after transaction commit."""

        text = (BASE / "workflows" / "payment_posting.py").read_text(encoding="utf-8")
        self.assertIn("publish_after_commit", text)


__all__ = ("PaymentPostingArchitectureTests",)
