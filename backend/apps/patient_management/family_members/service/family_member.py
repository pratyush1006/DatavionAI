"""
Business services for the Family Members module.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.family_members.models import FamilyMember

__all__ = [
    "create_family_member",
    "delete_family_member",
    "mark_as_emergency_contact",
    "mark_as_next_of_kin",
    "remove_emergency_contact",
    "remove_next_of_kin",
    "restore_family_member",
    "update_family_member",
]


@transaction.atomic
def create_family_member(
    **validated_data,
) -> FamilyMember:
    """
    Create a family member.
    """
    family_member = FamilyMember.objects.create(
        **validated_data,
    )

    return family_member


@transaction.atomic
def update_family_member(
    family_member: FamilyMember,
    **validated_data,
) -> FamilyMember:
    """
    Update a family member.
    """
    for field, value in validated_data.items():
        setattr(
            family_member,
            field,
            value,
        )

    family_member.save(
        update_fields=list(validated_data.keys()),
    )

    return family_member


@transaction.atomic
def delete_family_member(
    family_member: FamilyMember,
) -> None:
    """
    Soft delete a family member.
    """
    family_member.delete()


@transaction.atomic
def restore_family_member(
    family_member: FamilyMember,
) -> FamilyMember:
    """
    Restore a soft-deleted family member.
    """
    family_member.restore()

    return family_member


@transaction.atomic
def mark_as_next_of_kin(
    family_member: FamilyMember,
) -> FamilyMember:
    """
    Mark a family member as the patient's next of kin.
    Only one next of kin is allowed per patient.
    """
    FamilyMember.objects.filter(
        patient=family_member.patient,
        is_next_of_kin=True,
    ).exclude(
        id=family_member.id,
    ).update(
        is_next_of_kin=False,
    )

    family_member.is_next_of_kin = True

    family_member.save(
        update_fields=[
            "is_next_of_kin",
        ],
    )

    return family_member


@transaction.atomic
def remove_next_of_kin(
    family_member: FamilyMember,
) -> FamilyMember:
    """
    Remove next of kin designation.
    """
    family_member.is_next_of_kin = False

    family_member.save(
        update_fields=[
            "is_next_of_kin",
        ],
    )

    return family_member


@transaction.atomic
def mark_as_emergency_contact(
    family_member: FamilyMember,
) -> FamilyMember:
    """
    Mark as emergency contact.
    """
    family_member.is_emergency_contact = True

    family_member.save(
        update_fields=[
            "is_emergency_contact",
        ],
    )

    return family_member


@transaction.atomic
def remove_emergency_contact(
    family_member: FamilyMember,
) -> FamilyMember:
    """
    Remove emergency contact designation.
    """
    family_member.is_emergency_contact = False

    family_member.save(
        update_fields=[
            "is_emergency_contact",
        ],
    )

    return family_member
