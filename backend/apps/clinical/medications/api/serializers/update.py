"""
Medication update serializer.
"""

from __future__ import annotations

from apps.clinical.medications.api.serializers.base import (
    MedicationBaseSerializer,
)


class MedicationUpdateSerializer(
    MedicationBaseSerializer,
):
    """
    Serializer for updating medications.
    """


__all__ = [
    "MedicationUpdateSerializer",
]
