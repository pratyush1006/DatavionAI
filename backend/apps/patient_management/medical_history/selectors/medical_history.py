"""
Medical History selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.medical_history.models import PatientMedicalHistory
from apps.platform.organizations.models import Organization


class PatientMedicalHistorySelector:
    """
    Read-only queries for medical history records.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientMedicalHistory]:
        return PatientMedicalHistory.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        medical_history_id: UUID,
    ) -> PatientMedicalHistory:
        return get_object_or_404(
            PatientMedicalHistorySelector.queryset(),
            pk=medical_history_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[PatientMedicalHistory]:
        return PatientMedicalHistorySelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[PatientMedicalHistory]:
        return PatientMedicalHistorySelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "PatientMedicalHistorySelector",
]
