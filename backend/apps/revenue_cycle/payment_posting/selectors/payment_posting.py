"""
Payment Posting selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.payment_posting.models import PaymentPosting


class PaymentPostingSelector:
    """
    Read-only queries for payment posting records.
    """

    @staticmethod
    def queryset() -> QuerySet[PaymentPosting]:
        return PaymentPosting.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        posting_id: UUID,
    ) -> PaymentPosting:
        return get_object_or_404(
            PaymentPostingSelector.queryset(),
            pk=posting_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[PaymentPosting]:
        return PaymentPostingSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[PaymentPosting]:
        return PaymentPostingSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "PaymentPostingSelector",
]
