"""
Update serializer for the Budget model.
"""

from __future__ import annotations

from apps.billing.financial_management.models import Budget
from apps.billing.financial_management.services import update_budget

from .base_budget import BudgetBaseSerializer
from .fields_budget import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class BudgetUpdateSerializer(BudgetBaseSerializer):
    """
    Serializer used for updating budget records.
    """

    class Meta(BudgetBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: Budget,
        validated_data: dict[str, object],
    ) -> Budget:
        """
        Update a budget.
        """

        return update_budget(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "BudgetUpdateSerializer",
]
