"""
Eligibility Check selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.eligibility.models import EligibilityCheck


class EligibilityCheckSelector:
    """
    Read-only queries for eligibility check records.
    """

    @staticmethod
    def queryset() -> QuerySet[EligibilityCheck]:
        return EligibilityCheck.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        eligibility_id: UUID,
    ) -> EligibilityCheck:
        return get_object_or_404(
            EligibilityCheckSelector.queryset(),
            pk=eligibility_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[EligibilityCheck]:
        return EligibilityCheckSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[EligibilityCheck]:
        return EligibilityCheckSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "EligibilityCheckSelector",
]
