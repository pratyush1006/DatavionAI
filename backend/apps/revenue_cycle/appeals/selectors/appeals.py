"""
Claim Appeal selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.appeals.models import ClaimAppeal


class ClaimAppealSelector:
    """
    Read-only queries for claim appeal records.
    """

    @staticmethod
    def queryset() -> QuerySet[ClaimAppeal]:
        return ClaimAppeal.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        appeal_id: UUID,
    ) -> ClaimAppeal:
        return get_object_or_404(
            ClaimAppealSelector.queryset(),
            pk=appeal_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[ClaimAppeal]:
        return ClaimAppealSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[ClaimAppeal]:
        return ClaimAppealSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "ClaimAppealSelector",
]
