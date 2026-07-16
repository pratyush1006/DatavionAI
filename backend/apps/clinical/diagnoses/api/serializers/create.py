"""
Diagnosis create serializer.
"""

from __future__ import annotations

from .base import DiagnosisBaseSerializer


class DiagnosisCreateSerializer(
    DiagnosisBaseSerializer,
):
    """
    Serializer for creating diagnoses.
    """


__all__ = [
    "DiagnosisCreateSerializer",
]
