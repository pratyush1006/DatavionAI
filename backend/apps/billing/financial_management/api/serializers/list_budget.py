"""
List serializer for the Budget model.
"""

from __future__ import annotations

from .base_budget import BudgetBaseSerializer
from .fields_budget import (
    LIST_FIELDS,
    READ_ONLY_FIELDS,
)


class BudgetListSerializer(BudgetBaseSerializer):
    """
    Serializer used for listing budget records.
    """

    class Meta(BudgetBaseSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


__all__ = [
    "BudgetListSerializer",
]
