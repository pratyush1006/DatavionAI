"""
Patient Profile selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.patient_management.profile.models import PatientProfile
from apps.platform.organizations.models import Organization
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class ProfileSelector:
    """
    Read-only queries for patient profiles.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientProfile]:
        return PatientProfile.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        profile_id: UUID,
    ) -> PatientProfile:
        return get_object_or_404(
            ProfileSelector.queryset(),
            pk=profile_id,
        )

    @staticmethod
    def get_for_patient(
        *,
        patient_id: UUID,
    ) -> PatientProfile:
        return get_object_or_404(
            ProfileSelector.queryset(),
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[PatientProfile]:
        return ProfileSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "ProfileSelector",
]
