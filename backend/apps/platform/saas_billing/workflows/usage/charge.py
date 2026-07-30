"""
Usage charge workflow.

Calculates DatavionOS billable usage
charges for subscription billing.

Workflow:

Billable Usage
        |
Validate Usage
        |
Calculate Cost
        |
Publish UsageCharged Event
        |
Invoice Generation
"""

from __future__ import annotations

from decimal import Decimal

from apps.platform.saas_billing.events import (
    UsageCharged,
)
from apps.platform.saas_billing.models import (
    Usage,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class ChargeUsageWorkflow(
    BaseWorkflow,
):
    """
    Enterprise usage charging workflow.
    """

    def handle(
        self,
        *,
        usage: Usage,
        rate: Decimal | None = None,
    ) -> Usage:
        """
        Calculate usage based billing.

        Supports:

        - AI usage
        - API usage
        - Storage usage
        - Pharmacy transactions
        - Laboratory usage
        - Enterprise overages
        """

        if not usage:
            raise ValueError(
                "Usage record is required.",
            )

        # --------------------------------------------------------------
        # Skip non-billable usage
        # --------------------------------------------------------------

        if not usage.is_billable:
            return usage

        # --------------------------------------------------------------
        # Idempotency check
        # --------------------------------------------------------------

        if usage.calculated_cost:
            return usage

        # --------------------------------------------------------------
        # Resolve billing rate
        # --------------------------------------------------------------

        billing_rate = rate or usage.billing_rate

        if billing_rate <= 0:
            raise ValueError(
                "Billing rate must be greater than zero.",
            )

        # --------------------------------------------------------------
        # Calculate charge
        # --------------------------------------------------------------

        calculated_cost = usage.value * billing_rate

        usage.calculated_cost = calculated_cost

        usage.metadata = {
            **usage.metadata,
            "charge_calculated": True,
            "billing_rate": str(
                billing_rate,
            ),
            "calculated_cost": str(
                calculated_cost,
            ),
        }

        usage.save(
            update_fields=[
                "calculated_cost",
                "metadata",
                "updated_at",
            ],
        )

        # --------------------------------------------------------------
        # Publish event
        # --------------------------------------------------------------

        self.publish_event(
            UsageCharged(
                aggregate_id=(usage.id),
                metadata={
                    "organization_id": (str(usage.organization.id)),
                    "metric_type": (usage.metric_type),
                    "amount": (str(calculated_cost)),
                },
            )
        )

        return usage


__all__ = [
    "ChargeUsageWorkflow",
]
