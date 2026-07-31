"""
Plan deactivation workflow.

Deactivates DatavionOS SaaS billing plans.

Workflow:

Deactivate Request
        |
Validate Plan
        |
Deactivate Plan
        |
Publish PlanDeactivated Event
        |
Return Plan
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    PlanDeactivated,
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


class DeactivatePlanWorkflow(
    BaseWorkflow,
):
    """
    Enterprise SaaS plan deactivation workflow.
    """

    def handle(
        self,
        *,
        plan: Plan,
    ) -> Plan:
        """
        Execute plan deactivation.
        """

        if not plan:
            raise ValueError(
                "Plan is required.",
            )

        plan = PlanService.deactivate(
            plan=plan,
        )

        self.publish_event(
            PlanDeactivated(
                aggregate_id=plan.id,
                metadata={
                    "plan_code": plan.code,
                },
            )
        )

        return plan


__all__ = [
    "DeactivatePlanWorkflow",
]
