"""
Patient Contact authorization policies.

Public policy exports for the Contacts bounded context.
"""

from apps.patient_management.contacts.policies.contact import (
    ContactPolicy,
)

__all__ = ("ContactPolicy",)
