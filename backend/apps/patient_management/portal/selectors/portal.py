"""
Portal Account selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.portal.models import PatientPortalAccount
from apps.platform.organizations.models import Organization


class PatientPortalAccountSelector:
    """
    Read-only queries for portal account records.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientPortalAccount]:
        return PatientPortalAccount.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        portal_account_id: UUID,
    ) -> PatientPortalAccount:
        return get_object_or_404(
            PatientPortalAccountSelector.queryset(),
            pk=portal_account_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[PatientPortalAccount]:
        return PatientPortalAccountSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[PatientPortalAccount]:
        return PatientPortalAccountSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "PatientPortalAccountSelector",
]
