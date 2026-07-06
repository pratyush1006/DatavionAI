"""
Prescription detail serializer.
"""

from __future__ import annotations

from apps.prescriptions.api.serializers.base import (
    PrescriptionBaseSerializer,
)


class PrescriptionDetailSerializer(
    PrescriptionBaseSerializer,
):
    """
    Serializer for prescription details.
    """


__all__ = [
    "PrescriptionDetailSerializer",
]
