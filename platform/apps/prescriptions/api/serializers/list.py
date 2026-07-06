"""
Prescription list serializer.
"""

from __future__ import annotations

from apps.prescriptions.api.serializers.base import (
    PrescriptionBaseSerializer,
)


class PrescriptionListSerializer(
    PrescriptionBaseSerializer,
):
    """
    Serializer for listing prescriptions.
    """


__all__ = [
    "PrescriptionListSerializer",
]
