"""
Selectors for the Addresses module.
"""

from .address import (
    get_address_by_id,
    get_address_by_value,
    get_patient_addresses,
    get_primary_address,
)

__all__ = [
    "get_address_by_id",
    "get_address_by_value",
    "get_patient_addresses",
    "get_primary_address",
]
