"""Architecture tests for organization context and RBAC control."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class OrganizationAccessControlArchitectureTests(SimpleTestCase):
    """Validate authority and tenant-isolation contracts."""

    def paths(self):
        root = Path(__file__).resolve().parents[1]
        return (
            root / "access_control" / "service.py",
            root / "access_control" / "api" / "views.py",
        )

    def test_bootstrap_owns_active_organization_resolution(self):
        text = self.paths()[1].read_text(encoding="utf-8")
        self.assertIn("PlatformBootstrapSelector", text)
        self.assertIn("bootstrap.organization", text)

    def test_backend_uses_canonical_rbac_authority(self):
        text = self.paths()[0].read_text(encoding="utf-8")
        self.assertIn("user_has_permission", text)
        self.assertIn("EffectiveCapabilityContext", text)

    def test_department_membership_is_tenant_scoped(self):
        text = self.paths()[1].read_text(encoding="utf-8")
        self.assertIn("department__organization=organization", text)
        self.assertIn("organization=organization", text)
