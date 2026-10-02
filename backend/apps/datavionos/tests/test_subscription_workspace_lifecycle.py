"""End-to-end SaaS subscription-to-workspace lifecycle tests."""

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
    return SimpleNamespace(
        identifier="module-a",
        is_available=True,
        feature_flags=("module-a.dashboard",),
        permissions=("module-a.view",),
        dashboard=SimpleNamespace(
            enabled=True,
            title="Module A",
            description="Subscription lifecycle workspace",
            icon="grid",
            route="/module-a",
            order=10,
        ),
        has_navigation=True,
        navigation=SimpleNamespace(
            title="Module A",
            route="/module-a",
            icon="grid",
            category="platform",
            order=10,
        ),
        category="platform",
    )


class SubscriptionWorkspaceLifecycleTests(unittest.TestCase):
    """Prove subscription state propagates into the effective workspace."""

    def setUp(self):
        self.module = make_module()
        self.dashboard_builder = DashboardBuilder()
        self.navigation_builder = NavigationBuilder()

    @staticmethod
    def context(*, entitled, module_enabled, feature_enabled, permission):
        return build_effective_capability_context(
            user_id="subscription-lifecycle-user",
            organization_id="subscription-lifecycle-org",
            tenant_id="subscription-lifecycle-tenant",
            modules={"module-a": entitled and module_enabled},
            features={
                "module-a.dashboard": (entitled and module_enabled and feature_enabled)
            },
            permissions={"module-a.view"} if permission else set(),
        )

    def render(self, context: EffectiveCapabilityContext):
        dashboard = self.dashboard_builder.build(
            modules=[self.module],
            permissions={"module-a.view"},
            feature_flags={"module-a.dashboard": True},
            effective_context=context,
        )
        navigation = self.navigation_builder.build(
            modules=[self.module],
            permissions={"module-a.view"},
            feature_flags={"module-a.dashboard": True},
            effective_context=context,
        )
        return dashboard, navigation

    def assert_visible(self, context):
        dashboard, navigation = self.render(context)
        self.assertEqual(len(dashboard), 1)
        self.assertEqual(len(navigation), 1)
        self.assertEqual(dashboard[0].route, "/module-a")
        self.assertEqual(navigation[0].route, "/module-a")

    def assert_hidden(self, context):
        dashboard, navigation = self.render(context)
        self.assertEqual(dashboard, [])
        self.assertEqual(navigation, [])

    def test_subscription_a_entitles_module_and_workspace_is_visible(self):
        self.assert_visible(
            self.context(
                entitled=True,
                module_enabled=True,
                feature_enabled=True,
                permission=True,
            )
        )

    def test_admin_disable_hides_entitled_workspace(self):
        self.assert_hidden(
            self.context(
                entitled=True,
                module_enabled=False,
                feature_enabled=True,
                permission=True,
            )
        )

    def test_admin_reenable_restores_entitled_workspace(self):
        self.assert_visible(
            self.context(
                entitled=True,
                module_enabled=True,
                feature_enabled=True,
                permission=True,
            )
        )

    def test_unentitled_module_is_hidden_even_when_local_module_is_on(self):
        self.assert_hidden(
            self.context(
                entitled=False,
                module_enabled=True,
                feature_enabled=True,
                permission=True,
            )
        )

    def test_subscription_removal_removes_workspace(self):
        self.assert_hidden(
            self.context(
                entitled=False,
                module_enabled=True,
                feature_enabled=True,
                permission=True,
            )
        )

    def test_subscription_change_to_entitled_restores_workspace(self):
        self.assert_visible(
            self.context(
                entitled=True,
                module_enabled=True,
                feature_enabled=True,
                permission=True,
            )
        )

    def test_rbac_removal_removes_workspace(self):
        self.assert_hidden(
            self.context(
                entitled=True,
                module_enabled=True,
                feature_enabled=True,
                permission=False,
            )
        )

    def test_feature_removal_removes_workspace(self):
        self.assert_hidden(
            self.context(
                entitled=True,
                module_enabled=True,
                feature_enabled=False,
                permission=True,
            )
        )

    def test_effective_context_controls_dashboard_and_navigation_together(self):
        dashboard, navigation = self.render(
            self.context(
                entitled=True,
                module_enabled=True,
                feature_enabled=True,
                permission=True,
            )
        )
        self.assertEqual(dashboard[0].route, navigation[0].route)


__all__ = ["SubscriptionWorkspaceLifecycleTests"]
