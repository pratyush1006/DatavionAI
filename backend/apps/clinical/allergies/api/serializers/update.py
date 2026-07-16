"""
Allergy update serializer.
"""

from __future__ import annotations

from apps.clinical.allergies.api.serializers.base import (
    AllergyBaseSerializer,
)


class AllergyUpdateSerializer(
    AllergyBaseSerializer,
):
    """
    Serializer for updating allergies.
    """


__all__ = [
    "AllergyUpdateSerializer",
]
