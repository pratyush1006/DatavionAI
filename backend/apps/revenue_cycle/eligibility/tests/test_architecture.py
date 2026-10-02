"""Architecture tests for Revenue Cycle Eligibility."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class EligibilityArchitectureTests(SimpleTestCase):
    """Verify the RC1 architectural contract."""

    def test_canonical_patient(self):
        """Eligibility must use the canonical Patient module."""
        source = Path("apps/revenue_cycle/eligibility/models/eligibility.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("apps.patient_management.patients.models", source)

    def test_tenant_scoped_selectors(self):
        """Selectors must constrain tenant and organization."""
        source = Path(
            "apps/revenue_cycle/eligibility/selectors/eligibility.py"
        ).read_text(encoding="utf-8")
        self.assertIn("organization__tenant_id=tenant_id", source)
        self.assertIn("organization_id=organization_id", source)

    def test_after_commit_events(self):
        """Mutation workflows must dispatch events after commit."""
        source = Path(
            "apps/revenue_cycle/eligibility/workflows/eligibility.py"
        ).read_text(encoding="utf-8")
        self.assertIn("publish_after_commit", source)

    def test_explicit_request_context(self):
        """API must require explicit tenant and organization context."""
        source = Path(
            "apps/revenue_cycle/eligibility/api/views/eligibility.py"
        ).read_text(encoding="utf-8")
        self.assertIn('getattr(request, "tenant", None)', source)
        self.assertIn('getattr(request, "organization", None)', source)


__all__ = ("EligibilityArchitectureTests",)
