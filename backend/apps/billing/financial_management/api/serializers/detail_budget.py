"""
Detail serializer for the Budget model.
"""

from __future__ import annotations

from .base_budget import BudgetBaseSerializer
from .fields_budget import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class BudgetDetailSerializer(BudgetBaseSerializer):
    """
    Serializer used for retrieving budget details.
    """

    class Meta(BudgetBaseSerializer.Meta):
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "BudgetDetailSerializer",
]
