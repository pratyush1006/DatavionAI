"""Read-only Address selectors."""

from __future__ import annotations

from uuid import UUID

from apps.patient_management.addresses.models import Address


def list_addresses(*, tenant=None, organization=None, patient=None, active_only=True):
    qs = Address.objects.with_relations()
    if tenant is not None:
        qs = qs.filter(tenant=tenant)
    if organization is not None:
        qs = qs.filter(organization=organization)
    if patient is not None:
        qs = qs.filter(patient=patient)
    return qs.active() if active_only else qs


def list_organization_addresses(organization):
    return list_addresses(organization=organization)


def list_patient_addresses(patient):
    return list_addresses(patient=patient)


def get_address_by_id(address_id: UUID | str):
    return Address.objects.with_relations().get(pk=address_id)


def get_address_by_uuid(address_uuid: UUID | str):
    return get_address_by_id(address_uuid)


def get_primary_patient_address(patient):
    return (
        Address.objects.with_relations()
        .filter(patient=patient, is_primary=True)
        .exclude(status="inactive")
        .order_by("-created_at")
        .first()
    )
