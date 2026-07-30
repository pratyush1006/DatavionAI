"""
Claim Denial selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.denials.models import ClaimDenial
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class ClaimDenialSelector:
    """
    Read-only queries for claim denial records.
    """

    @staticmethod
    def queryset() -> QuerySet[ClaimDenial]:
        return ClaimDenial.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        denial_id: UUID,
    ) -> ClaimDenial:
        return get_object_or_404(
            ClaimDenialSelector.queryset(),
            pk=denial_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[ClaimDenial]:
        return ClaimDenialSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[ClaimDenial]:
        return ClaimDenialSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "ClaimDenialSelector",
]
