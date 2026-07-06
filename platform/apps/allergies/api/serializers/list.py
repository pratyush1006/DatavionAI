"""
Allergy list serializer.
"""

from __future__ import annotations

from apps.allergies.api.serializers.base import (
    AllergyBaseSerializer,
)


class AllergyListSerializer(
    AllergyBaseSerializer,
):
    """
    Serializer for listing allergies.
    """


__all__ = [
    "AllergyListSerializer",
]
