"""
Emergency contact selectors.
"""

from .emergency_contact import (
    get_emergency_contact_by_uuid,
    get_primary_emergency_contact,
    list_emergency_contacts,
    list_organization_emergency_contacts,
    list_patient_emergency_contacts,
    search_emergency_contacts,
)

__all__ = [
    "get_emergency_contact_by_uuid",
    "get_primary_emergency_contact",
    "list_emergency_contacts",
    "list_organization_emergency_contacts",
    "list_patient_emergency_contacts",
    "search_emergency_contacts",
]
