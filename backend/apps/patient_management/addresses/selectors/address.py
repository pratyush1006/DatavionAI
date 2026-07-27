"""
Selectors for patient addresses.
"""

from __future__ import annotations

from django.db.models import QuerySet

from apps.patient_management.addresses.models import Address


def get_address_by_id(
    address_id: int,
) -> Address:
    """
    Return an address by its primary key.
    """
    return Address.objects.get(
        pk=address_id,
    )


def get_address_by_value(
    *,
    organization_id: int,
    address_type: str,
    line_1: str,
    postal_code: str,
) -> Address:
    """
    Return an address by type, line 1, and postal code.
    """
    return Address.objects.get(
        organization_id=organization_id,
        address_type=address_type,
        line_1=line_1,
        postal_code=postal_code,
    )


def get_patient_addresses(
    *,
    patient_id: int,
) -> QuerySet[Address]:
    """
    Return all addresses for a patient.
    """
    return (
        Address.objects.filter(
            patient_id=patient_id,
        )
        .select_related(
            "organization",
            "patient",
        )
        .order_by(
            "-is_primary",
            "address_type",
        )
    )


def get_primary_address(
    *,
    patient_id: int,
    address_type: str,
) -> Address | None:
    """
    Return the primary address for a patient and address type.
    """
    return (
        Address.objects.filter(
            patient_id=patient_id,
            address_type=address_type,
            is_primary=True,
        )
        .select_related(
            "organization",
            "patient",
        )
        .first()
    )


__all__ = [
    "get_address_by_id",
    "get_address_by_value",
    "get_patient_addresses",
    "get_primary_address",
]
