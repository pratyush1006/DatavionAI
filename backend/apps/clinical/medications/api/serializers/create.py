"""
Medication create serializer.
"""

from __future__ import annotations

from apps.clinical.medications.api.serializers.base import (
    MedicationBaseSerializer,
)


class MedicationCreateSerializer(
    MedicationBaseSerializer,
):
    """
    Serializer for creating medications.
    """


__all__ = [
    "MedicationCreateSerializer",
]
