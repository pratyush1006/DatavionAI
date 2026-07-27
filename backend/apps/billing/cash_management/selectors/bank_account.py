"""
BankAccount selectors.
"""

from __future__ import annotations

from uuid import UUID

from apps.billing.cash_management.models import BankAccount
from apps.platform.organizations.models import Organization
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class BankAccountSelector:
    """
    Read-only queries for bank_account.
    """

    @staticmethod
    def queryset() -> QuerySet[BankAccount]:
        """
        Return the base bank_account queryset.
        """

        return BankAccount.objects.select_related(
            "organization",
        )

    @staticmethod
    def list() -> QuerySet[BankAccount]:
        """
        Return all bank_account records.
        """

        return BankAccountSelector.queryset()

    @staticmethod
    def get(
        *,
        bank_account_id: UUID,
    ) -> BankAccount:
        """
        Return a bank_account by identifier.
        """

        return get_object_or_404(
            BankAccountSelector.queryset(),
            pk=bank_account_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[BankAccount]:
        """
        Return all bank_account records for an organization.
        """

        return BankAccountSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        bank_account_id: UUID,
    ) -> bool:
        """
        Determine whether a bank_account exists.
        """

        return (
            BankAccountSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=bank_account_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of bank_account records for an organization.
        """

        return BankAccountSelector.list_by_organization(
            organization=organization,
        ).count()


get_bank_accounts = BankAccountSelector.list

get_bank_account_by_id = BankAccountSelector.get

get_organization_bank_accounts = BankAccountSelector.list_by_organization


__all__ = [
    "BankAccountSelector",
    "get_bank_account_by_id",
    "get_bank_accounts",
    "get_organization_bank_accounts",
]
