"""
Patient Address services.
"""

from apps.patient_management.addresses.services.address import (
    AddressService,
    activate_address,
    create_address,
    deactivate_address,
    delete_address,
    set_primary_address,
    update_address,
    verify_address,
)

__all__ = (
    "AddressService",
    "activate_address",
    "create_address",
    "deactivate_address",
    "delete_address",
    "set_primary_address",
    "update_address",
    "verify_address",
)
