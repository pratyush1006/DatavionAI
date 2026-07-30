"""
Usage collection workflow.

Captures DatavionOS resource consumption
from healthcare modules.

Workflow:

Module Event
      |
Validate Usage
      |
Usage Service
      |
Publish UsageRecorded Event
      |
Return Usage Record
"""

from __future__ import annotations

from decimal import Decimal

from apps.platform.saas_billing.events import (
    UsageRecorded,
)
from apps.platform.saas_billing.models import (
    Usage,
)
from apps.platform.saas_billing.services import (
    UsageService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class CollectUsageWorkflow(
    BaseWorkflow,
):
    """
    Enterprise usage collection workflow.
    """

    def handle(
        self,
        *,
        organization,
        metric_type: str,
        value: Decimal,
        department=None,
        module: str | None = None,
        source: str | None = None,
        reference_id: str | None = None,
        billable: bool = False,
    ) -> Usage:
        """
        Collect resource usage.

        Supports:

        - Patients
        - Appointments
        - Lab orders
        - Pharmacy transactions
        - AI requests
        - Storage
        - API usage
        """

        if not organization:
            raise ValueError(
                "Organization is required.",
            )

        if value < 0:
            raise ValueError(
                "Usage value cannot be negative.",
            )

        # --------------------------------------------------------------
        # Record usage
        # --------------------------------------------------------------

        usage = UsageService.record_usage(
            organization=organization,
            metric_type=metric_type,
            value=value,
            unit="count",
            source=(source or ""),
            reference_id=(reference_id or ""),
            is_billable=billable,
            metadata={
                "department_id": (str(department.id) if department else None),
                "module": module,
            },
        )

        # --------------------------------------------------------------
        # Publish event
        # --------------------------------------------------------------

        self.publish_event(
            UsageRecorded(
                aggregate_id=(usage.id),
                metadata={
                    "organization_id": (str(organization.id)),
                    "metric_type": (metric_type),
                    "value": (str(value)),
                    "module": module,
                },
            )
        )

        return usage


__all__ = [
    "CollectUsageWorkflow",
]
