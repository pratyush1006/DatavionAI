"""
Communication selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.communication.models import PatientCommunication
from apps.platform.organizations.models import Organization


class PatientCommunicationSelector:
    """
    Read-only queries for communication records.
    """

    @staticmethod
    def queryset() -> QuerySet[PatientCommunication]:
        return PatientCommunication.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        communication_id: UUID,
    ) -> PatientCommunication:
        return get_object_or_404(
            PatientCommunicationSelector.queryset(),
            pk=communication_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[PatientCommunication]:
        return PatientCommunicationSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[PatientCommunication]:
        return PatientCommunicationSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "PatientCommunicationSelector",
]
