"""
Services for patient contacts.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.contacts.models import Contact


@transaction.atomic
def create_contact(
    **validated_data: object,
) -> Contact:
    """
    Create a patient contact.
    """
    return Contact.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_contact(
    *,
    contact: Contact,
    **validated_data: object,
) -> Contact:
    """
    Update a patient contact.
    """
    for field, value in validated_data.items():
        setattr(
            contact,
            field,
            value,
        )

    contact.save()

    return contact


@transaction.atomic
def delete_contact(
    *,
    contact: Contact,
) -> None:
    """
    Delete a patient contact.
    """
    contact.delete()


__all__ = [
    "create_contact",
    "delete_contact",
    "update_contact",
]
