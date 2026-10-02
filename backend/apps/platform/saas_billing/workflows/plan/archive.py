"""
Plan archive workflow.

Archives DatavionOS SaaS billing plans.

Workflow:

Archive Request
        |
Validate Plan
        |
Archive Plan
        |
Publish PlanArchived Event
        |
Return Plan
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    PlanArchived,
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


class ArchivePlanWorkflow(
    BaseWorkflow,
):
    """
    Enterprise SaaS plan archive workflow.
    """

    def handle(
        self,
        *,
        plan: Plan,
    ) -> Plan:
        """
        Execute plan archive.
        """

        if not plan:
            raise ValueError(
                "Plan is required.",
            )

        plan = PlanService.archive(
            plan=plan,
        )

        self.publish_event(
            PlanArchived(
                aggregate_id=plan.id,
                metadata={
                    "plan_code": plan.code,
                },
            )
        )

        return plan


__all__ = [
    "ArchivePlanWorkflow",
]
