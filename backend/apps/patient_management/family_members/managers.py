"""
Managers and querysets for the Family Members module.
"""

from __future__ import annotations

from django.db import models

__all__ = [
    "DeletedFamilyMemberManager",
    "FamilyMemberManager",
    "FamilyMemberQuerySet",
]


class FamilyMemberQuerySet(models.QuerySet):
    """
    Custom queryset for FamilyMember.
    """

    def active(self) -> FamilyMemberQuerySet:
        """
        Return active family members.
        """
        return self.filter(
            is_active=True,
            is_deleted=False,
        )

    def inactive(self) -> FamilyMemberQuerySet:
        """
        Return inactive family members.
        """
        return self.filter(
            is_active=False,
            is_deleted=False,
        )

    def deleted(self) -> FamilyMemberQuerySet:
        """
        Return soft-deleted family members.
        """
        return self.filter(
            is_deleted=True,
        )

    def living(self) -> FamilyMemberQuerySet:
        """
        Return living family members.
        """
        return self.filter(
            is_living=True,
            is_deleted=False,
        )

    def deceased(self) -> FamilyMemberQuerySet:
        """
        Return deceased family members.
        """
        return self.filter(
            is_living=False,
            is_deleted=False,
        )

    def emergency_contacts(self) -> FamilyMemberQuerySet:
        """
        Return family members marked as emergency contacts.
        """
        return self.filter(
            is_emergency_contact=True,
            is_deleted=False,
        )

    def next_of_kin(self) -> FamilyMemberQuerySet:
        """
        Return next of kin.
        """
        return self.filter(
            is_next_of_kin=True,
            is_deleted=False,
        )

    def for_patient(
        self,
        patient_id,
    ) -> FamilyMemberQuerySet:
        """
        Return family members for a patient.
        """
        return self.filter(
            patient_id=patient_id,
            is_deleted=False,
        )

    def for_organization(
        self,
        organization_id,
    ) -> FamilyMemberQuerySet:
        """
        Return family members for an organization.
        """
        return self.filter(
            organization_id=organization_id,
            is_deleted=False,
        )

    def search(
        self,
        query: str,
    ) -> FamilyMemberQuerySet:
        """
        Search family members.
        """
        if not query:
            return self

        return self.filter(
            models.Q(first_name__icontains=query)
            | models.Q(middle_name__icontains=query)
            | models.Q(last_name__icontains=query)
            | models.Q(mobile_number__icontains=query)
            | models.Q(email__icontains=query)
            | models.Q(family_member_number__icontains=query),
            is_deleted=False,
        )


class FamilyMemberManager(models.Manager):
    """
    Default manager.
    """

    def get_queryset(self) -> FamilyMemberQuerySet:
        """
        Return active queryset.
        """
        return FamilyMemberQuerySet(
            self.model,
            using=self._db,
        ).filter(
            is_deleted=False,
        )

    def active(self) -> FamilyMemberQuerySet:
        return self.get_queryset().active()

    def inactive(self) -> FamilyMemberQuerySet:
        return self.get_queryset().inactive()

    def living(self) -> FamilyMemberQuerySet:
        return self.get_queryset().living()

    def deceased(self) -> FamilyMemberQuerySet:
        return self.get_queryset().deceased()

    def emergency_contacts(self) -> FamilyMemberQuerySet:
        return self.get_queryset().emergency_contacts()

    def next_of_kin(self) -> FamilyMemberQuerySet:
        return self.get_queryset().next_of_kin()

    def for_patient(
        self,
        patient_id,
    ) -> FamilyMemberQuerySet:
        return self.get_queryset().for_patient(
            patient_id,
        )

    def for_organization(
        self,
        organization_id,
    ) -> FamilyMemberQuerySet:
        return self.get_queryset().for_organization(
            organization_id,
        )

    def search(
        self,
        query: str,
    ) -> FamilyMemberQuerySet:
        return self.get_queryset().search(query)


class DeletedFamilyMemberManager(models.Manager):
    """
    Manager for deleted family members.
    """

    def get_queryset(self) -> FamilyMemberQuerySet:
        """
        Return deleted queryset.
        """
        return FamilyMemberQuerySet(
            self.model,
            using=self._db,
        ).filter(
            is_deleted=True,
        )
