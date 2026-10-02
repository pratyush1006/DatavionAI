"""
Patient Contact selectors.

Public selector API for the Contacts bounded context.

The ContactSelector class remains the canonical tenant-aware selector.
The module-level get_contact_by_id function is retained as a compatibility
facade for existing callers and tests.
"""

from __future__ import annotations

from uuid import UUID

from apps.patient_management.contacts.models import Contact
from apps.patient_management.contacts.selectors.contact import ContactSelector


def get_contact_by_id(
    contact_id: UUID,
) -> Contact:
    """
    Retrieve a contact by primary key.

    This compatibility facade preserves the historical selector API.

    Production application services should prefer ContactSelector.get()
    when an explicit organization boundary is available.
    """
    return Contact.objects.select_related(
        "organization",
        "patient",
    ).get(
        pk=contact_id,
    )


__all__ = (
    "ContactSelector",
    "get_contact_by_id",
)
