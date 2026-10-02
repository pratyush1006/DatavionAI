"""
Subscription lifecycle tests.

Validates:

- Subscription activation
- Subscription renewal
- Subscription cancellation
- Subscription expiry
"""

from __future__ import annotations

from decimal import Decimal

from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.saas_billing.models import (
    Subscription,
)
from apps.platform.saas_billing.services.entitlement_service import (
    EntitlementService,
)
from apps.platform.saas_billing.services.subscription_service import (
    SubscriptionService,
)
from apps.platform.saas_billing.workflows.subscription.activate import (
    ActivateSubscriptionWorkflow,
)
from apps.platform.saas_billing.workflows.subscription.cancel import (
    CancelSubscriptionWorkflow,
)
from apps.platform.saas_billing.workflows.subscription.expire import (
    ExpireSubscriptionWorkflow,
)
from apps.platform.saas_billing.workflows.subscription.renew import (
    RenewSubscriptionWorkflow,
)

from .base import (
    SaaSBillingTestBase,
)


class SubscriptionLifecycleTest(
    SaaSBillingTestBase,
):
    """
    Subscription workflow lifecycle tests.
    """

    def test_zero_day_free_plan_is_open_ended_and_entitled(self):
        self.plan.price = Decimal("0.00")
        self.plan.trial_days = 0
        self.plan.modules = {"pharmacy": True}
        self.plan.save(
            update_fields=["price", "trial_days", "modules", "updated_at"],
        )
        organization = Organization.objects.create(
            tenant=self.tenant,
            name="Free Pharmacy",
            display_name="Free Pharmacy",
            code="FREE-PHARMACY",
            slug="free-pharmacy",
        )

        subscription = SubscriptionService.create_trial_subscription(
            organization=organization,
            plan=self.plan,
        )

        self.assertEqual(subscription.status, Subscription.Status.ACTIVE)
        self.assertIsNone(subscription.trial_start)
        self.assertIsNone(subscription.trial_end)
        self.assertIsNone(subscription.current_period_end)
        self.assertIsNotNone(subscription.started_at)
        self.assertTrue(
            EntitlementService.has_module(
                organization=organization,
                module="pharmacy",
            )
        )

    def test_positive_trial_plan_keeps_a_finite_trial_period(self):
        self.plan.trial_days = 14
        self.plan.save(update_fields=["trial_days", "updated_at"])
        organization = Organization.objects.create(
            tenant=self.tenant,
            name="Trial Pharmacy",
            display_name="Trial Pharmacy",
            code="TRIAL-PHARMACY",
            slug="trial-pharmacy",
        )

        subscription = SubscriptionService.create_trial_subscription(
            organization=organization,
            plan=self.plan,
        )

        self.assertEqual(subscription.status, Subscription.Status.TRIAL)
        self.assertIsNotNone(subscription.trial_start)
        self.assertIsNotNone(subscription.trial_end)
        self.assertGreater(
            subscription.current_period_end,
            subscription.current_period_start,
        )

    def test_subscription_activation(
        self,
    ):
        """
        Validate activation flow.
        """

        subscription = self.subscription

        subscription.status = Subscription.Status.TRIAL

        subscription.save()

        activated = ActivateSubscriptionWorkflow().handle(
            subscription=subscription,
        )

        self.assertEqual(
            activated.status,
            Subscription.Status.ACTIVE,
        )

    def test_subscription_renewal(
        self,
    ):
        """
        Validate renewal flow.
        """

        old_end = self.subscription.current_period_end

        renewed = RenewSubscriptionWorkflow().handle(
            subscription=self.subscription,
        )

        renewed.refresh_from_db()

        self.assertEqual(
            renewed.status,
            Subscription.Status.ACTIVE,
        )

        self.assertGreater(
            renewed.current_period_end,
            old_end,
        )

    def test_subscription_cancellation(
        self,
    ):
        """
        Validate cancellation flow.
        """

        cancelled = CancelSubscriptionWorkflow().handle(
            subscription=self.subscription,
            reason=(Subscription.CancellationReason.CUSTOMER_REQUEST),
        )

        cancelled.refresh_from_db()

        self.assertEqual(
            cancelled.status,
            Subscription.Status.CANCELLED,
        )

        self.assertEqual(
            cancelled.cancellation_reason,
            Subscription.CancellationReason.CUSTOMER_REQUEST,
        )

    def test_subscription_expiry(
        self,
    ):
        """
        Validate expiry flow.
        """

        expired = ExpireSubscriptionWorkflow().handle(
            subscription=self.subscription,
        )

        expired.refresh_from_db()

        self.assertEqual(
            expired.status,
            Subscription.Status.EXPIRED,
        )
