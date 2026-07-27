"""
Detail serializer for patient addresses.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.addresses.models import Address


class AddressDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a patient address.
    """

    class Meta:
        model = Address
        fields = "__all__"
