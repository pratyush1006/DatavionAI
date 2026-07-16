"""
Diagnosis detail serializer.
"""

from __future__ import annotations

from .fields import DiagnosisFieldsSerializer


class DiagnosisDetailSerializer(
    DiagnosisFieldsSerializer,
):
    """
    Serializer for diagnosis details.
    """


__all__ = [
    "DiagnosisDetailSerializer",
]
