"""
Patient Contact selectors.

Public selector exports for the Contacts bounded context.
"""

from apps.patient_management.contacts.selectors.contact import (
    ContactSelector,
)

__all__ = ("ContactSelector",)
