"""
Filters for the Contacts API.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.contacts.models import Contact


class ContactFilter(django_filters.FilterSet):
    """
    FilterSet for patient contacts.
    """

    class Meta:
        model = Contact
        fields = {
            "contact_type": ["exact"],
            "purpose": ["exact"],
            "status": ["exact"],
            "source": ["exact"],
            "is_primary": ["exact"],
            "is_preferred": ["exact"],
            "patient": ["exact"],
            "organization": ["exact"],
        }


__all__ = [
    "ContactFilter",
]
