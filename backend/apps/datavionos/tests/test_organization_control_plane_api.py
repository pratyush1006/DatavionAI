from __future__ import annotations

from django.test import SimpleTestCase


class OrganizationControlPlaneContractTest(SimpleTestCase):
    def test_backend_authority_contract(self):
        service = open(
            "apps/datavionos/control_plane/service.py", encoding="utf-8"
        ).read()
        view = open(
            "apps/datavionos/control_plane/api/views.py", encoding="utf-8"
        ).read()
        for token in (
            "OrganizationModule",
            "OrganizationFeature",
            "Subscription",
            "OrganizationPolicy",
        ):
            self.assertIn(token, service)
        for token in (
            "can_manage_modules",
            "can_manage_features",
            "organization=organization",
            "enable_module(instance=module)",
            "disable_module(instance=module)",
            "enable_feature(instance=feature)",
            "disable_feature(instance=feature)",
        ):
            self.assertIn(token, view)

    def test_family_members_not_referenced(self):
        source = (
            open("apps/datavionos/control_plane/api/views.py", encoding="utf-8")
            .read()
            .lower()
        )
        self.assertNotIn("family_members", source)
        self.assertNotIn("family-members", source)
