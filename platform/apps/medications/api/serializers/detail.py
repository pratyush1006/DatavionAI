"""
Medication detail serializer.
"""

from __future__ import annotations

from apps.medications.api.serializers.base import (
    MedicationBaseSerializer,
)


class MedicationDetailSerializer(
    MedicationBaseSerializer,
):
    """
    Serializer for medication details.
    """

    pass


__all__ = [
    "MedicationDetailSerializer",
]
