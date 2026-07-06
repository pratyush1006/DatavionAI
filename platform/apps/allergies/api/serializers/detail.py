"""
Allergy detail serializer.
"""

from __future__ import annotations

from apps.allergies.api.serializers.base import (
    AllergyBaseSerializer,
)


class AllergyDetailSerializer(
    AllergyBaseSerializer,
):
    """
    Serializer for allergy details.
    """


__all__ = [
    "AllergyDetailSerializer",
]
