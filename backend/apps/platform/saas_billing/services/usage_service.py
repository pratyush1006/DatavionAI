"""
Usage services.

Business logic layer for DatavionOS SaaS usage tracking.

Responsibilities:

- Track organization resource usage
- Maintain usage counters
- Calculate billable usage
- Validate subscription quotas
- Support healthcare modules
- Support AI metering

Architecture:

Healthcare Module
        |
UsageService
        |
Usage Workflow
        |
Usage Records
        |
Billing Calculation
"""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.platform.saas_billing.models import (
    Subscription,
    Usage,
)


class UsageService:
    """
    Enterprise SaaS usage service.
    """

    @staticmethod
    @transaction.atomic
    def record_usage(
        *,
        organization,
        metric_type: str,
        value: Decimal,
        unit: str = "count",
        source: str = "",
        reference_id: str = "",
        is_billable: bool = False,
        billing_rate: Decimal = Decimal("0"),
        metadata: dict | None = None,
    ) -> Usage:
        """
        Create usage record.

        Used by:

        - Patient Management
        - Appointment System
        - Laboratory
        - Pharmacy
        - AI Platform
        - Workflow Engine
        """

        if value < 0:
            raise ValueError(
                "Usage value cannot be negative.",
            )

        now = timezone.now()

        calculated_cost = Decimal(
            "0",
        )

        if is_billable:
            calculated_cost = value * billing_rate

        return Usage.objects.create(
            tenant=(organization.tenant),
            organization=organization,
            metric_type=metric_type,
            value=value,
            unit=unit,
            is_billable=is_billable,
            billing_rate=billing_rate,
            calculated_cost=calculated_cost,
            period_start=now,
            period_end=now,
            source=source,
            reference_id=reference_id,
            metadata=metadata or {},
        )

    @staticmethod
    @transaction.atomic
    def increment_usage(
        *,
        organization,
        metric_type: str,
        value: Decimal,
        unit: str = "count",
    ) -> Usage:
        """
        Increment usage counter.
        """

        usage = (
            Usage.objects.filter(
                organization=organization,
                metric_type=metric_type,
            )
            .order_by(
                "-created_at",
            )
            .first()
        )

        if usage:
            usage.value += value

            usage.save(
                update_fields=[
                    "value",
                    "updated_at",
                ],
            )

            return usage

        return UsageService.record_usage(
            organization=organization,
            metric_type=metric_type,
            value=value,
            unit=unit,
        )

    @staticmethod
    def get_usage_total(
        *,
        organization,
        metric_type: str,
        start=None,
        end=None,
    ) -> Decimal:
        """
        Calculate total usage.
        """

        queryset = Usage.objects.filter(
            organization=organization,
            metric_type=metric_type,
        )

        if start:
            queryset = queryset.filter(
                period_start__gte=start,
            )

        if end:
            queryset = queryset.filter(
                period_end__lte=end,
            )

        result = queryset.aggregate(
            total=Sum(
                "value",
            )
        )

        return result["total"] or Decimal("0")

    @staticmethod
    def calculate_billable_cost(
        *,
        organization,
    ) -> Decimal:
        """
        Calculate billable usage cost.
        """

        result = Usage.objects.filter(
            organization=organization,
            is_billable=True,
        ).aggregate(
            total=Sum(
                "calculated_cost",
            )
        )

        return result["total"] or Decimal("0")

    @staticmethod
    def check_limit(
        *,
        subscription: Subscription,
        metric_type: str,
        requested_value: Decimal = Decimal("1"),
    ) -> bool:
        """
        Validate subscription quota.
        """

        limits = subscription.plan_snapshot.get(
            "limits",
            {},
        )

        metric_mapping = {
            "USERS": "users",
            "PATIENTS": "patients",
            "STORAGE_GB": "storage_gb",
            "API_CALLS": "api_requests",
            "AI_REQUESTS": "ai_requests",
        }

        limit_key = metric_mapping.get(
            metric_type,
        )

        if not limit_key:
            return True

        max_allowed = limits.get(
            limit_key,
        )

        if max_allowed is None:
            return True

        current_usage = UsageService.get_usage_total(
            organization=(subscription.organization),
            metric_type=metric_type,
        )

        return current_usage + requested_value <= max_allowed

    @staticmethod
    def usage_summary(
        *,
        organization,
    ) -> dict:
        """
        Generate usage dashboard summary.
        """

        records = (
            Usage.objects.filter(
                organization=organization,
            )
            .values(
                "metric_type",
            )
            .annotate(
                total=Sum(
                    "value",
                ),
            )
        )

        return {item["metric_type"]: item["total"] for item in records}

    @staticmethod
    def ai_usage_summary(
        *,
        organization,
    ) -> dict:
        """
        AI workload metering summary.
        """

        metrics = [
            "AI_REQUESTS",
            "AI_TOKENS",
            "AI_DOCUMENTS",
        ]

        return {
            metric: (
                UsageService.get_usage_total(
                    organization=organization,
                    metric_type=metric,
                )
            )
            for metric in metrics
        }


__all__ = [
    "UsageService",
]
