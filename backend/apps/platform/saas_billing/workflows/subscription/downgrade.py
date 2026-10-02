"""
DatavionOS SaaS Subscription downgrade workflow.

Responsibilities:

- Downgrade organization subscription plan
- Update subscription entitlements
- Emit SubscriptionDowngraded domain event

Architecture:

API
 |
WorkflowRegistry
 |
DowngradeSubscriptionWorkflow
 |
SubscriptionService
 |
Subscription Model
 |
Domain Event
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    SubscriptionDowngraded,
)
from apps.platform.saas_billing.events.dispatcher import (
    EventDispatcher,
)
from apps.platform.saas_billing.services import (
    SubscriptionService,
)
from apps.platform.saas_billing.workflows.base import (
    BaseWorkflow,
)


class DowngradeSubscriptionWorkflow(
    BaseWorkflow,
):
    """
    Downgrade SaaS subscription workflow.
    """

    def execute(
        self,
        *,
        subscription,
        new_plan,
    ):
        """
        Execute subscription downgrade.
        """

        subscription = SubscriptionService.downgrade(
            subscription=subscription,
            new_plan=new_plan,
        )

        EventDispatcher.dispatch(
            SubscriptionDowngraded(
                aggregate_id=subscription.id,
                payload={
                    "subscription_id": str(
                        subscription.id,
                    ),
                    "organization_id": str(
                        subscription.organization_id,
                    ),
                    "old_plan": (
                        subscription.plan_snapshot.get(
                            "code",
                        )
                    ),
                    "new_plan": (new_plan.code),
                },
            ),
        )

        return subscription


__all__ = [
    "DowngradeSubscriptionWorkflow",
]
