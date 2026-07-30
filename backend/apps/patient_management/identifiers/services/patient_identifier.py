"""
Services for patient identifiers.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.identifiers.models import (
    IdentifierVerification,
    PatientIdentifier,
)


@transaction.atomic
def create_patient_identifier(
    **validated_data: object,
) -> PatientIdentifier:
    """
    Create a patient identifier.
    """
    return PatientIdentifier.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_patient_identifier(
    *,
    identifier: PatientIdentifier,
    **validated_data: object,
) -> PatientIdentifier:
    """
    Update a patient identifier.
    """
    for field, value in validated_data.items():
        setattr(
            identifier,
            field,
            value,
        )

    identifier.save()

    return identifier


@transaction.atomic
def delete_patient_identifier(
    *,
    identifier: PatientIdentifier,
) -> None:
    """
    Delete a patient identifier.
    """
    identifier.delete()


@transaction.atomic
def verify_patient_identifier(
    *,
    identifier: PatientIdentifier,
    verification: IdentifierVerification,
) -> PatientIdentifier:
    """
    Verify a patient identifier.
    """
    identifier.verification_status = verification.status
    identifier.verified_by = verification.verified_by
    identifier.verified_at = verification.verified_at

    identifier.save(
        update_fields=[
            "verification_status",
            "verified_by",
            "verified_at",
            "updated_at",
        ],
    )

    return identifier


__all__ = [
    "create_patient_identifier",
    "delete_patient_identifier",
    "update_patient_identifier",
    "verify_patient_identifier",
]
