"""
Managers and querysets for Patient Family Members.
"""

from __future__ import annotations

from uuid import UUID

from django.db import models

from apps.patient_management.family_members.constants import FamilyMemberStatus


class FamilyMemberQuerySet(models.QuerySet):
    """Reusable query primitives for family members."""

    def active(self) -> FamilyMemberQuerySet:
        return self.filter(
            status=FamilyMemberStatus.ACTIVE,
            is_active=True,
        )

    def inactive(self) -> FamilyMemberQuerySet:
        return self.filter(
            status=FamilyMemberStatus.INACTIVE,
        )

    def deleted(self) -> FamilyMemberQuerySet:
        return self.filter(is_deleted=True)

    def living(self) -> FamilyMemberQuerySet:
        return self.filter(is_living=True)

    def deceased(self) -> FamilyMemberQuerySet:
        return self.filter(is_living=False)

    def emergency_contacts(self) -> FamilyMemberQuerySet:
        return self.filter(is_emergency_contact=True)

    def next_of_kin(self) -> FamilyMemberQuerySet:
        return self.filter(is_next_of_kin=True)

    def for_patient(
        self,
        patient_id: UUID,
    ) -> FamilyMemberQuerySet:
        return self.filter(patient_id=patient_id)

    def for_organization(
        self,
        organization_id: UUID,
    ) -> FamilyMemberQuerySet:
        return self.filter(organization_id=organization_id)

    def for_patient_in_organization(
        self,
        *,
        organization_id: UUID,
        patient_id: UUID,
    ) -> FamilyMemberQuerySet:
        return self.filter(
            organization_id=organization_id,
            patient_id=patient_id,
        )

    def search(
        self,
        query: str,
    ) -> FamilyMemberQuerySet:
        query = (query or "").strip()

        if not query:
            return self

        return self.filter(
            models.Q(first_name__icontains=query)
            | models.Q(middle_name__icontains=query)
            | models.Q(last_name__icontains=query)
            | models.Q(mobile_number__icontains=query)
            | models.Q(email__icontains=query)
            | models.Q(family_member_number__icontains=query)
        )


class FamilyMemberManager(
    models.Manager.from_queryset(FamilyMemberQuerySet),
):
    """Default manager exposing only non-deleted family members."""

    def get_queryset(self) -> FamilyMemberQuerySet:
        return super().get_queryset().filter(is_deleted=False)


class DeletedFamilyMemberManager(
    models.Manager.from_queryset(FamilyMemberQuerySet),
):
    """Manager exposing only soft-deleted family members."""

    def get_queryset(self) -> FamilyMemberQuerySet:
        return super().get_queryset().filter(is_deleted=True)


__all__ = (
    "DeletedFamilyMemberManager",
    "FamilyMemberManager",
    "FamilyMemberQuerySet",
)
