"""Services for Revenue Analytics snapshot generation."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from django.db import transaction

from .constants import AnalyticsPeriod
from .events import publish_revenue_analytics_event
from .models import RevenueMetricSnapshot


class RevenueAnalyticsService:
    """Generate deterministic organization-scoped KPI snapshots."""

    @staticmethod
    @transaction.atomic
    def create_snapshot(
        *,
        organization: Any,
        period: str,
        period_start: date,
        period_end: date,
        gross_charges: Decimal = Decimal("0.00"),
        payments: Decimal = Decimal("0.00"),
        adjustments: Decimal = Decimal("0.00"),
        denials: Decimal = Decimal("0.00"),
        write_offs: Decimal = Decimal("0.00"),
        outstanding_ar: Decimal = Decimal("0.00"),
        encounter_count: int = 0,
        claim_count: int = 0,
        denied_claim_count: int = 0,
        paid_claim_count: int = 0,
        actor: Any = None,
    ) -> RevenueMetricSnapshot:
        """Create or return the unique snapshot for a reporting period."""

        if period not in AnalyticsPeriod.values:
            raise ValueError("Unsupported analytics period.")
        if period_end < period_start:
            raise ValueError("period_end cannot precede period_start.")

        monetary_values = {
            "gross_charges": gross_charges,
            "payments": payments,
            "adjustments": adjustments,
            "denials": denials,
            "write_offs": write_offs,
            "outstanding_ar": outstanding_ar,
        }
        if any(value < 0 for value in monetary_values.values()):
            raise ValueError("Analytics monetary values cannot be negative.")

        count_values = {
            "encounter_count": encounter_count,
            "claim_count": claim_count,
            "denied_claim_count": denied_claim_count,
            "paid_claim_count": paid_claim_count,
        }
        if any(value < 0 for value in count_values.values()):
            raise ValueError("Analytics counts cannot be negative.")

        snapshot, created = RevenueMetricSnapshot.objects.get_or_create(
            organization=organization,
            period=period,
            period_start=period_start,
            period_end=period_end,
            defaults={
                **monetary_values,
                **count_values,
            },
        )

        if not created:
            raise ValueError("An analytics snapshot already exists for this period.")

        publish_revenue_analytics_event(
            event_type="revenue_cycle.analytics.snapshot_created",
            aggregate_id=snapshot.id,
            payload={
                "organization_id": str(organization.id),
                "period": period,
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "generated_by": str(actor.id) if actor else None,
            },
        )
        return snapshot


__all__ = ("RevenueAnalyticsService",)
