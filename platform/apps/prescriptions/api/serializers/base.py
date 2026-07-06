"""
Base prescription serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.prescriptions.models import Prescription


class PrescriptionBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for prescriptions.
    """

    class Meta:
        model = Prescription

        fields = (
            "id",
            "organization",
            "patient",
            "provider",
            "encounter",
            "medication",
            "prescription_number",
            "status",
            "dosage",
            "dosage_unit",
            "frequency",
            "quantity",
            "duration_days",
            "refills",
            "start_date",
            "end_date",
            "instructions",
            "is_prn",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


__all__ = [
    "PrescriptionBaseSerializer",
]
