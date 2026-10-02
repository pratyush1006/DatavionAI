"""
Plan update workflow.

Updates DatavionOS SaaS billing plans.

Workflow:

Plan Update Request
        |
Validate Plan
        |
Update Plan
        |
Publish PlanUpdated Event
        |
Return Plan
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    PlanUpdated,
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


class UpdatePlanWorkflow(
    BaseWorkflow,
):
    """
    Enterprise SaaS plan update workflow.
    """

    def handle(
        self,
        *,
        plan: Plan,
        data: dict,
    ) -> Plan:
        """
        Execute plan update.
        """

        if not plan:
            raise ValueError(
                "Plan is required.",
            )

        if not data:
            raise ValueError(
                "Plan update data is required.",
            )

        plan = PlanService.update_plan(
            plan=plan,
            data=data,
        )

        self.publish_event(
            PlanUpdated(
                aggregate_id=plan.id,
                metadata={
                    "plan_code": plan.code,
                    "plan_name": plan.name,
                },
            )
        )

        return plan


__all__ = [
    "UpdatePlanWorkflow",
]
