"""
Patient Contact domain services.

Public service exports for the Contacts bounded context.
"""

from apps.patient_management.contacts.services.contact import (
    ContactService,
    activate_contact,
    create_contact,
    deactivate_contact,
    delete_contact,
    set_primary_contact,
    update_contact,
    verify_contact,
)

__all__ = (
    "ContactService",
    "activate_contact",
    "create_contact",
    "deactivate_contact",
    "delete_contact",
    "set_primary_contact",
    "update_contact",
    "verify_contact",
)
