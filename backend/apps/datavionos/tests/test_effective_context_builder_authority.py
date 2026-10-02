"""
DatavionAI — Effective Capability Context Builder Authority Tests.

Canonical contract tests for:

    EffectiveCapabilityContext
            ↓
    DashboardBuilder / NavigationBuilder

These tests intentionally validate:

    1. canonical EffectiveCapabilityContext APIs
    2. builder context contract
    3. allowed module rendering
    4. module denial
    5. feature denial
    6. RBAC denial
    7. fail-closed behavior

Do not introduce a synthetic NavigationItem.key field.
NavigationItem uses its canonical route attribute.
"""

from __future__ import annotations

import inspect
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
    Build the smallest module contract required by the canonical builders.
    """

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


def make_context(
    *,
    module_enabled=True,
    feature_enabled=True,
    permission_enabled=True,
):
    permissions = {"patients.view"} if permission_enabled else set()

    return build_effective_capability_context(
        user_id="u",
        organization_id="o",
        tenant_id="t",
        modules={
            "patients": module_enabled,
        },
        features={
            "patients.dashboard": feature_enabled,
        },
        permissions=permissions,
    )


class EffectiveContextBuilderAuthorityTests(unittest.TestCase):
    """
    Canonical authority tests.

    Django must discover all seven tests.
    """

    def test_context_contract(self):
        self.assertTrue(
            hasattr(
                EffectiveCapabilityContext,
                "module_enabled",
            )
        )

        self.assertTrue(
            hasattr(
                EffectiveCapabilityContext,
                "feature_enabled",
            )
        )

        self.assertTrue(
            hasattr(
                EffectiveCapabilityContext,
                "has_permission",
            )
        )

        self.assertTrue(
            hasattr(
                EffectiveCapabilityContext,
                "has_any_permission",
            )
        )

    def test_builder_interface_requires_effective_context(self):
        dashboard_signature = inspect.signature(
            DashboardBuilder.build,
        )

        navigation_signature = inspect.signature(
            NavigationBuilder.build,
        )

        self.assertIn(
            "effective_context",
            dashboard_signature.parameters,
        )

        self.assertIn(
            "effective_context",
            navigation_signature.parameters,
        )

    def test_allowed_context_builds_dashboard_and_navigation(self):
        module = make_module()
        context = make_context()

        dashboard = DashboardBuilder().build(
            modules=[module],
            permissions=set(),
            feature_flags={},
            effective_context=context,
        )

        navigation = NavigationBuilder().build(
            modules=[module],
            permissions=set(),
            feature_flags={},
            effective_context=context,
        )

        self.assertTrue(dashboard)
        self.assertTrue(navigation)

        self.assertEqual(
            navigation[0].route,
            "/patients",
        )

    def test_denied_module_blocks_dashboard_and_navigation(self):
        module = make_module()
        context = make_context(
            module_enabled=False,
        )

        dashboard = DashboardBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={
                "patients.dashboard": True,
            },
            effective_context=context,
        )

        navigation = NavigationBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={
                "patients.dashboard": True,
            },
            effective_context=context,
        )

        self.assertEqual(
            dashboard,
            [],
        )

        self.assertEqual(
            navigation,
            [],
        )

    def test_denied_feature_blocks_dashboard_and_navigation(self):
        module = make_module()
        context = make_context(
            feature_enabled=False,
        )

        dashboard = DashboardBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={
                "patients.dashboard": True,
            },
            effective_context=context,
        )

        navigation = NavigationBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={
                "patients.dashboard": True,
            },
            effective_context=context,
        )

        self.assertEqual(
            dashboard,
            [],
        )

        self.assertEqual(
            navigation,
            [],
        )

    def test_denied_permission_blocks_dashboard_and_navigation(self):
        module = make_module()
        context = make_context(
            permission_enabled=False,
        )

        dashboard = DashboardBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={
                "patients.dashboard": True,
            },
            effective_context=context,
        )

        navigation = NavigationBuilder().build(
            modules=[module],
            permissions={"patients.view"},
            feature_flags={
                "patients.dashboard": True,
            },
            effective_context=context,
        )

        self.assertEqual(
            dashboard,
            [],
        )

        self.assertEqual(
            navigation,
            [],
        )

    def test_builders_fail_closed_without_effective_context(self):
        module = make_module()

        with self.assertRaises(ValueError):
            DashboardBuilder().build(
                modules=[module],
                permissions={"patients.view"},
                feature_flags={
                    "patients.dashboard": True,
                },
            )

        with self.assertRaises(ValueError):
            NavigationBuilder().build(
                modules=[module],
                permissions={"patients.view"},
                feature_flags={
                    "patients.dashboard": True,
                },
            )


if __name__ == "__main__":
    unittest.main()
