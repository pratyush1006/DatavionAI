"""
CashTransaction selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.billing.cash_management.models import CashTransaction
from apps.platform.organizations.models import Organization
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class CashTransactionSelector:
    """
    Read-only queries for cash_transaction.
    """

    @staticmethod
    def queryset() -> QuerySet[CashTransaction]:
        """
        Return the base cash_transaction queryset.
        """

        return CashTransaction.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[CashTransaction]:
        """
        Return all cash_transaction records.
        """

        return CashTransactionSelector.queryset()

    @staticmethod
    def get(
        *,
        cash_transaction_id: UUID,
    ) -> CashTransaction:
        """
        Return a cash_transaction by identifier.
        """

        return get_object_or_404(
            CashTransactionSelector.queryset(),
            pk=cash_transaction_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[CashTransaction]:
        """
        Return all cash_transaction records for an organization.
        """

        return CashTransactionSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        cash_transaction_id: UUID,
    ) -> bool:
        """
        Determine whether a cash_transaction exists.
        """

        return (
            CashTransactionSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=cash_transaction_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of cash_transaction records for an organization.
        """

        return CashTransactionSelector.list_by_organization(
            organization=organization,
        ).count()


get_cash_transactions = CashTransactionSelector.list

get_cash_transaction_by_id = CashTransactionSelector.get

get_organization_cash_transactions = CashTransactionSelector.list_by_organization


__all__ = [
    "CashTransactionSelector",
    "get_cash_transaction_by_id",
    "get_cash_transactions",
    "get_organization_cash_transactions",
]
