"""
Patient Contact API permission classes.

Public permission exports for the Contacts bounded context.
"""

from apps.patient_management.contacts.permissions.contact import (
    CanActivateContact,
    CanCreateContact,
    CanDeactivateContact,
    CanDeleteContact,
    CanSetPrimaryContact,
    CanUpdateContact,
    CanVerifyContact,
    CanViewContact,
)

__all__ = (
    "CanActivateContact",
    "CanCreateContact",
    "CanDeactivateContact",
    "CanDeleteContact",
    "CanSetPrimaryContact",
    "CanUpdateContact",
    "CanVerifyContact",
    "CanViewContact",
)
