"""
Budget selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.billing.financial_management.models import Budget
from apps.platform.organizations.models import Organization


class BudgetSelector:
    """
    Read-only queries for budget.
    """

    @staticmethod
    def queryset() -> QuerySet[Budget]:
        """
        Return the base budget queryset.
        """

        return Budget.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[Budget]:
        """
        Return all budget records.
        """

        return BudgetSelector.queryset()

    @staticmethod
    def get(
        *,
        budget_id: UUID,
    ) -> Budget:
        """
        Return a budget by identifier.
        """

        return get_object_or_404(
            BudgetSelector.queryset(),
            pk=budget_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Budget]:
        """
        Return all budget records for an organization.
        """

        return BudgetSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        budget_id: UUID,
    ) -> bool:
        """
        Determine whether a budget exists.
        """

        return (
            BudgetSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=budget_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of budget records for an organization.
        """

        return BudgetSelector.list_by_organization(
            organization=organization,
        ).count()


get_budgets = BudgetSelector.list

get_budget_by_id = BudgetSelector.get

get_organization_budgets = BudgetSelector.list_by_organization


__all__ = [
    "BudgetSelector",
    "get_budget_by_id",
    "get_budgets",
    "get_organization_budgets",
]
