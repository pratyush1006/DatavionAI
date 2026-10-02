"""Selectors for organization-scoped emergency records."""

from __future__ import annotations

from uuid import UUID

from apps.patient_management.emergency.models import EmergencyContact


class EmergencySelector:
    """Read emergency records without performing mutations."""

    @staticmethod
    def queryset(*, organization):
        """Return non-deleted emergency records for an organization."""

        return EmergencyContact.objects.filter(
            organization=organization,
            is_deleted=False,
        ).select_related("patient")

    @classmethod
    def get(cls, *, organization, emergency_id: UUID) -> EmergencyContact:
        """Return one organization-scoped emergency record."""

        return cls.queryset(organization=organization).get(id=emergency_id)

    @classmethod
    def for_patient(cls, *, organization, patient_id: UUID):
        """Return emergency records for one organization-scoped patient."""

        return cls.queryset(organization=organization).filter(
            patient_id=patient_id,
        )


__all__ = ("EmergencySelector",)
