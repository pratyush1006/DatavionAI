"""
Medication list serializer.
"""

from __future__ import annotations

from apps.medications.api.serializers.base import (
    MedicationBaseSerializer,
)


class MedicationListSerializer(
    MedicationBaseSerializer,
):
    """
    Serializer for listing medications.
    """

    pass


__all__ = [
    "MedicationListSerializer",
]
