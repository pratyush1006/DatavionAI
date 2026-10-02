"""
DatavionOS SaaS Billing subscription expiry workflow.

Responsibilities:

- Expire subscription
- Update subscription lifecycle state
- Trigger subscription expiry domain event

Architecture:

Workflow
    |
SubscriptionService
    |
Subscription Model
    |
Domain Event
    |
Event Dispatcher
    |
Handlers
"""

from __future__ import annotations

from apps.platform.saas_billing.models import (
    Subscription,
)
from apps.platform.saas_billing.services.subscription_service import (
    SubscriptionService,
)
from apps.platform.saas_billing.workflows.base import (
    BaseWorkflow,
)


class ExpireSubscriptionWorkflow(
    BaseWorkflow,
):
    """
    Expire SaaS subscription workflow.
    """

    def handle(
        self,
        *,
        subscription: Subscription,
    ) -> Subscription:
        """
        Execute subscription expiry.
        """

        return SubscriptionService.expire(
            subscription=subscription,
        )


__all__ = [
    "ExpireSubscriptionWorkflow",
]
