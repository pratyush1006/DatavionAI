"""Architecture tests for ERA."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase

BASE = Path(__file__).resolve().parents[1]


class ERAArchitectureTests(SimpleTestCase):
    """Verify critical ERA architecture boundaries."""

    def test_canonical_patient(self) -> None:
        """Ensure ERA references canonical Patient."""

        text = (BASE / "models" / "era.py").read_text(encoding="utf-8")
        self.assertIn('"patient_core.Patient"', text)
        self.assertNotIn("apps.clinical.patients", text)

    def test_platform_rbac(self) -> None:
        """Ensure ERA authorization uses platform RBAC."""

        text = (BASE / "rbac.py").read_text(encoding="utf-8")
        self.assertIn("apps.platform.rbac.resolvers", text)

    def test_tenant_context(self) -> None:
        """Ensure APIs require explicit tenant and organization context."""

        text = (BASE / "tenant.py").read_text(encoding="utf-8")
        self.assertIn("request.tenant", text)
        self.assertIn("request.organization", text)

    def test_row_locking(self) -> None:
        """Ensure mutation selectors use row locking."""

        text = (BASE / "selectors.py").read_text(encoding="utf-8")
        self.assertIn("select_for_update", text)

    def test_after_commit(self) -> None:
        """Ensure workflows publish events after transaction commit."""

        text = (BASE / "workflows" / "era.py").read_text(encoding="utf-8")
        self.assertIn("publish_after_commit", text)


__all__ = ("ERAArchitectureTests",)
