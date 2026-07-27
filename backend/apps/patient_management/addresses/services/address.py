"""
Services for patient addresses.
"""

from __future__ import annotations

from django.db import transaction

from apps.patient_management.addresses.models import Address


@transaction.atomic
def create_address(
    **validated_data: object,
) -> Address:
    """
    Create a patient address.
    """
    return Address.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_address(
    *,
    address: Address,
    **validated_data: object,
) -> Address:
    """
    Update a patient address.
    """
    for field, value in validated_data.items():
        setattr(
            address,
            field,
            value,
        )

    address.save()

    return address


@transaction.atomic
def delete_address(
    *,
    address: Address,
) -> None:
    """
    Delete a patient address.
    """
    address.delete()


__all__ = [
    "create_address",
    "delete_address",
    "update_address",
]
