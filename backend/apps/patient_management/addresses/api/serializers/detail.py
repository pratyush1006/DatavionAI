"""
Detail serializer for Patient Addresses.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.addresses.models import Address


class AddressDetailSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = Address
        fields = (
            "id",
            "organization",
            "patient",
            "address_type",
            "address_use",
            "line_1",
            "line_2",
            "city",
            "state",
            "country",
            "postal_code",
            "status",
            "source",
            "is_primary",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "organization",
            "patient",
            "status",
            "created_at",
            "updated_at",
        )


__all__ = ("AddressDetailSerializer",)
