"""
Medication detail serializer.
"""

from __future__ import annotations

from apps.clinical.medications.api.serializers.base import (
    MedicationBaseSerializer,
)


class MedicationDetailSerializer(
    MedicationBaseSerializer,
):
    """
    Serializer for medication details.
    """


__all__ = [
    "MedicationDetailSerializer",
]
