"""
Detail serializers for the Laboratories application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.laboratories.api.serializers.laboratory_order.base import (
    LaboratoryOrderSerializer,
)


class LaboratoryOrderDetailSerializer(
    LaboratoryOrderSerializer,
):
    """
    Serializer for retrieving laboratory order details.
    """

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    provider_name = serializers.CharField(
        source="provider.full_name",
        read_only=True,
    )

    encounter_number = serializers.CharField(
        source="encounter.encounter_number",
        read_only=True,
    )

    class Meta(
        LaboratoryOrderSerializer.Meta,
    ):
        """
        Serializer metadata.
        """

        fields = (
            *LaboratoryOrderSerializer.Meta.fields,
            "patient_name",
            "provider_name",
            "encounter_number",
        )

        read_only_fields = (
            *LaboratoryOrderSerializer.Meta.read_only_fields,
            "patient_name",
            "provider_name",
            "encounter_number",
        )


__all__ = [
    "LaboratoryOrderDetailSerializer",
]
