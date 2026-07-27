"""
Services for Patient Relationships.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


@transaction.atomic
def create_relationship(
    **validated_data: object,
) -> PatientRelationship:
    """
    Create a patient relationship.
    """
    return PatientRelationship.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_relationship(
    *,
    relationship: PatientRelationship,
    **validated_data: object,
) -> PatientRelationship:
    """
    Update a patient relationship.
    """
    for field, value in validated_data.items():
        setattr(
            relationship,
            field,
            value,
        )

    relationship.save()

    return relationship


@transaction.atomic
def verify_relationship(
    *,
    relationship: PatientRelationship,
) -> PatientRelationship:
    """
    Verify a patient relationship.
    """
    relationship.verify()

    return relationship


@transaction.atomic
def terminate_relationship(
    *,
    relationship: PatientRelationship,
) -> PatientRelationship:
    """
    Terminate a patient relationship.
    """
    relationship.terminate()

    return relationship


@transaction.atomic
def delete_relationship(
    *,
    relationship: PatientRelationship,
) -> None:
    """
    Delete a patient relationship.
    """
    relationship.delete()


__all__ = [
    "create_relationship",
    "delete_relationship",
    "terminate_relationship",
    "update_relationship",
    "verify_relationship",
]
