"""
Plan creation workflow.

Creates DatavionOS SaaS billing plans.

Workflow:

Plan Create Request
        |
Validate Plan Data
        |
PlanService
        |
Create Plan
        |
Publish PlanCreated Event
        |
Return Plan
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    PlanCreated,
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


class CreatePlanWorkflow(
    BaseWorkflow,
):
    """
    Enterprise SaaS plan creation workflow.

    Handles:

    - Platform plan creation
    - Default plan provisioning
    - Pricing catalog updates
    - Event publishing
    """

    def handle(
        self,
        *,
        data: dict,
    ) -> Plan:
        """
        Execute plan creation.
        """

        if not data:
            raise ValueError(
                "Plan data is required.",
            )

        code = data.get(
            "code",
        )

        if not code:
            raise ValueError(
                "Plan code is required.",
            )

        plan = PlanService.create_plan(
            data=data,
        )

        self.publish_event(
            PlanCreated(
                aggregate_id=plan.id,
                metadata={
                    "plan_code": plan.code,
                    "plan_name": plan.name,
                },
            )
        )

        return plan


__all__ = [
    "CreatePlanWorkflow",
]
