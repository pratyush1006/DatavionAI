"""
Update serializer for Patient Addresses.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.addresses.models import Address


class AddressUpdateSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = Address
        fields = (
            "address_type",
            "address_use",
            "line_1",
            "line_2",
            "city",
            "state",
            "country",
            "postal_code",
            "is_primary",
        )


__all__ = ("AddressUpdateSerializer",)
