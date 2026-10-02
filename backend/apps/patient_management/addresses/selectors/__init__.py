"""Patient Address selectors."""

from __future__ import annotations

from .address import (
    get_address_by_id,
    get_address_by_uuid,
    get_primary_patient_address,
    list_addresses,
    list_organization_addresses,
    list_patient_addresses,
)

__all__ = (
    "get_address_by_id",
    "get_address_by_uuid",
    "get_primary_patient_address",
    "list_addresses",
    "list_organization_addresses",
    "list_patient_addresses",
)
