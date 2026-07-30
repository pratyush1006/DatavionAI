"""
RCM Metric selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.analytics.models import RcmMetric


class RcmMetricSelector:
    """
    Read-only queries for rcm metric records.
    """

    @staticmethod
    def queryset() -> QuerySet[RcmMetric]:
        return RcmMetric.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        metric_id: UUID,
    ) -> RcmMetric:
        return get_object_or_404(
            RcmMetricSelector.queryset(),
            pk=metric_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[RcmMetric]:
        return RcmMetricSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[RcmMetric]:
        return RcmMetricSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "RcmMetricSelector",
]
