"""
List serializer for Patient Addresses.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.addresses.models import Address


class AddressListSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = Address
        fields = (
            "id",
            "patient",
            "address_type",
            "address_use",
            "line_1",
            "city",
            "state",
            "country",
            "postal_code",
            "status",
            "is_primary",
        )


__all__ = ("AddressListSerializer",)
