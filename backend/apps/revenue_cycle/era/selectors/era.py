"""
Remittance Advice selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.era.models import RemittanceAdvice


class RemittanceAdviceSelector:
    """
    Read-only queries for remittance advice records.
    """

    @staticmethod
    def queryset() -> QuerySet[RemittanceAdvice]:
        return RemittanceAdvice.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        remittance_id: UUID,
    ) -> RemittanceAdvice:
        return get_object_or_404(
            RemittanceAdviceSelector.queryset(),
            pk=remittance_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[RemittanceAdvice]:
        return RemittanceAdviceSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[RemittanceAdvice]:
        return RemittanceAdviceSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "RemittanceAdviceSelector",
]
