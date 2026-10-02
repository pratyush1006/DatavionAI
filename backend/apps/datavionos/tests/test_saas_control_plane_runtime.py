from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.datavionos.services.saas_capability_control_plane import (
    SaaSCapabilityProvider,
)


class SaaSControlPlaneRuntimeTests(SimpleTestCase):
    @staticmethod
    def manager(rows):
        value = MagicMock()
        value.filter.return_value = rows
        return value

    def test_organization_disable_hides_purchased_module(self):
        organization = SimpleNamespace(pk="org-1")
        modules = self.manager(
            [
                SimpleNamespace(module_code="PHARMACY", status="disabled", settings={}),
            ]
        )
        with patch(
            "apps.datavionos.services.saas_capability_control_plane.OrganizationModule.objects",
            modules,
        ):
            result = SaaSCapabilityProvider.resolve_organization_modules(
                organization=organization,
                entitled_modules={"pharmacy": True},
            )
        self.assertFalse(result["pharmacy"])

    def test_organization_override_cannot_create_unpurchased_module(self):
        organization = SimpleNamespace(pk="org-2")
        modules = self.manager(
            [
                SimpleNamespace(
                    module_code="LABORATORY", status="enabled", settings={}
                ),
            ]
        )
        with patch(
            "apps.datavionos.services.saas_capability_control_plane.OrganizationModule.objects",
            modules,
        ):
            result = SaaSCapabilityProvider.resolve_organization_modules(
                organization=organization,
                entitled_modules={"pharmacy": True},
            )
        self.assertNotIn("laboratory", result)

    def test_active_module_carries_department_and_ai_scope(self):
        organization = SimpleNamespace(pk="org-3")
        modules = self.manager(
            [
                SimpleNamespace(
                    module_code="PHARMACY",
                    status="enabled",
                    settings={
                        "department_code": "pharmacy",
                        "ai_capabilities": {"pharmacy.ai": True},
                    },
                ),
            ]
        )
        with patch(
            "apps.datavionos.services.saas_capability_control_plane.OrganizationModule.objects",
            modules,
        ):
            result = SaaSCapabilityProvider._apply_module_overrides(
                organization=organization,
                entitled_modules={"pharmacy": True},
            )
        self.assertEqual(result[1], {"PHARMACY"})
        self.assertEqual(result[2], {"pharmacy.ai": True})

    @patch(
        "apps.datavionos.services.saas_capability_control_plane.EntitlementResolver.resolve"
    )
    @patch(
        "apps.datavionos.services.saas_capability_control_plane.PermissionResolver.resolve"
    )
    @patch(
        "apps.datavionos.services.saas_capability_control_plane.OrganizationFeature.objects"
    )
    @patch(
        "apps.datavionos.services.saas_capability_control_plane.OrganizationModule.objects"
    )
    def test_provider_composes_saas_org_and_rbac(
        self,
        modules,
        features,
        permissions,
        entitlements,
    ):
        organization = SimpleNamespace(pk="org-4", tenant_id="tenant-4")
        user = SimpleNamespace(pk="user-4", is_authenticated=True)
        entitlements.return_value = {
            "modules": {"pharmacy": True, "laboratory": True},
            "features": {"pharmacy.ai": True},
        }
        permissions.return_value = {"pharmacy.view"}
        modules.filter.return_value = [
            SimpleNamespace(module_code="PHARMACY", status="enabled", settings={}),
            SimpleNamespace(module_code="LABORATORY", status="disabled", settings={}),
        ]
        features.filter.return_value = []

        snapshot = SaaSCapabilityProvider().resolve(
            user=user,
            organization=organization,
        )

        self.assertEqual(
            snapshot.modules,
            {"pharmacy": True, "laboratory": False},
        )
        self.assertEqual(snapshot.permissions, frozenset({"pharmacy.view"}))

    def test_unentitled_ai_feature_cannot_be_activated_by_local_settings(self):
        organization = SimpleNamespace(pk="org-5", tenant_id="tenant-5")
        user = SimpleNamespace(pk="user-5", is_authenticated=True)
        modules = self.manager(
            [
                SimpleNamespace(
                    module_code="PHARMACY",
                    status="enabled",
                    settings={"ai_capabilities": {"pharmacy.ai": True}},
                ),
            ]
        )
        features = self.manager([])
        with (
            patch(
                "apps.datavionos.services.saas_capability_control_plane.OrganizationModule.objects",
                modules,
            ),
            patch(
                "apps.datavionos.services.saas_capability_control_plane.OrganizationFeature.objects",
                features,
            ),
            patch(
                "apps.datavionos.services.saas_capability_control_plane.EntitlementResolver.resolve",
                return_value={"modules": {"pharmacy": True}, "features": {}},
            ),
            patch(
                "apps.datavionos.services.saas_capability_control_plane.PermissionResolver.resolve",
                return_value=set(),
            ),
        ):
            snapshot = SaaSCapabilityProvider().resolve(
                user=user, organization=organization
            )
        self.assertEqual(snapshot.ai_capabilities, {})

    def test_missing_organization_fails_closed(self):
        snapshot = SaaSCapabilityProvider().resolve(user=None, organization=None)
        self.assertEqual(snapshot.modules, {})
        self.assertEqual(snapshot.features, {})
        self.assertEqual(snapshot.permissions, frozenset())
