"""
Subscription creation workflow.

Creates DatavionOS SaaS subscription
during organization onboarding.

Workflow:

Organization Created
        |
Validate Organization
        |
Resolve Plan
        |
Create Trial Subscription
        |
Publish SubscriptionCreated Event
        |
Return Subscription
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    SubscriptionCreated,
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


class CreateSubscriptionWorkflow(
    BaseWorkflow,
):
    """
    Enterprise subscription creation workflow.
    """

    def handle(
        self,
        *,
        organization,
        plan: Plan | None = None,
    ) -> Subscription:
        """
        Execute subscription creation.

        Used during:

        - Organization registration
        - Tenant onboarding
        - SaaS provisioning
        """

        if not organization:
            raise ValueError(
                "Organization is required.",
            )

        existing = Subscription.objects.filter(
            organization=organization,
        ).first()

        if existing:
            return existing

        if plan is None:
            plan = Plan.objects.default()

        if not plan:
            raise ValueError(
                "No default SaaS plan configured.",
            )

        subscription = SubscriptionService.create_trial_subscription(
            organization=organization,
            plan=plan,
        )

        self.publish_event(
            SubscriptionCreated(
                aggregate_id=(subscription.id),
                metadata={
                    "organization_id": (str(organization.id)),
                    "plan_id": (str(plan.id)),
                    "plan_code": (plan.code),
                },
            )
        )

        return subscription


__all__ = [
    "CreateSubscriptionWorkflow",
]
