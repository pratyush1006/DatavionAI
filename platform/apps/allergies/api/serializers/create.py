"""
Allergy create serializer.
"""

from __future__ import annotations

from apps.allergies.api.serializers.base import (
    AllergyBaseSerializer,
)


class AllergyCreateSerializer(
    AllergyBaseSerializer,
):
    """
    Serializer for creating allergies.
    """


__all__ = [
    "AllergyCreateSerializer",
]
