"""
Coding Entry selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.coding.models import ChargeCoding


class ChargeCodingSelector:
    """
    Read-only queries for coding entry records.
    """

    @staticmethod
    def queryset() -> QuerySet[ChargeCoding]:
        return ChargeCoding.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        coding_id: UUID,
    ) -> ChargeCoding:
        return get_object_or_404(
            ChargeCodingSelector.queryset(),
            pk=coding_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[ChargeCoding]:
        return ChargeCodingSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[ChargeCoding]:
        return ChargeCodingSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "ChargeCodingSelector",
]
