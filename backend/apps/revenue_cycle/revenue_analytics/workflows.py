"""Workflow orchestration for Revenue Analytics."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from .policies import RevenueAnalyticsPolicy
from .services import RevenueAnalyticsService


class RevenueAnalyticsWorkflow:
    """Orchestrate authorized analytics snapshot generation."""

    @staticmethod
    def generate(
        *,
        user: Any,
        organization: Any,
        period: str,
        period_start: date,
        period_end: date,
        gross_charges: Decimal,
        payments: Decimal,
        adjustments: Decimal,
        denials: Decimal,
        write_offs: Decimal,
        outstanding_ar: Decimal,
        encounter_count: int,
        claim_count: int,
        denied_claim_count: int,
        paid_claim_count: int,
    ) -> Any:
        """Authorize and generate a Revenue Analytics snapshot."""

        if not RevenueAnalyticsPolicy.can_generate(
            user=user,
            organization=organization,
        ):
            raise PermissionError(
                "Revenue Analytics generation permission is required."
            )

        return RevenueAnalyticsService.create_snapshot(
            organization=organization,
            period=period,
            period_start=period_start,
            period_end=period_end,
            gross_charges=gross_charges,
            payments=payments,
            adjustments=adjustments,
            denials=denials,
            write_offs=write_offs,
            outstanding_ar=outstanding_ar,
            encounter_count=encounter_count,
            claim_count=claim_count,
            denied_claim_count=denied_claim_count,
            paid_claim_count=paid_claim_count,
            actor=user,
        )


__all__ = ("RevenueAnalyticsWorkflow",)
