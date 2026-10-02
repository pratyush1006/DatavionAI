"""
Emergency Contacts domain services.
"""

from .emergency_contact import (
    EmergencyContactService,
    activate_emergency_contact,
    block_emergency_contact,
    create_emergency_contact,
    deactivate_emergency_contact,
    delete_emergency_contact,
    set_primary_emergency_contact,
    update_emergency_contact,
    verify_emergency_contact,
)

__all__ = (
    "EmergencyContactService",
    "activate_emergency_contact",
    "block_emergency_contact",
    "create_emergency_contact",
    "deactivate_emergency_contact",
    "delete_emergency_contact",
    "set_primary_emergency_contact",
    "update_emergency_contact",
    "verify_emergency_contact",
)
