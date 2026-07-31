"""
Plan activation workflow.

Activates DatavionOS SaaS plans.

Workflow:

Activate Request
        |
Validate Plan
        |
Activate Plan
        |
Publish PlanActivated Event
        |
Return Plan
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    PlanActivated,
)
from apps.platform.saas_billing.models import (
    Plan,
)
from apps.platform.saas_billing.services import (
    PlanService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class ActivatePlanWorkflow(
    BaseWorkflow,
):
    """
    Enterprise SaaS plan activation workflow.
    """

    def handle(
        self,
        *,
        plan: Plan,
    ) -> Plan:
        """
        Execute plan activation.
        """

        if not plan:
            raise ValueError(
                "Plan is required.",
            )

        plan = PlanService.activate(
            plan=plan,
        )

        self.publish_event(
            PlanActivated(
                aggregate_id=plan.id,
                metadata={
                    "plan_code": plan.code,
                },
            )
        )

        return plan


__all__ = [
    "ActivatePlanWorkflow",
]
