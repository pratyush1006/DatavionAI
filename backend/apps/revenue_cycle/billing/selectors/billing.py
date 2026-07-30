"""
Billing Batch selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.billing.models import BillingBatch


class BillingBatchSelector:
    """
    Read-only queries for billing batch records.
    """

    @staticmethod
    def queryset() -> QuerySet[BillingBatch]:
        return BillingBatch.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        batch_id: UUID,
    ) -> BillingBatch:
        return get_object_or_404(
            BillingBatchSelector.queryset(),
            pk=batch_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[BillingBatch]:
        return BillingBatchSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[BillingBatch]:
        return BillingBatchSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "BillingBatchSelector",
]
