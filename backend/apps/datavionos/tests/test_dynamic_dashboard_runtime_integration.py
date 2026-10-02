from __future__ import annotations

import inspect
from pathlib import Path
from unittest.mock import Mock, patch

from django.test import SimpleTestCase


class DynamicDashboardRuntimeIntegrationTests(SimpleTestCase):
    def test_selector_uses_status_field(self):
        from apps.platform.organizations.selectors.organization_module import (
            get_modules,
        )

        source = inspect.getsource(get_modules)
        self.assertIn("status=OrganizationModule.Status.ENABLED", source)
        self.assertNotIn("is_enabled=is_enabled", source)

    def test_missing_subscription_fails_closed(self):
        from apps.datavionos.resolvers.entitlement import EntitlementResolver

        with patch(
            "apps.datavionos.resolvers.entitlement.EntitlementService.get_subscription",
            return_value=None,
        ):
            result = EntitlementResolver.resolve(organization=Mock())
        self.assertEqual(result["modules"], {})
        self.assertEqual(result["features"], {})

    def test_effective_context_contract(self):
        from apps.datavionos.services.effective_capability import (
            build_effective_capability_context,
        )

        context = build_effective_capability_context(
            user_id="u",
            organization_id="o",
            tenant_id="t",
            modules={"pharmacy": True},
            features={"pharmacy.ai": True},
            permissions={"pharmacy.view"},
        )
        self.assertTrue(context.module_enabled("pharmacy"))
        self.assertTrue(context.feature_enabled("pharmacy.ai"))
        self.assertTrue(context.has_permission("pharmacy.view"))

    def test_dashboard_requires_effective_context(self):
        from apps.datavionos.builders.dashboard import DashboardBuilder

        with self.assertRaises(ValueError):
            DashboardBuilder().build(
                modules=[], permissions=set(), feature_flags={}, effective_context=None
            )

    def test_bootstrap_feature_flags_before_context(self):
        path = Path(__file__).resolve().parents[1] / "bootstrap" / "service.py"
        source = path.read_text(encoding="utf-8")
        self.assertLess(
            source.index("feature_flags = self._bootstrap_feature_flags"),
            source.index("effective_context = build_effective_capability_context"),
        )
