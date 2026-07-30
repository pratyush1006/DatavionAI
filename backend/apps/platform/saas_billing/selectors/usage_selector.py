"""
Usage selectors.

Read-only query layer for DatavionOS
SaaS usage tracking.

Responsibilities:

- Organization usage lookup
- Metric based filtering
- Billing period usage
- AI consumption queries
- Healthcare resource analytics
- Billable usage reporting

Architecture:

API
 |
Selectors
 |
Models
"""

from __future__ import annotations

from apps.platform.saas_billing.models import (
    Usage,
)


class UsageSelector:
    """
    Usage read operations.
    """

    @staticmethod
    def by_organization(
        *,
        organization,
    ):
        """
        Return organization usage records.
        """

        return Usage.objects.by_organization(
            organization,
        ).order_by(
            "-created_at",
        )

    @staticmethod
    def by_metric(
        *,
        organization,
        metric_type: str,
    ):
        """
        Return usage by metric.

        Examples:

        USERS
        PATIENTS
        AI_REQUESTS
        STORAGE_GB
        """

        return Usage.objects.by_organization(
            organization,
        ).by_metric(
            metric_type,
        )

    @staticmethod
    def current_period(
        *,
        organization,
        start,
        end,
    ):
        """
        Return usage inside billing period.
        """

        return Usage.objects.by_organization(
            organization,
        ).current_period(
            start,
            end,
        )

    @staticmethod
    def billable_usage(
        *,
        organization,
    ):
        """
        Return usage contributing
        to billing.
        """

        return Usage.objects.filter(
            organization=organization,
            is_billable=True,
        ).order_by(
            "-created_at",
        )

    @staticmethod
    def ai_usage(
        *,
        organization,
    ):
        """
        Return AI consumption records.

        Includes:

        - AI Requests
        - AI Tokens
        - AI Documents
        """

        return Usage.objects.filter(
            organization=organization,
            metric_type__in=[
                Usage.MetricType.AI_REQUESTS,
                Usage.MetricType.AI_TOKENS,
                Usage.MetricType.AI_DOCUMENTS,
            ],
        )

    @staticmethod
    def healthcare_usage(
        *,
        organization,
    ):
        """
        Return healthcare module usage.

        Includes:

        - Patients
        - Appointments
        - Encounters
        - Prescriptions
        - Lab Orders
        - Imaging
        """

        return Usage.objects.filter(
            organization=organization,
            metric_type__in=[
                Usage.MetricType.PATIENTS,
                Usage.MetricType.APPOINTMENTS,
                Usage.MetricType.ENCOUNTERS,
                Usage.MetricType.PRESCRIPTIONS,
                Usage.MetricType.LAB_ORDERS,
                Usage.MetricType.IMAGING_STUDIES,
            ],
        )

    @staticmethod
    def pharmacy_usage(
        *,
        organization,
    ):
        """
        Return pharmacy usage.

        Includes:

        - Pharmacy Orders
        - Inventory Transactions
        - Billing Transactions
        """

        return Usage.objects.filter(
            organization=organization,
            metric_type__in=[
                Usage.MetricType.PHARMACY_ORDERS,
                Usage.MetricType.INVENTORY_TRANSACTIONS,
                Usage.MetricType.BILLING_TRANSACTIONS,
            ],
        )

    @staticmethod
    def latest(
        *,
        organization,
        limit: int = 10,
    ):
        """
        Return latest usage records.
        """

        return Usage.objects.by_organization(
            organization,
        ).latest(
            limit,
        )

    @staticmethod
    def exists(
        *,
        organization,
        metric_type: str,
    ) -> bool:
        """
        Check usage existence.
        """

        return Usage.objects.filter(
            organization=organization,
            metric_type=metric_type,
        ).exists()


__all__ = [
    "UsageSelector",
]
