"""
Filters for the Patient Addresses API.

Organization is deliberately not exposed as a client-controlled filter;
the API always applies the resolved organization boundary first.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.addresses.models import Address


class AddressFilter(
    django_filters.FilterSet,
):
    class Meta:
        model = Address
        fields = {
            "patient": ("exact",),
            "address_type": ("exact",),
            "address_use": ("exact",),
            "status": ("exact",),
            "source": ("exact",),
            "is_primary": ("exact",),
            "city": (
                "exact",
                "icontains",
            ),
            "state": (
                "exact",
                "icontains",
            ),
            "country": (
                "exact",
                "icontains",
            ),
        }


__all__ = ("AddressFilter",)
