"""
Subscription activation workflow.

Activates DatavionOS SaaS subscriptions.

Workflow:

Subscription
        |
Validate Lifecycle
        |
Activate Subscription
        |
Publish SubscriptionActivated Event
        |
Return Activated Subscription
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    SubscriptionActivated,
)
from apps.platform.saas_billing.models import (
    Subscription,
)
from apps.platform.saas_billing.services import (
    SubscriptionService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class ActivateSubscriptionWorkflow(
    BaseWorkflow,
):
    """
    Enterprise subscription activation workflow.
    """

    def handle(
        self,
        *,
        subscription: Subscription,
    ) -> Subscription:
        """
        Activate subscription.

        Used during:

        - Successful payment
        - Trial conversion
        - Manual activation
        """

        if not subscription:
            raise ValueError(
                "Subscription is required.",
            )

        # --------------------------------------------------------------
        # Validate lifecycle
        # --------------------------------------------------------------

        if subscription.status == (Subscription.Status.CANCELLED):
            raise ValueError(
                "Cancelled subscription cannot be activated.",
            )

        if subscription.status == (Subscription.Status.EXPIRED):
            raise ValueError(
                "Expired subscription cannot be activated.",
            )

        # --------------------------------------------------------------
        # Activate subscription
        # --------------------------------------------------------------

        subscription = SubscriptionService.activate(
            subscription=subscription,
        )

        # --------------------------------------------------------------
        # Publish domain event
        # --------------------------------------------------------------

        self.publish_event(
            SubscriptionActivated(
                aggregate_id=(subscription.id),
                metadata={
                    "organization_id": (str(subscription.organization.id)),
                    "plan_id": (str(subscription.plan.id)),
                    "plan_code": (subscription.plan.code),
                },
            )
        )

        return subscription


__all__ = [
    "ActivateSubscriptionWorkflow",
]
