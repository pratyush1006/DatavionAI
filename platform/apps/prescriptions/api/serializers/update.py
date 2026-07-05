"""
Prescription update serializer.
"""

from __future__ import annotations

from apps.prescriptions.api.serializers.base import (
    PrescriptionBaseSerializer,
)


class PrescriptionUpdateSerializer(
    PrescriptionBaseSerializer,
):
    """
    Serializer for updating prescriptions.
    """

    pass


__all__ = [
    "PrescriptionUpdateSerializer",
]