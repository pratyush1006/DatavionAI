"""
Managers and querysets for Emergency Contacts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast
from uuid import UUID

from django.db import models

if TYPE_CHECKING:
    from apps.patient_management.patients.models import Patient
    from apps.platform.organizations.models import Organization


class EmergencyContactQuerySet(
    models.QuerySet,
):
    """Queryset helpers for EmergencyContact."""

    def active(
        self,
    ) -> EmergencyContactQuerySet:
        return self.filter(status="ACTIVE")

    def inactive(
        self,
    ) -> EmergencyContactQuerySet:
        return self.filter(status="INACTIVE")

    def blocked(
        self,
    ) -> EmergencyContactQuerySet:
        return self.filter(status="BLOCKED")

    def verified(
        self,
    ) -> EmergencyContactQuerySet:
        return self.filter(is_verified=True)

    def unverified(
        self,
    ) -> EmergencyContactQuerySet:
        return self.filter(is_verified=False)

    def primary(
        self,
    ) -> EmergencyContactQuerySet:
        return self.filter(is_primary=True)

    def legal_guardians(
        self,
    ) -> EmergencyContactQuerySet:
        return self.filter(is_legal_guardian=True)

    def medical_power_of_attorney(
        self,
    ) -> EmergencyContactQuerySet:
        return self.filter(
            has_medical_power_of_attorney=True,
        )

    def for_patient(
        self,
        patient: Patient | UUID,
    ) -> EmergencyContactQuerySet:
        return self.filter(patient=patient)

    def for_patient_in_organization(
        self,
        *,
        patient_id: UUID,
        organization_id: UUID,
    ) -> EmergencyContactQuerySet:
        return self.filter(
            patient_id=patient_id,
            organization_id=organization_id,
        )

    def for_organization(
        self,
        organization: Organization | UUID,
    ) -> EmergencyContactQuerySet:
        return self.filter(
            organization=organization,
        )

    def search(
        self,
        query: str,
    ) -> EmergencyContactQuerySet:
        query = query.strip()

        if not query:
            return self

        return self.filter(
            models.Q(first_name__icontains=query)
            | models.Q(middle_name__icontains=query)
            | models.Q(last_name__icontains=query)
            | models.Q(
                mobile_number__icontains=query,
            )
            | models.Q(
                alternate_mobile_number__icontains=query,
            )
            | models.Q(
                home_phone__icontains=query,
            )
            | models.Q(
                work_phone__icontains=query,
            )
            | models.Q(email__icontains=query)
            | models.Q(
                emergency_contact_number__icontains=query,
            )
        ).distinct()

    def with_related(
        self,
    ) -> EmergencyContactQuerySet:
        return self.select_related(
            "organization",
            "patient",
            "verified_by",
        )


class EmergencyContactManager(models.Manager):
    """Concrete migration-serializable manager class."""

    def get_queryset(self) -> EmergencyContactQuerySet:
        return cast(EmergencyContactQuerySet, super().get_queryset())


__all__ = [
    "EmergencyContactManager",
    "EmergencyContactQuerySet",
]
