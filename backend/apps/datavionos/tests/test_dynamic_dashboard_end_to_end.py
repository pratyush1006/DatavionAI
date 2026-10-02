# DatavionAI Dynamic Dashboard authority contract tests.
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()
from types import SimpleNamespace

from django.test import SimpleTestCase

from apps.datavionos.builders.dashboard import DashboardBuilder
from apps.datavionos.builders.navigation import NavigationBuilder
from apps.datavionos.services.effective_capability import (
    build_effective_capability_context,
)


def make_module():
    return SimpleNamespace(
        identifier="patients",
        is_available=True,
        feature_flags=("patients.dashboard",),
        permissions=("patients.view",),
        dashboard=SimpleNamespace(
            enabled=True,
            title="Patients",
            description="Patients",
            icon="users",
            route="/patients",
            order=1,
        ),
        has_navigation=True,
        navigation=SimpleNamespace(
            title="Patients",
            route="/patients",
            icon="users",
            category="clinical",
            order=1,
        ),
        category="clinical",
    )


class DynamicDashboardAuthorityTests(SimpleTestCase):
    def setUp(self):
        self.module = make_module()

    def context(self, module=True, feature=True, permission=True):
        return build_effective_capability_context(
            user_id="e2e-user",
            organization_id="e2e-org",
            tenant_id="e2e-tenant",
            modules={"patients": module},
            features={"patients.dashboard": feature},
            permissions={"patients.view"} if permission else set(),
        )

    def build(self, builder, context):
        return builder.build(
            modules=[self.module],
            permissions={"patients.view"},
            feature_flags={"patients.dashboard": True},
            effective_context=context,
        )

    def test_enabled_context_reaches_dashboard_and_navigation(self):
        context = self.context()
        self.assertTrue(self.build(DashboardBuilder(), context))
        self.assertTrue(self.build(NavigationBuilder(), context))

    def test_disabled_module_is_hidden_everywhere(self):
        context = self.context(module=False)
        self.assertEqual(self.build(DashboardBuilder(), context), [])
        self.assertEqual(self.build(NavigationBuilder(), context), [])

    def test_disabled_feature_is_hidden_everywhere(self):
        context = self.context(feature=False)
        self.assertEqual(self.build(DashboardBuilder(), context), [])
        self.assertEqual(self.build(NavigationBuilder(), context), [])

    def test_missing_permission_is_hidden_everywhere(self):
        context = self.context(permission=False)
        self.assertEqual(self.build(DashboardBuilder(), context), [])
        self.assertEqual(self.build(NavigationBuilder(), context), [])

    def test_builders_fail_closed_without_context(self):
        for builder in (DashboardBuilder(), NavigationBuilder()):
            with self.assertRaises(ValueError):
                builder.build(
                    modules=[self.module], permissions=set(), feature_flags={}
                )
