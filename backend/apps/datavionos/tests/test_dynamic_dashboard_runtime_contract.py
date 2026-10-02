from __future__ import annotations

from django.test import SimpleTestCase

from apps.datavionos.services.effective_capability import (
    build_effective_capability_context,
)


class DynamicDashboardRuntimeContractTests(SimpleTestCase):
    """Executable Django test contract for the effective dashboard boundary."""

    def test_effective_context_converges_dashboard_inputs(self):
        context = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"patients": True, "pharmacy": False},
            features={"patients.dashboard": True, "pharmacy.ai": False},
            permissions={"patients.view"},
            roles={"organization_admin"},
            facilities={"facility-a"},
            departments={"clinical"},
            data_scopes={"patient": "organization"},
            ai_capabilities={"pharmacy.ai": False},
            limits={"patients": {"included": 100}},
        )
        self.assertTrue(context.module_enabled("patients"))
        self.assertFalse(context.module_enabled("pharmacy"))
        self.assertTrue(context.feature_enabled("patients.dashboard"))
        self.assertTrue(context.has_permission("patients.view"))
        self.assertFalse(context.ai_enabled("pharmacy.ai"))

    def test_unentitled_module_cannot_be_granted_by_organization_assignment(self):
        plan = {"patients": True}
        organization = {"pharmacy": True}
        effective = {
            key: bool(plan.get(key, False)) and bool(organization.get(key, True))
            for key in set(plan) | set(organization)
        }
        self.assertTrue(effective["patients"])
        self.assertFalse(effective["pharmacy"])

    def test_module_disable_and_reenable_transition_is_deterministic(self):
        enabled = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"patients": True},
            features={"patients.dashboard": True},
            permissions={"patients.view"},
        )
        disabled = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"patients": False},
            features={"patients.dashboard": True},
            permissions={"patients.view"},
        )
        restored = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"patients": True},
            features={"patients.dashboard": True},
            permissions={"patients.view"},
        )
        self.assertTrue(enabled.module_enabled("patients"))
        self.assertFalse(disabled.module_enabled("patients"))
        self.assertTrue(restored.module_enabled("patients"))

    def test_rbac_permission_removal_is_fail_closed(self):
        context = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"patients": True},
            features={"patients.dashboard": True},
            permissions=set(),
        )
        self.assertFalse(context.has_permission("patients.view"))


__all__ = ("DynamicDashboardRuntimeContractTests",)
