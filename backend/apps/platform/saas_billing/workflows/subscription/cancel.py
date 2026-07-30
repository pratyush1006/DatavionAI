"""
Subscription cancellation workflow.

Handles DatavionOS subscription
cancellation lifecycle.

Workflow:

Active Subscription
        |
Validate Cancellation
        |
Cancel Subscription Service
        |
Publish SubscriptionCancelled Event
        |
Return Subscription
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    SubscriptionCancelled,
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


class CancelSubscriptionWorkflow(
    BaseWorkflow,
):
    """
    Enterprise subscription cancellation workflow.
    """

    def handle(
        self,
        *,
        subscription: Subscription,
        reason: str | None = None,
    ) -> Subscription:
        """
        Cancel subscription.

        Supports:

        - Customer cancellation
        - Payment failure cancellation
        - Plan migration
        - Enterprise termination
        """

        if not subscription:
            raise ValueError(
                "Subscription is required.",
            )

        # --------------------------------------------------------------
        # Validate lifecycle
        # --------------------------------------------------------------

        if subscription.status == (Subscription.Status.CANCELLED):
            return subscription

        if subscription.status == (Subscription.Status.EXPIRED):
            raise ValueError(
                "Expired subscription cannot be cancelled.",
            )

        # --------------------------------------------------------------
        # Resolve cancellation reason
        # --------------------------------------------------------------

        cancellation_reason = reason or Subscription.CancellationReason.CUSTOMER_REQUEST

        # --------------------------------------------------------------
        # Cancel subscription
        # --------------------------------------------------------------

        subscription = SubscriptionService.cancel(
            subscription=subscription,
            reason=cancellation_reason,
        )

        # --------------------------------------------------------------
        # Publish domain event
        # --------------------------------------------------------------

        self.publish_event(
            SubscriptionCancelled(
                aggregate_id=(subscription.id),
                metadata={
                    "organization_id": (str(subscription.organization.id)),
                    "reason": (cancellation_reason),
                    "plan_code": (subscription.plan.code),
                },
            )
        )

        return subscription


__all__ = [
    "CancelSubscriptionWorkflow",
]
