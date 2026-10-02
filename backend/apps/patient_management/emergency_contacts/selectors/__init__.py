"""
Organization-scoped selectors for Emergency Contacts.

The EmergencyContactSelector class is the canonical tenant-aware selector.

Module-level functions are compatibility facades for the existing public
selector API. They intentionally preserve the existing selector behavior
while delegating to the canonical selector implementation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from django.db.models import QuerySet

from ..models import EmergencyContact

if TYPE_CHECKING:
    from apps.patient_management.patients.models import Patient
    from apps.platform.organizations.models import Organization


class EmergencyContactSelector:
    """Read-only, organization-scoped EmergencyContact queries."""

    @staticmethod
    def queryset(
        *,
        organization: Organization,
    ) -> QuerySet[EmergencyContact]:
        """
        Return the active/default tenant-scoped queryset.

        EmergencyContact.objects.for_organization() and the model manager's
        default queryset preserve the bounded-context filtering semantics,
        including soft-delete exclusion.
        """
        return EmergencyContact.objects.for_organization(organization).with_related()

    @classmethod
    def get(
        cls,
        *,
        organization: Organization,
        emergency_contact_id: UUID,
    ) -> EmergencyContact:
        """Retrieve an emergency contact inside an organization boundary."""
        return cls.queryset(
            organization=organization,
        ).get(
            pk=emergency_contact_id,
        )

    @classmethod
    def list(
        cls,
        *,
        organization: Organization,
    ) -> QuerySet[EmergencyContact]:
        """List emergency contacts for an organization."""
        return cls.queryset(
            organization=organization,
        )

    @classmethod
    def list_by_patient(
        cls,
        *,
        organization: Organization,
        patient_id: UUID,
    ) -> QuerySet[EmergencyContact]:
        """List emergency contacts belonging to a patient."""
        return cls.queryset(
            organization=organization,
        ).filter(
            patient_id=patient_id,
        )

    @classmethod
    def get_primary(
        cls,
        *,
        organization: Organization,
        patient_id: UUID,
    ) -> EmergencyContact | None:
        """Return the primary emergency contact for a patient."""
        return (
            cls.list_by_patient(
                organization=organization,
                patient_id=patient_id,
            )
            .filter(is_primary=True)
            .first()
        )

    @classmethod
    def search(
        cls,
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[EmergencyContact]:
        """Search emergency contacts within an organization."""
        return cls.queryset(
            organization=organization,
        ).search(query)

    @classmethod
    def list_active(
        cls,
        *,
        organization: Organization,
    ) -> QuerySet[EmergencyContact]:
        """Return active emergency contacts."""
        return cls.queryset(
            organization=organization,
        ).active()

    @classmethod
    def list_verified(
        cls,
        *,
        organization: Organization,
    ) -> QuerySet[EmergencyContact]:
        """Return verified emergency contacts."""
        return cls.queryset(
            organization=organization,
        ).verified()


def get_emergency_contact_by_id(
    emergency_contact_id: UUID,
) -> EmergencyContact:
    """
    Retrieve an emergency contact by primary key.

    Compatibility facade for callers that do not yet provide an explicit
    organization boundary.
    """
    return EmergencyContact.objects.with_related().get(
        pk=emergency_contact_id,
    )


def get_emergency_contact_by_uuid(
    emergency_contact_uuid: UUID,
) -> EmergencyContact:
    """
    Backward-compatible UUID alias.

    EmergencyContact uses its UUID primary key, so this delegates directly
    to get_emergency_contact_by_id().
    """
    return get_emergency_contact_by_id(
        emergency_contact_uuid,
    )


def list_emergency_contacts() -> QuerySet[EmergencyContact]:
    """
    Return the default emergency-contact queryset.

    The model's default manager semantics are preserved, including
    exclusion of soft-deleted records.
    """
    return EmergencyContact.objects.with_related()


def list_patient_emergency_contacts(
    *,
    patient: Patient,
) -> QuerySet[EmergencyContact]:
    """Return emergency contacts belonging to the supplied patient."""
    return list_emergency_contacts().filter(
        patient_id=patient.pk,
    )


def list_organization_emergency_contacts(
    *,
    organization: Organization,
) -> QuerySet[EmergencyContact]:
    """Return emergency contacts belonging to the supplied organization."""
    return list_emergency_contacts().filter(
        organization_id=organization.pk,
    )


def get_primary_emergency_contact(
    *,
    patient: Patient,
) -> EmergencyContact | None:
    """Return the primary emergency contact for the supplied patient."""
    return (
        list_patient_emergency_contacts(
            patient=patient,
        )
        .filter(is_primary=True)
        .first()
    )


def search_emergency_contacts(
    *,
    search: str,
) -> QuerySet[EmergencyContact]:
    """
    Search emergency contacts using the canonical queryset search API.
    """
    return list_emergency_contacts().search(
        search,
    )


__all__ = (
    "EmergencyContactSelector",
    "get_emergency_contact_by_id",
    "get_emergency_contact_by_uuid",
    "get_primary_emergency_contact",
    "list_emergency_contacts",
    "list_organization_emergency_contacts",
    "list_patient_emergency_contacts",
    "search_emergency_contacts",
)
