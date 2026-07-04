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

    pass


__all__ = [
    "DiagnosisDetailSerializer",
]
