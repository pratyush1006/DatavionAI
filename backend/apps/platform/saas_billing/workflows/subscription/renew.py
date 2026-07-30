"""
Subscription renewal workflow.

Handles DatavionOS subscription renewal lifecycle.

Workflow:

Subscription Expiring
        |
Validate Renewal Eligibility
        |
Generate Renewal Invoice
        |
Renew Subscription
        |
Publish SubscriptionRenewed Event
        |
Return Subscription
"""

from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.platform.saas_billing.events import (
    SubscriptionRenewed,
)
from apps.platform.saas_billing.models import (
    Subscription,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class RenewSubscriptionWorkflow(
    BaseWorkflow,
):
    """
    Enterprise subscription renewal workflow.
    """

    def handle(
        self,
        *,
        subscription: Subscription,
    ) -> Subscription:
        """
        Renew subscription.

        Used for:

        - Automatic renewal
        - Manual renewal
        - Enterprise contract renewal
        """

        if not subscription:
            raise ValueError(
                "Subscription is required.",
            )

        # --------------------------------------------------------------
        # Validate subscription state
        # --------------------------------------------------------------

        if subscription.status in [
            Subscription.Status.CANCELLED,
            Subscription.Status.SUSPENDED,
        ]:
            raise ValueError(
                "Subscription cannot be renewed.",
            )

        # --------------------------------------------------------------
        # Validate renewal permission
        # --------------------------------------------------------------

        if not subscription.auto_renew:
            raise ValueError(
                "Auto renewal is disabled.",
            )

        # --------------------------------------------------------------
        # Calculate renewal period
        # --------------------------------------------------------------

        current_end = subscription.current_period_end or timezone.now()

        billing_cycle = subscription.plan.billing_cycle

        if billing_cycle == "yearly":
            duration = timedelta(
                days=365,
            )

        else:
            duration = timedelta(
                days=30,
            )

        new_end = current_end + duration

        # --------------------------------------------------------------
        # Update subscription
        # --------------------------------------------------------------

        subscription.current_period_start = current_end

        subscription.current_period_end = new_end

        subscription.expires_at = new_end

        subscription.status = Subscription.Status.ACTIVE

        subscription.save(
            update_fields=[
                "current_period_start",
                "current_period_end",
                "expires_at",
                "status",
                "updated_at",
            ],
        )

        # --------------------------------------------------------------
        # Publish domain event
        # --------------------------------------------------------------

        self.publish_event(
            SubscriptionRenewed(
                aggregate_id=(subscription.id),
                metadata={
                    "organization_id": (str(subscription.organization.id)),
                    "plan_code": (subscription.plan.code),
                    "renewed_until": (new_end.isoformat()),
                },
            )
        )

        return subscription


__all__ = [
    "RenewSubscriptionWorkflow",
]
