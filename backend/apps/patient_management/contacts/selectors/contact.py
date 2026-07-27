"""
Selectors for patient contacts.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.contacts.models import Contact


def get_contact_by_id(
    contact_id: int,
) -> Contact:
    """
    Return a contact by its primary key.
    """
    return Contact.objects.get(
        pk=contact_id,
    )


def get_contact_by_value(
    *,
    organization_id: int,
    contact_type: str,
    value: str,
) -> Contact:
    """
    Return a contact by type and value.
    """
    return Contact.objects.get(
        organization_id=organization_id,
        contact_type=contact_type,
        value=value,
    )


def get_patient_contacts(
    *,
    patient_id: int,
) -> QuerySet[Contact]:
    """
    Return all contacts for a patient.
    """
    return (
        Contact.objects.filter(
            patient_id=patient_id,
        )
        .select_related(
            "organization",
            "patient",
        )
        .order_by(
            "-is_primary",
            "contact_type",
        )
    )


def get_primary_contact(
    *,
    patient_id: int,
    contact_type: str,
) -> Contact | None:
    """
    Return the primary contact for a patient and contact type.
    """
    return (
        Contact.objects.filter(
            patient_id=patient_id,
            contact_type=contact_type,
            is_primary=True,
        )
        .select_related(
            "organization",
            "patient",
        )
        .first()
    )


__all__ = [
    "get_contact_by_id",
    "get_contact_by_value",
    "get_patient_contacts",
    "get_primary_contact",
]
