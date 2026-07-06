"""
Diagnosis update serializer.
"""

from __future__ import annotations

from .base import DiagnosisBaseSerializer


class DiagnosisUpdateSerializer(
    DiagnosisBaseSerializer,
):
    """
    Serializer for updating diagnoses.
    """


__all__ = [
    "DiagnosisUpdateSerializer",
]
