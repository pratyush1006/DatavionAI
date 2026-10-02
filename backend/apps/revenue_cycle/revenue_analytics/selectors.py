"""Organization-scoped selectors for Revenue Analytics."""

from __future__ import annotations

from datetime import date
from uuid import UUID

from django.db.models import QuerySet

from .models import RevenueMetricSnapshot


class RevenueAnalyticsSelector:
    """Provide read-only analytics snapshot queries."""

    @staticmethod
    def snapshots(
        *,
        organization_id: UUID,
        period: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> QuerySet[RevenueMetricSnapshot]:
        """Return organization-scoped snapshots matching optional filters."""

        queryset = RevenueMetricSnapshot.objects.filter(
            organization_id=organization_id,
        )
        if period:
            queryset = queryset.filter(period=period)
        if start_date:
            queryset = queryset.filter(period_end__gte=start_date)
        if end_date:
            queryset = queryset.filter(period_start__lte=end_date)
        return queryset.order_by("-period_end", "-generated_at")

    @staticmethod
    def latest(
        *,
        organization_id: UUID,
        period: str,
    ) -> RevenueMetricSnapshot | None:
        """Return the latest snapshot for one organization and period."""

        return (
            RevenueMetricSnapshot.objects.filter(
                organization_id=organization_id,
                period=period,
            )
            .order_by("-period_end", "-generated_at")
            .first()
        )


__all__ = ("RevenueAnalyticsSelector",)
