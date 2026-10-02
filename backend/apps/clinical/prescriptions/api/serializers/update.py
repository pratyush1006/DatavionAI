"""
Prescription update serializer.
"""

from __future__ import annotations

from apps.clinical.prescriptions.api.serializers.base import (
    PrescriptionBaseSerializer,
)


class PrescriptionUpdateSerializer(
    PrescriptionBaseSerializer,
):
    """
    Serializer for updating prescriptions.
    """


__all__ = [
    "PrescriptionUpdateSerializer",
]
