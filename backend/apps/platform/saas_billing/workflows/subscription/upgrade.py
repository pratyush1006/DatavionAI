"""
Subscription upgrade workflow.

Changes DatavionOS SaaS subscription
to a higher tier plan.

Workflow:

Upgrade Request
        |
Validate Subscription
        |
Validate Target Plan
        |
SubscriptionService.upgrade()
        |
Refresh Entitlements
        |
Publish SubscriptionUpgraded Event
        |
Return Subscription
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    SubscriptionUpgraded,
)
from apps.platform.saas_billing.models import (
    Plan,
    Subscription,
)
from apps.platform.saas_billing.services import (
    SubscriptionService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class UpgradeSubscriptionWorkflow(
    BaseWorkflow,
):
    """
    Enterprise SaaS subscription upgrade workflow.

    Handles:

    - Subscription plan upgrade
    - Plan snapshot refresh
    - Feature refresh
    - Module refresh
    - Domain event publishing
    """

    def handle(
        self,
        *,
        subscription: Subscription,
        plan: Plan,
    ) -> Subscription:
        """
        Execute subscription upgrade.
        """

        if not subscription:
            raise ValueError(
                "Subscription is required.",
            )

        if not plan:
            raise ValueError(
                "Target plan is required.",
            )

        if subscription.plan_id == plan.id:
            return subscription

        old_plan = subscription.plan

        subscription = SubscriptionService.upgrade(
            subscription=subscription,
            new_plan=plan,
        )

        subscription = SubscriptionService.refresh_entitlements(
            subscription=subscription,
        )

        self.publish_event(
            SubscriptionUpgraded(
                aggregate_id=subscription.id,
                metadata={
                    "organization_id": (
                        str(
                            subscription.organization_id,
                        )
                    ),
                    "old_plan_id": (
                        str(
                            old_plan.id,
                        )
                    ),
                    "old_plan_code": old_plan.code,
                    "new_plan_id": (
                        str(
                            plan.id,
                        )
                    ),
                    "new_plan_code": plan.code,
                },
            )
        )

        return subscription


__all__ = [
    "UpgradeSubscriptionWorkflow",
]
