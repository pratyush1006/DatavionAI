"""
Update serializer for patient addresses.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.addresses.models import Address


class AddressUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a patient address.
    """

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
            "status",
            "source",
            "is_primary",
        )
