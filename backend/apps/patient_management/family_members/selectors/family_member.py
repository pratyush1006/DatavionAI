"""
Selectors for the Family Members module.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.patient_management.family_members.models import FamilyMember

__all__ = [
    "count_patient_family_members",
    "get_emergency_contact_family_members",
    "get_family_member_by_id",
    "get_next_of_kin",
    "list_family_members",
    "list_organization_family_members",
    "list_patient_family_members",
    "search_family_members",
]


def get_family_member_by_id(
    family_member_id,
) -> FamilyMember:
    """
    Return a family member by its unique identifier.
    """
    return get_object_or_404(
        FamilyMember.objects.select_related(
            "organization",
            "patient",
        ),
        id=family_member_id,
    )


def list_family_members() -> QuerySet[FamilyMember]:
    """
    Return all active family members.
    """
    return (
        FamilyMember.objects.select_related(
            "organization",
            "patient",
        )
        .all()
        .order_by(
            "first_name",
            "last_name",
        )
    )


def list_patient_family_members(
    patient_id,
) -> QuerySet[FamilyMember]:
    """
    Return family members belonging to a patient.
    """
    return (
        FamilyMember.objects.for_patient(
            patient_id,
        )
        .select_related(
            "organization",
            "patient",
        )
        .order_by(
            "relationship",
            "first_name",
        )
    )


def list_organization_family_members(
    organization_id,
) -> QuerySet[FamilyMember]:
    """
    Return family members for an organization.
    """
    return (
        FamilyMember.objects.for_organization(
            organization_id,
        )
        .select_related(
            "patient",
        )
        .order_by(
            "patient",
            "first_name",
        )
    )


def search_family_members(
    query: str,
) -> QuerySet[FamilyMember]:
    """
    Search family members.
    """
    return (
        FamilyMember.objects.search(
            query,
        )
        .select_related(
            "organization",
            "patient",
        )
        .order_by(
            "first_name",
        )
    )


def get_next_of_kin(
    patient_id,
) -> QuerySet[FamilyMember]:
    """
    Return the patient's next of kin.
    """
    return FamilyMember.objects.for_patient(
        patient_id,
    ).next_of_kin()


def get_emergency_contact_family_members(
    patient_id,
) -> QuerySet[FamilyMember]:
    """
    Return family members marked as emergency contacts.
    """
    return FamilyMember.objects.for_patient(
        patient_id,
    ).emergency_contacts()


def count_patient_family_members(
    patient_id,
) -> int:
    """
    Return the total number of active family members.
    """
    return FamilyMember.objects.for_patient(
        patient_id,
    ).count()
