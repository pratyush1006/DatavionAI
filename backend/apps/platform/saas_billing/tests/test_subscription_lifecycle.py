"""
Subscription lifecycle tests.

Validates:

- Create subscription
- Activate subscription
- Renew subscription
- Cancel subscription
"""

from __future__ import annotations

from apps.platform.saas_billing.models import (
    Subscription,
)
from apps.platform.saas_billing.workflows.subscription.activate import (
    ActivateSubscriptionWorkflow,
)
from apps.platform.saas_billing.workflows.subscription.cancel import (
    CancelSubscriptionWorkflow,
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
