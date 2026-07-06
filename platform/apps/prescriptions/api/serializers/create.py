"""
Prescription create serializer.
"""

from __future__ import annotations

from apps.prescriptions.api.serializers.base import (
    PrescriptionBaseSerializer,
)


class PrescriptionCreateSerializer(
    PrescriptionBaseSerializer,
):
    """
    Serializer for creating prescriptions.
    """


__all__ = [
    "PrescriptionCreateSerializer",
]
