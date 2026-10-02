"""
Usage evaluation workflow.

Evaluates DatavionOS resource consumption
against subscription entitlements.

Workflow:

Usage Record
      |
Load Subscription
      |
Resolve Usage Pricing Rules
      |
Calculate Overage
      |
Publish Usage Events
      |
Return Usage
"""

from __future__ import annotations

from decimal import Decimal

from apps.platform.saas_billing.events import (
    UsageEvaluated,
    UsageLimitExceeded,
)
from apps.platform.saas_billing.models import (
    Usage,
)
from apps.platform.saas_billing.services import (
    EntitlementService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class EvaluateUsageWorkflow(
    BaseWorkflow,
):
    """
    Enterprise usage evaluation workflow.

    Handles:

    - Included quota
    - Overage calculation
    - Usage billing rate
    - Billable usage detection
    """

    def handle(
        self,
        *,
        usage: Usage,
    ) -> Usage:
        """
        Evaluate usage against plan limits.
        """

        if not usage:
            raise ValueError(
                "Usage record is required.",
            )

        subscription = EntitlementService.get_subscription(
            organization=(usage.organization),
        )

        if not subscription:
            raise ValueError(
                "Organization subscription not found.",
            )

        plan = subscription.plan

        usage_config = plan.get_usage_limit(
            usage.metric_type,
        )

        included_limit = Decimal(
            str(
                usage_config.get(
                    "included",
                    0,
                )
            )
        )

        overage_rate = Decimal(
            str(
                usage_config.get(
                    "overage_rate",
                    0,
                )
            )
        )

        excess_usage = Decimal("0")

        calculated_cost = Decimal("0")

        is_billable = False

        if usage.value > included_limit:
            excess_usage = usage.value - included_limit

            if overage_rate > 0:
                is_billable = True

                calculated_cost = excess_usage * overage_rate

        usage.is_billable = is_billable

        usage.billing_rate = overage_rate

        usage.calculated_cost = calculated_cost

        usage.metadata = {
            **usage.metadata,
            "evaluated": True,
            "included_limit": (str(included_limit)),
            "overage_rate": (str(overage_rate)),
            "excess_usage": (str(excess_usage)),
            "calculated_cost": (str(calculated_cost)),
        }

        usage.save(
            update_fields=[
                "is_billable",
                "billing_rate",
                "calculated_cost",
                "metadata",
                "updated_at",
            ],
        )

        self.publish_event(
            UsageEvaluated(
                aggregate_id=(usage.id),
                metadata={
                    "metric_type": (usage.metric_type),
                    "is_billable": (is_billable),
                    "calculated_cost": (str(calculated_cost)),
                },
            )
        )

        if is_billable:
            self.publish_event(
                UsageLimitExceeded(
                    aggregate_id=(usage.id),
                    metadata={
                        "organization_id": (str(usage.organization.id)),
                        "metric_type": (usage.metric_type),
                        "excess_usage": (str(excess_usage)),
                        "calculated_cost": (str(calculated_cost)),
                    },
                )
            )

        return usage


__all__ = [
    "EvaluateUsageWorkflow",
]
