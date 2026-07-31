"""
Budget services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.billing.financial_management.models import Budget


class BudgetService:
    """
    Application service for budget write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> Budget:
        """
        Create a new budget.
        """

        instance = Budget(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Budget,
        validated_data: Mapping[str, Any],
        performed_by: Any | None = None,
    ) -> Budget:
        """
        Update an existing budget.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Budget,
        performed_by: Any | None = None,
    ) -> None:
        """
        Delete a budget.
        """

        instance.hard_delete()


create_budget = BudgetService.create

update_budget = BudgetService.update

delete_budget = BudgetService.delete


__all__ = [
    "BudgetService",
    "create_budget",
    "update_budget",
    "delete_budget",
]
