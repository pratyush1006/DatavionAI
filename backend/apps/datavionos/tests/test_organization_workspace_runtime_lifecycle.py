"""
DatavionOS organization workspace runtime lifecycle tests.

These tests validate the runtime contract between:

    subscription / entitlement state
        ->
    organization module state
        ->
    effective capability context
        ->
    dashboard / navigation

The tests deliberately use the existing canonical builders and
EffectiveCapabilityContext. They do not create a second authorization
implementation.
"""

from __future__ import annotations

import unittest
from types import SimpleNamespace

from apps.datavionos.builders.dashboard import DashboardBuilder
from apps.datavionos.builders.navigation import NavigationBuilder
from apps.datavionos.services.effective_capability import (
    EffectiveCapabilityContext,
    build_effective_capability_context,
)


def make_module():
    """
    Create a minimal module contract-shaped object.

    The production builder remains the authority under test.
    """

    return SimpleNamespace(
        identifier="patients",
        is_available=True,
        feature_flags=("patients.dashboard",),
        permissions=("patients.view",),
        dashboard=SimpleNamespace(
            enabled=True,
            title="Patients",
            description="Patient workspace",
            icon="users",
            route="/patients",
            order=10,
        ),
        has_navigation=True,
        navigation=SimpleNamespace(
            title="Patients",
            route="/patients",
            icon="users",
            category="clinical",
            order=10,
        ),
        category="clinical",
    )


class WorkspaceRuntimeLifecycleTests(
    unittest.TestCase,
):
    """
    Verify organization workspace capability transitions.
    """

    def setUp(self):
        self.module = make_module()

        self.dashboard_builder = DashboardBuilder()

        self.navigation_builder = NavigationBuilder()

    @staticmethod
    def context(
        *,
        module_enabled: bool,
        feature_enabled: bool,
        permission: bool,
    ) -> EffectiveCapabilityContext:
        return build_effective_capability_context(
            user_id="workspace-user",
            organization_id="workspace-organization",
            tenant_id="workspace-tenant",
            modules={
                "patients": module_enabled,
            },
            features={
                "patients.dashboard": feature_enabled,
            },
            permissions=({"patients.view"} if permission else set()),
        )

    def render(
        self,
        context: EffectiveCapabilityContext,
    ):
        dashboard = self.dashboard_builder.build(
            modules=[self.module],
            permissions={
                "patients.view",
            },
            feature_flags={
                "patients.dashboard": True,
            },
            effective_context=context,
        )

        navigation = self.navigation_builder.build(
            modules=[self.module],
            permissions={
                "patients.view",
            },
            feature_flags={
                "patients.dashboard": True,
            },
            effective_context=context,
        )

        return dashboard, navigation

    def test_subscription_entitled_and_module_enabled_is_visible(
        self,
    ):
        """
        Subscription entitlement + organization ON + feature ON +
        RBAC permission produces workspace visibility.
        """

        context = self.context(
            module_enabled=True,
            feature_enabled=True,
            permission=True,
        )

        dashboard, navigation = self.render(context)

        self.assertEqual(
            len(dashboard),
            1,
        )

        self.assertEqual(
            len(navigation),
            1,
        )

        self.assertEqual(
            dashboard[0].route,
            "/patients",
        )

        self.assertEqual(
            navigation[0].route,
            "/patients",
        )

    def test_organization_admin_disable_removes_workspace_capability(
        self,
    ):
        """
        Organization OFF must immediately remove the capability from
        dashboard and navigation after bootstrap/context refresh.
        """

        context = self.context(
            module_enabled=False,
            feature_enabled=True,
            permission=True,
        )

        dashboard, navigation = self.render(context)

        self.assertEqual(
            dashboard,
            [],
        )

        self.assertEqual(
            navigation,
            [],
        )

    def test_organization_admin_reenable_restores_workspace_capability(
        self,
    ):
        """
        Turning the organization module back ON restores the capability
        when SaaS entitlement and RBAC remain valid.
        """

        disabled = self.context(
            module_enabled=False,
            feature_enabled=True,
            permission=True,
        )

        disabled_dashboard, disabled_navigation = self.render(disabled)

        self.assertEqual(
            disabled_dashboard,
            [],
        )

        self.assertEqual(
            disabled_navigation,
            [],
        )

        enabled = self.context(
            module_enabled=True,
            feature_enabled=True,
            permission=True,
        )

        enabled_dashboard, enabled_navigation = self.render(enabled)

        self.assertEqual(
            len(enabled_dashboard),
            1,
        )

        self.assertEqual(
            len(enabled_navigation),
            1,
        )

    def test_subscription_entitlement_removal_removes_workspace(
        self,
    ):
        """
        A subscription downgrade/removal represented in the effective
        capability context must remove the workspace capability even if
        the organization toggle and RBAC permission remain enabled.

        The effective context is the runtime boundary; the SaaS Billing
        service remains the owner of how entitlement state is produced.
        """

        entitled = self.context(
            module_enabled=True,
            feature_enabled=True,
            permission=True,
        )

        dashboard, navigation = self.render(entitled)

        self.assertEqual(
            len(dashboard),
            1,
        )

        self.assertEqual(
            len(navigation),
            1,
        )

        downgraded = self.context(
            module_enabled=False,
            feature_enabled=True,
            permission=True,
        )

        dashboard_after, navigation_after = self.render(downgraded)

        self.assertEqual(
            dashboard_after,
            [],
        )

        self.assertEqual(
            navigation_after,
            [],
        )

    def test_rbac_removal_removes_workspace(
        self,
    ):
        """
        RBAC removal must remove presentation eligibility even when
        module and feature state remain enabled.
        """

        context = self.context(
            module_enabled=True,
            feature_enabled=True,
            permission=False,
        )

        dashboard, navigation = self.render(context)

        self.assertEqual(
            dashboard,
            [],
        )

        self.assertEqual(
            navigation,
            [],
        )

    def test_feature_removal_removes_workspace(
        self,
    ):
        """
        Feature OFF must remove the capability.
        """

        context = self.context(
            module_enabled=True,
            feature_enabled=False,
            permission=True,
        )

        dashboard, navigation = self.render(context)

        self.assertEqual(
            dashboard,
            [],
        )

        self.assertEqual(
            navigation,
            [],
        )

    def test_fail_closed_without_effective_context(
        self,
    ):
        """
        Builders must not silently reconstruct authorization when the
        effective context is absent.
        """

        with self.assertRaises(
            ValueError,
        ):
            self.dashboard_builder.build(
                modules=[self.module],
                permissions={
                    "patients.view",
                },
                feature_flags={
                    "patients.dashboard": True,
                },
            )

        with self.assertRaises(
            ValueError,
        ):
            self.navigation_builder.build(
                modules=[self.module],
                permissions={
                    "patients.view",
                },
                feature_flags={
                    "patients.dashboard": True,
                },
            )


if __name__ == "__main__":
    unittest.main()
