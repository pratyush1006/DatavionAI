"""
Organization-scoped selectors for Emergency Contacts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from django.db.models import QuerySet

from ..models import EmergencyContact

if TYPE_CHECKING:
    from apps.platform.organizations.models import Organization


class EmergencyContactSelector:
    """Read-only, organization-scoped EmergencyContact queries."""

    @staticmethod
    def queryset(
        *,
        organization: Organization,
    ) -> QuerySet[EmergencyContact]:
        return EmergencyContact.objects.for_organization(organization).with_related()

    @classmethod
    def get(
        cls,
        *,
        organization: Organization,
        emergency_contact_id: UUID,
    ) -> EmergencyContact:
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
        return (
            cls.list_by_patient(
                organization=organization,
                patient_id=patient_id,
            )
            .primary()
            .first()
        )

    @classmethod
    def search(
        cls,
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[EmergencyContact]:
        return cls.queryset(
            organization=organization,
        ).search(query)

    @classmethod
    def list_active(
        cls,
        *,
        organization: Organization,
    ) -> QuerySet[EmergencyContact]:
        return cls.queryset(
            organization=organization,
        ).active()

    @classmethod
    def list_verified(
        cls,
        *,
        organization: Organization,
    ) -> QuerySet[EmergencyContact]:
        return cls.queryset(
            organization=organization,
        ).verified()


__all__ = [
    "EmergencyContactSelector",
]
