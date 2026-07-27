"""
Create serializer for the Budget model.
"""

from __future__ import annotations

from apps.billing.financial_management.services import create_budget

from .base_budget import BudgetBaseSerializer
from .fields_budget import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class BudgetCreateSerializer(BudgetBaseSerializer):
    """
    Serializer used for creating budget records.
    """

    class Meta(BudgetBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a budget.
        """

        return create_budget(
            validated_data=validated_data,
        )


__all__ = [
    "BudgetCreateSerializer",
]
