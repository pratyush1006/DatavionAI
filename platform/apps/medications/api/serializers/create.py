"""
Medication create serializer.
"""

from __future__ import annotations

from apps.medications.api.serializers.base import (
    MedicationBaseSerializer,
)


class MedicationCreateSerializer(
    MedicationBaseSerializer,
):
    """
    Serializer for creating medications.
    """

    pass


__all__ = [
    "MedicationCreateSerializer",
]
