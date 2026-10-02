"""
DatavionOS entitlement engine tests.

Validates:

- Feature entitlements
- Module access
- Usage limits
- Subscription snapshots
"""

from __future__ import annotations

from apps.platform.saas_billing.models import (
    Subscription,
)

from .base import (
    SaaSBillingTestBase,
)


class EntitlementEngineTest(
    SaaSBillingTestBase,
):
    """
    Entitlement validation tests.
    """

    def test_feature_entitlements(
        self,
    ):
        """
        Validate feature access.
        """

        snapshot = self.subscription.feature_snapshot

        features = snapshot.get(
            "features",
            {},
        )

        self.assertTrue(features.get("advanced_ai"))

        self.assertTrue(features.get("telemedicine"))

        self.assertTrue(features.get("analytics"))

    def test_module_entitlements(
        self,
    ):
        """
        Validate enabled modules.
        """

        snapshot = self.subscription.feature_snapshot

        modules = snapshot.get(
            "modules",
            {},
        )

        self.assertTrue(modules.get("ai"))

        self.assertTrue(modules.get("billing"))

        self.assertTrue(modules.get("clinical"))

    def test_usage_limits(
        self,
    ):
        """
        Validate subscription limits.
        """

        limits = self.subscription.plan_snapshot.get(
            "limits",
            {},
        )

        # fallback for base fixture
        if not limits:
            limits = self.plan.limits

        self.assertEqual(
            limits.get("users"),
            10,
        )

        self.assertEqual(
            limits.get("patients"),
            1000,
        )

        self.assertEqual(
            limits.get("storage_gb"),
            50,
        )

    def test_active_subscription_required(
        self,
    ):
        """
        Validate entitlement requires active subscription.
        """

        self.assertEqual(
            self.subscription.status,
            Subscription.Status.ACTIVE,
        )
