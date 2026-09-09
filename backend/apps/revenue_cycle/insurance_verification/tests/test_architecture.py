"""Architecture tests for Revenue Cycle Insurance Verification."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class InsuranceVerificationArchitectureTests(SimpleTestCase):
    """Verify the Insurance Verification architectural contract."""

    def test_canonical_patient(self):
        """Insurance Verification must use canonical Patient."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/models/insurance_verification.py"
        ).read_text(encoding="utf-8")
        self.assertIn("apps.patient_management.patients.models", source)

    def test_tenant_scoped_selectors(self):
        """Selectors must constrain tenant and organization."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/selectors/insurance_verification.py"
        ).read_text(encoding="utf-8")
        self.assertIn("organization__tenant_id=tenant_id", source)
        self.assertIn("organization_id=organization_id", source)

    def test_after_commit_events(self):
        """Mutation workflows must dispatch events after commit."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/workflows/insurance_verification.py"
        ).read_text(encoding="utf-8")
        self.assertIn("publish_after_commit", source)

    def test_platform_rbac(self):
        """Authorization must use the canonical platform RBAC engine."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/policies.py"
        ).read_text(encoding="utf-8")
        self.assertIn("apps.platform.rbac.resolvers", source)

    def test_explicit_context(self):
        """API must require explicit tenant and organization context."""

        source = Path(
            "apps/revenue_cycle/insurance_verification/api/views/insurance_verification.py"
        ).read_text(encoding="utf-8")
        self.assertIn('getattr(request, "tenant", None)', source)
        self.assertIn('getattr(request, "organization", None)', source)


__all__ = ("InsuranceVerificationArchitectureTests",)
