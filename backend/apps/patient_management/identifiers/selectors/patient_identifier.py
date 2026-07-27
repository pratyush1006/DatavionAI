"""
Selectors for patient identifiers.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.identifiers.models import PatientIdentifier


def get_identifier_by_id(
    identifier_id: int,
) -> PatientIdentifier:
    """
    Return an identifier by its primary key.
    """
    return PatientIdentifier.objects.get(
        pk=identifier_id,
    )


def get_identifier_by_value(
    *,
    organization_id: int,
    identifier_type: str,
    identifier_value: str,
) -> PatientIdentifier:
    """
    Return an identifier by type and value.
    """
    return PatientIdentifier.objects.get(
        organization_id=organization_id,
        identifier_type=identifier_type,
        identifier_value=identifier_value,
    )


def get_patient_identifiers(
    *,
    patient_id: int,
) -> QuerySet[PatientIdentifier]:
    """
    Return all identifiers for a patient.
    """
    return (
        PatientIdentifier.objects.filter(
            patient_id=patient_id,
        )
        .select_related(
            "organization",
            "patient",
            "verified_by",
        )
        .order_by(
            "-is_primary",
            "identifier_type",
        )
    )


def get_primary_identifier(
    *,
    patient_id: int,
    identifier_type: str,
) -> PatientIdentifier | None:
    """
    Return the primary identifier for a patient and type.
    """
    return (
        PatientIdentifier.objects.filter(
            patient_id=patient_id,
            identifier_type=identifier_type,
            is_primary=True,
        )
        .select_related(
            "organization",
            "patient",
            "verified_by",
        )
        .first()
    )


__all__ = [
    "get_identifier_by_id",
    "get_identifier_by_value",
    "get_patient_identifiers",
    "get_primary_identifier",
]
