"""
Usage managers.

Provides reusable queryset operations
for DatavionOS SaaS resource consumption.

Responsibilities:

- Usage metric filtering
- Tenant usage queries
- Organization usage analytics
- Billing usage calculation
- Quota monitoring
- AI metering
- Healthcare usage reporting
"""

from __future__ import annotations

from django.db import models


class UsageQuerySet(
    models.QuerySet,
):
    """
    Usage queryset helpers.
    """

    # --------------------------------------------------------------
    # Ownership
    # --------------------------------------------------------------

    def by_tenant(
        self,
        tenant,
    ):
        """
        Filter usage by tenant.
        """

        return self.filter(
            tenant=tenant,
        )

    def by_organization(
        self,
        organization,
    ):
        """
        Filter usage by organization.
        """

        return self.filter(
            organization=organization,
        )

    # --------------------------------------------------------------
    # Metric
    # --------------------------------------------------------------

    def by_metric(
        self,
        metric_type: str,
    ):
        """
        Filter usage by metric type.
        """

        return self.filter(
            metric_type=metric_type,
        )

    def billable(
        self,
    ):
        """
        Return billable usage.
        """

        return self.filter(
            is_billable=True,
        )

    def non_billable(
        self,
    ):
        """
        Return non billable usage.
        """

        return self.filter(
            is_billable=False,
        )

    # --------------------------------------------------------------
    # Billing Period
    # --------------------------------------------------------------

    def current_period(
        self,
        start,
        end,
    ):
        """
        Return usage inside billing period.
        """

        return self.filter(
            period_start__gte=start,
            period_end__lte=end,
        )

    def overlapping_period(
        self,
        start,
        end,
    ):
        """
        Return usage overlapping period.
        """

        return self.filter(
            period_start__lte=end,
            period_end__gte=start,
        )

    # --------------------------------------------------------------
    # Common Metrics
    # --------------------------------------------------------------

    def users(
        self,
    ):
        return self.by_metric(
            "USERS",
        )

    def storage(
        self,
    ):
        return self.by_metric(
            "STORAGE_GB",
        )

    def patients(
        self,
    ):
        return self.by_metric(
            "PATIENTS",
        )

    def appointments(
        self,
    ):
        return self.by_metric(
            "APPOINTMENTS",
        )

    def prescriptions(
        self,
    ):
        return self.by_metric(
            "PRESCRIPTIONS",
        )

    def pharmacy_orders(
        self,
    ):
        return self.by_metric(
            "PHARMACY_ORDERS",
        )

    def inventory_transactions(
        self,
    ):
        return self.by_metric(
            "INVENTORY_TRANSACTIONS",
        )

    # --------------------------------------------------------------
    # AI Usage
    # --------------------------------------------------------------

    def ai_requests(
        self,
    ):
        return self.by_metric(
            "AI_REQUESTS",
        )

    def ai_tokens(
        self,
    ):
        return self.by_metric(
            "AI_TOKENS",
        )

    # --------------------------------------------------------------
    # Quota
    # --------------------------------------------------------------

    def exceeded_quota(
        self,
    ):
        """
        Return usage where consumed
        value exceeds configured limit.
        """

        return self.filter(
            value__gt=models.F(
                "billing_rate",
            ),
        )

    # --------------------------------------------------------------
    # Cost
    # --------------------------------------------------------------

    def with_cost(
        self,
    ):
        """
        Return billable usage records
        having calculated cost.
        """

        return self.filter(
            is_billable=True,
            calculated_cost__gt=0,
        )

    def expensive(
        self,
        amount,
    ):
        """
        Filter high cost usage.
        """

        return self.filter(
            calculated_cost__gte=amount,
        )

    # --------------------------------------------------------------
    # Reporting
    # --------------------------------------------------------------

    def latest(
        self,
        limit: int = 10,
    ):
        """
        Return latest usage records.
        """

        return self.order_by(
            "-created_at",
        )[:limit]

    def recent_periods(
        self,
        limit: int = 10,
    ):
        """
        Return recent billing periods.
        """

        return self.order_by(
            "-period_start",
        )[:limit]


class UsageManager(
    models.Manager,
):
    """
    Manager for Usage model.
    """

    def get_queryset(
        self,
    ):
        return UsageQuerySet(
            self.model,
            using=self._db,
        )

    def organization_usage(
        self,
        organization,
    ):
        """
        Return organization usage.
        """

        return self.get_queryset().by_organization(
            organization,
        )

    def billable_usage(
        self,
        organization,
    ):
        """
        Return billable organization usage.
        """

        return (
            self.get_queryset()
            .by_organization(
                organization,
            )
            .billable()
        )


__all__ = [
    "UsageManager",
    "UsageQuerySet",
]
