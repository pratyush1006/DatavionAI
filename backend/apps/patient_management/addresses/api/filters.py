"""
Filters for the Addresses API.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.addresses.models import Address


class AddressFilter(django_filters.FilterSet):
    """
    FilterSet for patient addresses.
    """

    class Meta:
        model = Address
        fields = {
            "address_type": ["exact"],
            "address_use": ["exact"],
            "status": ["exact"],
            "source": ["exact"],
            "is_primary": ["exact"],
            "patient": ["exact"],
            "organization": ["exact"],
            "city": ["exact", "icontains"],
            "state": ["exact", "icontains"],
            "country": ["exact", "icontains"],
        }


__all__ = [
    "AddressFilter",
]
