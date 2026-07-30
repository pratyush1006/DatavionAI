"""
Referral selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.referrals.models import PatientReferral
from apps.platform.organizations.models import Organization


class PatientReferralSelector:
    """
    Read-only queries for referral records.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientReferral]:
        return PatientReferral.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        referral_id: UUID,
    ) -> PatientReferral:
        return get_object_or_404(
            PatientReferralSelector.queryset(),
            pk=referral_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[PatientReferral]:
        return PatientReferralSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[PatientReferral]:
        return PatientReferralSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "PatientReferralSelector",
]
