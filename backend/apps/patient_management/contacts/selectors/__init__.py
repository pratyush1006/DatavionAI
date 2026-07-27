"""
Selectors for the Contacts module.
"""

from .contact import (
    get_contact_by_id,
    get_contact_by_value,
    get_patient_contacts,
    get_primary_contact,
)

__all__ = [
    "get_contact_by_id",
    "get_contact_by_value",
    "get_patient_contacts",
    "get_primary_contact",
]
