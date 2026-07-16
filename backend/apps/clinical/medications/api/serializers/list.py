"""
Medication list serializer.
"""

from __future__ import annotations

from apps.clinical.medications.api.serializers.base import (
    MedicationBaseSerializer,
)


class MedicationListSerializer(
    MedicationBaseSerializer,
):
    """
    Serializer for listing medications.
    """


__all__ = [
    "MedicationListSerializer",
]
