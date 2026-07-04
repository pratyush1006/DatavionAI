"""
Medication update serializer.
"""

from __future__ import annotations

from apps.medications.api.serializers.base import (
    MedicationBaseSerializer,
)


class MedicationUpdateSerializer(
    MedicationBaseSerializer,
):
    """
    Serializer for updating medications.
    """

    pass


__all__ = [
    "MedicationUpdateSerializer",
]
