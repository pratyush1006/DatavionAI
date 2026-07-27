"""
Insurance Verification selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.insurance_verification.models import InsuranceVerification
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class InsuranceVerificationSelector:
    """
    Read-only queries for insurance verification records.
    """

    @staticmethod
    def queryset() -> QuerySet[InsuranceVerification]:
        return InsuranceVerification.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        verification_id: UUID,
    ) -> InsuranceVerification:
        return get_object_or_404(
            InsuranceVerificationSelector.queryset(),
            pk=verification_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[InsuranceVerification]:
        return InsuranceVerificationSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[InsuranceVerification]:
        return InsuranceVerificationSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "InsuranceVerificationSelector",
]
